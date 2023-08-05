import uuid
import time
import os
import datetime
from sync.base import BaseSync
from utils.code import get_md5_hash
from classcard_dataclient.models.course import CourseTableManager, Course
from classcard_dataclient.models.subject import Subject
from utils.loggerutils import logging
from utils.dateutils import date2str
from requester.sdtu import SDTURequester
from config import SDTU_PAGE_SIZE

logger = logging.getLogger(__name__)


class CourseTableSync(BaseSync):
    def __init__(self):
        super(CourseTableSync, self).__init__()
        self.xn = None
        self.yjs_xq = None
        self.bks_xq = None
        self.table_begin_date = None
        self.table_end_date = None
        self.sdtu_requester = SDTURequester()
        self.get_bks_semester_info()
        self.get_yjs_semester_info()
        now = datetime.datetime.now()
        today = date2str(now)
        manager_number = str(uuid.uuid4())[:19]
        manager_name = "{}-{}-{}-{}".format(self.xn, self.bks_xq, today, manager_number[:4])
        self.manager = CourseTableManager(name=manager_name, number=manager_number,
                                          begin_date=self.table_begin_date, end_date=self.table_end_date)
        self.course_map = {}
        self.space_map = {}
        self.space_container = {}
        self.subject_map = {}
        self.subject_number_name = {}
        self.need_relate_student = True
        self.yjs_classroom_map = {}
        self.bks_classroom_map = {}

    def get_bks_semester_info(self):
        semester_res = self.sdtu_requester.get_bks_semester(page=1, pagesize=SDTU_PAGE_SIZE)
        data_list = semester_res["data"]["Rows"]
        data_list = sorted(data_list, key=lambda d: d["KSRQ"], reverse=True)
        if data_list:
            current_semester = data_list[0]
            self.table_begin_date, self.table_end_date = current_semester["KSRQ"], current_semester["JSRQ"]
            self.xn, self.bks_xq = current_semester["XN"], current_semester["XQDM"]

    def get_yjs_semester_info(self):
        semester_res = self.sdtu_requester.get_yjs_semester(page=1, pagesize=SDTU_PAGE_SIZE)
        data_list = semester_res["data"]["Rows"]
        data_list = sorted(data_list, key=lambda d: d["BEGINDATE"], reverse=True)
        if data_list:
            current_semester = data_list[0]
            self.yjs_xq = current_semester["TERMCODE"]

    def process_subject_info(self, subject_name):
        if not subject_name:
            return None
        subject_name = subject_name.replace(" ", "")
        subject_number = get_md5_hash(subject_name)
        if subject_number in self.subject_number_name:
            info = self.subject_number_name[subject_number]
        else:
            info = {'name': subject_name, 'number': subject_number, 'ori_num': subject_number}
            self.subject_number_name[subject_number] = info
            self.subject_map[subject_number] = Subject(number=subject_number, name=subject_name)
        return info

    def analyse_sksj(self, sksj):
        try:
            if "星期" not in sksj:
                return None
            week_map = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "日": 7}
            index_map = {"上午": 0, "下午": 4, "晚上": 8}
            sksj = sksj.replace(";", ":").replace("；", ":")
            sksj_split = sksj.split(":")
            week_range = sksj_split[0][1:-1].split("-")
            begin_week, end_week = int(week_range[0]), int(week_range[1])
            schedule_info = sksj_split[1]
            single = 0
            if "单周" in schedule_info:
                single = 1
            elif "双周" in schedule_info:
                single = 2
            week_info = schedule_info.split("-")[0][-1]
            week = week_map.get(week_info, None)
            position_info = schedule_info.split("-")[-1].split(",")
            positions = []
            for info in position_info:
                r_info = info[1:] if info[0] == ' ' else info
                index = index_map.get(r_info[:2], 0)
                num = index + int(r_info[-1])
                positions.append((num, week))
            result = {'begin_week': begin_week, 'end_week': end_week, 'single': single, "positions": positions}
        except (Exception,) as e:
            result = self.analyse_sksj_b(sksj)
            return result
        return result

    def analyse_sksj_b(self, sksj):
        try:
            if "星期" not in sksj:
                return None
            week_map = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "日": 7}
            index_map = {"上午": 0, "下午": 4, "晚上": 8}
            sksj_split = sksj.split(":")
            week_range = sksj_split[0][1:-1].split("-")
            begin_week, end_week = int(week_range[0]), int(week_range[1])
            schedule_info = sksj_split[1]
            single = 0
            if "单周" in schedule_info:
                single = 1
            elif "双周" in schedule_info:
                single = 2
            position_info = schedule_info.split("  ")[-1].split(",")
            positions = []
            for info in position_info:
                r_info = info[1:] if info[0] == ' ' else info
                week = week_map.get(r_info[2], None)
                index = index_map.get(r_info[4:6], 0)
                try:
                    begin_num, end_num = index + int(r_info[6]), index + int(r_info[10])
                except (ValueError,):
                    index = index_map.get(r_info[5:7], 0)
                    begin_num, end_num = index + int(r_info[7]), index + int(r_info[7])
                for num in range(begin_num, end_num + 1):
                    positions.append((num, week))
            result = {'begin_week': begin_week, 'end_week': end_week, 'single': single, "positions": positions}
        except (Exception,) as e:
            self.record("{}\n".format(sksj))
            return None
        return result

    def get_yjs_course(self):
        course_map = {}
        page_index = 1
        while True:
            course_res = self.sdtu_requester.get_yjs_course_table(page=page_index, pagesize=SDTU_PAGE_SIZE,
                                                                  params={"XQ": str(self.yjs_xq)})
            total_count = course_res["total"]
            current_rows = course_res["data"]["Rows"]
            for row in current_rows:
                subject_name = row["KCMC"]
                if not subject_name:
                    continue
                subject_info = self.process_subject_info(subject_name)
                subject_name, subject_number = subject_info['name'], subject_info['number']
                teacher_number = row["ZJJSBH"]
                classroom_yjs_num = row["JSBH"]
                classroom_num = self.yjs_classroom_map.get(classroom_yjs_num)
                time_info = row["SKSJMS"]
                if not (time_info and classroom_num):
                    continue
                time_result = self.analyse_sksj(time_info)
                if not time_result:
                    continue
                try:
                    course_name = classroom_num + subject_number + teacher_number
                except (Exception,):
                    continue
                if course_name in course_map:
                    course = course_map[course_name]
                else:
                    course_number = get_md5_hash(course_name)
                    course = Course(number=course_number, name=course_name[:63], teacher_number=teacher_number,
                                    classroom_number=classroom_num, subject_number=subject_number,
                                    begin_week=time_result['begin_week'], end_week=time_result['end_week'],
                                    required_student=False, is_present=True)
                    self.course_map[course_name] = course
                for position in time_result['positions']:
                    course.add_position(position[0], position[1], time_result['single'])
            if page_index * SDTU_PAGE_SIZE >= total_count:
                break
            page_index += 1
        return course_map

    def analyse_position(self, jc, week):
        course_week = int(week)
        position = []
        jc_items = jc.split('-')
        if len(jc_items) == 1:
            position.append((int(jc_items[0]), course_week))
        elif len(jc_items) == 2:
            for item in range(int(jc_items[0]), int(jc_items[1]) + 1):
                position.append((item, course_week))
        return position

    def combine_course(self):
        new_course_map = {}
        for space_name, container in self.space_container.items():
            sorted_c = sorted(container, key=lambda c: c.name)
            choose_c = sorted_c[0]
            self.space_map[space_name] = choose_c
            if choose_c.name not in new_course_map:
                new_course_map[choose_c.name] = choose_c
        self.course_map = new_course_map

    def get_bk_course(self):
        single_map = {"单": 1, "双": 2}
        page_index = 1
        while True:
            course_res = self.sdtu_requester.get_teacher_course_table(page=page_index, pagesize=SDTU_PAGE_SIZE,
                                                                      params={"XQ": str(self.bks_xq),
                                                                              "XN": str(self.xn)})
            total_count = course_res["total"]
            current_rows = course_res["data"]["Rows"]
            for row in current_rows:
                subject_name = row["KCMC"]
                if not subject_name:
                    continue
                subject_info = self.process_subject_info(subject_name)
                subject_name, subject_number = subject_info['name'], subject_info['number']
                class_number = row["SKBJH"]
                classroom_name = row["SKDD"]
                teacher_number = row["RKJSGH"]
                week_range = row["ZC"]
                week, num = row["XQJ"], row["JC"]
                single = single_map.get(row["DSZ"], 0)
                if not (week_range and classroom_name and week and num and teacher_number):
                    continue
                classroom_num = self.bks_classroom_map.get(classroom_name, None) or get_md5_hash(classroom_name)
                week_range = week_range.replace("周", "")
                begin_week, end_week = int(week_range.split("-")[0]), int(week_range.split("-")[-1])
                try:
                    space_name = classroom_num + week_range + num + week + str(single)
                    course_name = classroom_name + subject_number + teacher_number + str(class_number)
                except (Exception,) as e:
                    continue
                if course_name in self.course_map:
                    course = self.course_map[course_name]
                else:
                    course_number = get_md5_hash(course_name)
                    course = Course(number=course_number, name=course_name[:63], teacher_number=teacher_number,
                                    classroom_number=classroom_num, subject_number=subject_number, is_present=True,
                                    begin_week=begin_week, end_week=end_week, required_student=False)
                    self.course_map[course_name] = course

                positions = self.analyse_position(num, week)
                for position in positions:
                    course.add_position(position[0], position[1], single)
                if space_name not in self.space_container:
                    self.space_container[space_name] = []
                if course_name not in self.space_container[space_name]:
                    self.space_container[space_name].append(course)
            if page_index * SDTU_PAGE_SIZE >= total_count:
                break
            page_index += 1

    def relate_student(self):
        single_map = {"单": 1, "双": 2}
        page_index = 1
        while True:
            course_res = self.sdtu_requester.get_bks_course_table(page=page_index, pagesize=SDTU_PAGE_SIZE,
                                                                  params={"XQ": str(self.bks_xq),
                                                                          "XN": str(self.xn)})
            total_count = course_res["total"]
            current_rows = course_res["data"]["Rows"]
            for row in current_rows:
                subject_name = row["KCMC"]
                classroom_name = row["SKDD"]
                week_range = row["ZC"]
                week, num = row["XQJ"], row["JC"]
                single = single_map.get(row["DSZ"], 0)
                student_number = row["XH"]
                if not (week_range and classroom_name and subject_name and week and num):
                    continue
                classroom_num = self.bks_classroom_map.get(classroom_name, None) or get_md5_hash(classroom_name)
                try:
                    space_name = classroom_num + week_range + num + week + str(single)
                except (Exception,):
                    continue
                course = self.space_map.get(space_name, None)
                if course:
                    course.add_student(student_number)
            if page_index * SDTU_PAGE_SIZE >= total_count:
                break
            page_index += 1

    def analyse_rent_num(self, num_range):
        num_list = []
        jc_items = num_range.split('-')
        if len(jc_items) == 1:
            num_list = [int(jc_items[0])]
        elif len(jc_items) == 2:
            for item in range(int(jc_items[0]), int(jc_items[1]) + 1):
                num_list.append(item)
        return num_list

    def get_rent_classroom(self):
        """同步教室借用变成课程表"""
        course_map = {}
        single_map = {"单": 1, "双": 2}
        page_index = 1
        while True:
            course_res = self.sdtu_requester.get_rent_classroom_list(page=page_index, pagesize=SDTU_PAGE_SIZE,
                                                                     params={"XQ": str(self.bks_xq),
                                                                             "XN": str(self.xn)})
            total_count = course_res["total"]
            current_rows = course_res["data"]["Rows"]
            for row in current_rows:
                classroom_name = row["JSBH"]
                begin_week, end_week = row["KSZ"], row["JSZ"]
                single_sign = row.get("DSZ")
                single = single_map.get(single_sign, 0)
                week, num_range = row["XQJ"], row["JC"]
                group_name, teacher_number = row["JYDW"], row["JSBH1"]
                if not (classroom_name and begin_week and end_week and week and num_range):
                    continue
                begin_week = begin_week.replace("第", "").replace("周", "")
                end_week = end_week.replace("第", "").replace("周", "")
                begin_week, end_week = int(begin_week), int(end_week)
                classroom_num = self.bks_classroom_map.get(classroom_name, None) or get_md5_hash(classroom_name)
                num_list = self.analyse_rent_num(num_range)
                subject_name = "{}借用".format(group_name)
                subject_info = self.process_subject_info(subject_name)
                subject_name, subject_number = subject_info['name'], subject_info['number']
                try:
                    course_name = classroom_name + subject_name + str(teacher_number) + str(begin_week) + str(end_week)
                except (Exception,):
                    continue
                if course_name in course_map:
                    course = course_map[course_name]
                else:
                    course_number = get_md5_hash(course_name)
                    course_data = dict(number=course_number, name=course_name[:63], classroom_number=classroom_num,
                                       subject_number=subject_number, is_present=True, begin_week=begin_week,
                                       end_week=end_week, required_student=False)
                    if teacher_number:
                        course_data[teacher_number] = teacher_number
                    course = Course(**course_data)
                    course_map[course_name] = course
                for num in num_list:
                    course.add_position(num, int(week), single)
            if page_index * SDTU_PAGE_SIZE >= total_count:
                break
            page_index += 1
        return course_map

    def sync(self):
        self.record(">>>Start course sync")
        t1 = time.time()
        # self.get_bk_course()
        self.combine_course()
        self.record(">>>Total have {} courses".format(len(self.course_map)))
        # if self.need_relate_student:
        #     self.relate_student()
        self.record(">>>Get yjs course")
        yjs_course = self.get_yjs_course()
        self.course_map.update(yjs_course)
        self.record(">>>Get rent classroom")
        rent_course = self.get_rent_classroom()
        self.course_map.update(rent_course)
        self.record(">>>Start upload subjects")
        subjects = list(self.subject_map.values())
        self.client.create_subjects(self.school_id, subjects, new_name=True)
        self.record(">>>Finish upload subject")
        for number, course in self.course_map.items():
            self.manager.add_course(course)
        t2 = time.time()
        self.record(">>>Finish data process, cost {}s".format(t2 - t1))
        t3 = time.time()
        self.record(">>>Start upload course table")
        self.client.create_course_table(self.school_id, self.manager, is_active=False)
        t4 = time.time()
        self.record(">>>Finish upload course table, cost {}s".format(t4 - t3))
        self.record(">>>Active course table, Delete old table")
        self.client.active_course_table(self.school_id, self.manager, delete_other=True)
        t5 = time.time()
        self.record(">>>Total cost {}s".format(t5 - t1))

    def record(self, info):
        now = datetime.datetime.now()
        print(str(now), info)
        dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(dir_path, "course_info.txt")
        with open(file_path, "a+") as f:
            f.write("{} >>> {} \n".format(now, info))