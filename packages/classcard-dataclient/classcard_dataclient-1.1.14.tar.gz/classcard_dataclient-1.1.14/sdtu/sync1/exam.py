import datetime
import uuid
import time
from classcard_dataclient.models.course import CourseTableManager, Course
from classcard_dataclient.models.subject import Subject
from sync.base import BaseSync
from utils.loggerutils import logging
from utils.dateutils import date2str, str2datetime, str2_time, str2_date
from utils.code import get_md5_hash
from config import TABLE_BEGIN_DATE, TABLE_END_DATE, TABLE_YJS_SEMESTER, TABLE_YEAR, TABLE_SEMESTER

logger = logging.getLogger(__name__)


class ExamSync(BaseSync):
    def __init__(self):
        super(ExamSync, self).__init__()
        self.xn = TABLE_YEAR
        self.yjs_xq = TABLE_YJS_SEMESTER
        self.xq = TABLE_SEMESTER
        self.begin_date = str2_date(TABLE_BEGIN_DATE)
        self.end_date = str2_date(TABLE_END_DATE)
        self.course_map = {}
        self.min_num = None
        self.min_time = None
        self.max_num = None
        self.max_time = None
        self.new_manager = False
        self.manager = self._init_manager()
        self.time_slot = self._get_schedule()
        self.subject = self._init_subject()

    def _init_subject(self):
        f_subject_name = "考试"
        subject_number = get_md5_hash(f_subject_name)
        subject = Subject(number=subject_number, name=f_subject_name)
        return subject

    def _init_manager(self):
        manager_res = self.client.get_active_table(self.school_id)
        if manager_res:
            manager_data = manager_res[0]
            manager = CourseTableManager(uid=manager_data['uid'], name=manager_data['name'],
                                         number=manager_data['number'], begin_date=TABLE_BEGIN_DATE,
                                         end_date=TABLE_END_DATE)
        else:
            self.new_manager = True
            now = datetime.datetime.now()
            today = date2str(now)
            manager_number = str(uuid.uuid4())[:19]
            manager_name = "{}-{}-{}-{}".format(self.xn, self.xq, today, manager_number[:4])
            manager = CourseTableManager(name=manager_name, number=manager_number,
                                         begin_date=TABLE_BEGIN_DATE, end_date=TABLE_END_DATE)
        return manager

    def _get_schedule(self):
        pre_time_slot, time_slot = {}, {}
        schedule_res = self.client.get_active_schedule(self.school_id)
        if not schedule_res:
            return time_slot
        for s in schedule_res:
            if s['num'] not in pre_time_slot:
                pre_time_slot[s['num']] = {"start_time": s["start_time"], "stop_time": s["stop_time"]}
        for ts, tc in pre_time_slot.items():
            if self.min_num is None or ts <= self.min_num:
                self.min_num, self.min_time = ts, str2_time(tc["start_time"])
            if self.max_num is None or ts >= self.max_num:
                self.max_num, self.max_time = ts, str2_time(tc["stop_time"])
            pre_num = ts - 1
            if pre_num in pre_time_slot:
                start_time = pre_time_slot[pre_num]["stop_time"]
            else:
                start_time = tc["start_time"]
            time_slot[ts] = {"start_time": str2_time(start_time), "stop_time": str2_time(tc["stop_time"])}
        return time_slot

    def get_week_num(self, index_date):
        pass_days = (index_date - self.begin_date).days + 1 + self.begin_date.weekday()
        week_num = (pass_days - 1) // 7 + 1
        return week_num

    def get_time_slot(self, time_info):
        if time_info >= self.max_time:
            return self.max_num
        if time_info <= self.min_time:
            return self.min_num
        for ts, info in self.time_slot.items():
            if info["stop_time"] >= time_info >= info["start_time"]:
                return ts

    def exam2course(self):
        exam = self.client.get_future_exam_classroom(self.school_id)
        if not exam:
            logger.info("没有未进行的考试信息")
            return
        for e in exam:
            subject_info = e['subject'] or {}
            subject_name, subject_number = subject_info.get("name", ""), subject_info.get("number", None)
            classroom_info = e['classroom'] or {}
            classroom_number = classroom_info.get("num")
            start_time = str2datetime(e['start_time'])
            end_time = str2datetime(e['end_time'])
            begin_week, end_week = self.get_week_num(start_time), self.get_week_num(end_time)
            index, day_len = 0, (end_time.date() - start_time.date()).days
            current_week, week_num = start_time.weekday() + 1, begin_week
            for day in range(day_len + 1):
                if current_week > 7:
                    current_week -= 7
                    week_num += 1
                course_name = "{}考试_{}_{}".format(subject_name, classroom_number, week_num)
                course_number = get_md5_hash(course_name)
                if course_number in self.course_map:
                    course = self.course_map[course_number]
                else:
                    course = Course(number=course_number, name=course_number, classroom_number=classroom_number,
                                    subject_number=self.subject.number, is_present=False,
                                    begin_week=week_num, end_week=week_num, required_student=False)
                    self.course_map[course_number] = course
                begin_slot = self.get_time_slot(start_time.time()) if index == 0 else self.min_num
                end_slot = self.get_time_slot(end_time.time()) if index == day_len else self.max_num
                for slot in range(begin_slot, end_slot + 1):
                    course.add_position(slot, current_week, 0)
                index += 1
                current_week += 1

    def sync(self):
        if not self.time_slot:
            logger.info("没有设置作息，无法判断时间")
            return
        self.exam2course()
        if not self.course_map:
            logger.info("没有未进行的考试信息")
            return
        for number, course in self.course_map.items():
            self.manager.add_course(course)
        self.client.create_subjects(self.school_id, [self.subject], new_name=True)
        self.client.create_course_table(self.school_id, self.manager, is_active=False, create_manager=self.new_manager)
