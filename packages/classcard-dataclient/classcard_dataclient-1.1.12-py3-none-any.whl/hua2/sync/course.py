import datetime
import uuid
from sync.base import BaseSync
from utils.loggerutils import logging
from utils.code import get_md5_hash
from classcard_dataclient.models.course import CourseV2, CourseTableManagerV2, TableCategory, WalkingModeSet

logger = logging.getLogger(__name__)


class CourseSync(BaseSync):
    def __init__(self):
        super(CourseSync, self).__init__()
        self.offset = 300
        self.course_map = {}
        self.space_map = {}
        self.slot_map = {}
        self.student_map = {}
        self.teacher_map = {}
        self.classroom_map = {}
        self.class_set = {}
        self.classroom_set = {}
        self.class_name_num = {}
        self.rest_table = None
        self.semester = None
        self.course_name_list = []
        self.slot_course_table = {}  # {"slot_id" : "course_table_name"}
        self.course_container = {}  # {"course_table_name" : [course, course]}
        self.rest_table_slot = {}  # {"rest_name": [slot_id, slot_id, slot_id]}
        self.course_table_managers = {}
        self.classroom_sign = {}
        self.class_sign = {}
        self.student_section_map = {}

    def create_course_manager(self):
        """
        根据多作息，创建多课表
        :return:
        """
        begin_date, end_date = self.get_date_range(days=60)
        for rest_name, slot_list in self.rest_table_slot.items():
            course_table_name = "{}课表_{}".format(rest_name, str(uuid.uuid4())[:4])
            course_table_number = get_md5_hash(course_table_name)[:20]
            course_table_manager = CourseTableManagerV2(name=course_table_name, number=course_table_number,
                                                        rest_name=rest_name, walking_mode=WalkingModeSet.WALKING,
                                                        begin_date=begin_date, end_date=end_date,
                                                        semester_name=self.semester.name)
            for slot_id in slot_list:
                self.slot_course_table[slot_id] = course_table_name
            self.course_table_managers[course_table_name] = course_table_manager
            self.class_set[course_table_name] = set()
            self.classroom_set[course_table_name] = set()
            self.course_container[course_table_name] = []

    # def get_double_map(self):
    #     double_name = {"C2-413": ["C2-413-1", "C2-413-2"],
    #                    "小学阅览室": ["小学阅览室-1", "小学阅览室-2"],
    #                    "大会议室203人": ["大会议室203人-1", "大会议室203人-2"],
    #                    "A3-314": ["A3-314-1", "A3-314-2"]}
    #     double_number = {}
    #     for ori, dst_list in double_name.items():
    #         ori_number = get_md5_hash(ori)
    #         double_number[ori_number] = []
    #         for dst in dst_list:
    #             dst_number = get_md5_hash(dst)
    #             double_number[ori_number].append(dst_number)
    #     return double_number

    def get_double_map(self):
        double_number = {"1xx": ["1_A", "1_B"],
                         "2xx": ["2_A", "2_B"],
                         "3xx": ["3_A", "3_B"],
                         "4xx": ["4_A", "4_B"]}
        return double_number

    def create_unique_course_name(self, subject_name, class_name):
        course_name = "{}_{}".format(subject_name, class_name) if class_name else subject_name
        new_course_name = course_name
        while True:
            if new_course_name not in self.course_name_list:
                break
            new_course_name = "{}_{}".format(course_name, str(uuid.uuid4())[:3])
        self.course_name_list.append(new_course_name)
        return new_course_name

    def extract_course(self):
        double_number_map = self.get_double_map()
        today, last_day = self.get_date_range()
        # today, last_day = "2020-11-02", "2020-11-08"
        sql = "SELECT id, coursename, sectionid, classroomid, coursedate, weekday, userid, isteacher, deptname, outid " \
              "FROM mid_attendschedule " \
              "WHERE updateflag!='3' and coursedate > '{}' and coursedate <= '{}' " \
              "ORDER BY weekday".format(today, last_day)
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        for row in rows:
            category = TableCategory.ALL
            attend_id, subject_name, slot_id = row[0], row[1], row[2]
            classroom_id, course_date, week = row[3], row[4], row[5]
            user_id, is_teacher, class_name, user_number = row[6], row[7], row[8], row[9]
            # unique_key = "{}_{}".format(subject_name, classroom_id)
            subject_number = get_md5_hash(subject_name)
            num = self.slot_map.get(slot_id, None)
            if not num:
                print("Can't Find SlotID {}".format(slot_id))
                continue
            current_course_table = self.slot_course_table.get(slot_id)
            if not current_course_table:
                print("Can't Find SlotID {}".format(slot_id))
                continue
            # ori_classroom_number = self.classroom_map.get(str(classroom_id))
            ori_classroom_number = str(classroom_id)
            if ori_classroom_number == '11425':
                print("1")
            classroom_numbers = double_number_map.get(ori_classroom_number, [ori_classroom_number])
            for classroom_number in classroom_numbers:
                # 检测教室是否在其他作息课表出现,如果出现，就跳过
                exist_classroom_sign = self.classroom_sign.get(classroom_number)
                if exist_classroom_sign and current_course_table != exist_classroom_sign:
                    print("该教室{}已在{}课表出现，请检查数据".format(classroom_number, exist_classroom_sign))
                    continue

                unique_key = "{}_{}_{}_{}".format(subject_name, classroom_number, slot_id, week)
                course_number = get_md5_hash(unique_key)
                if course_number not in self.course_map:
                    course_name = self.create_unique_course_name(subject_name, class_name=class_name)
                    course_data = {'name': course_name, 'number': course_number, 'subject_number': subject_number,
                                   "subject_name": subject_name, 'classroom_number': classroom_number,
                                   'is_walking': True, "teacher_number": None, "begin_week": 1, "end_week": 1,
                                   'student_list': []}
                    course = CourseV2(**course_data)
                    # course.class_name = class_name
                    course.required_student = False
                    self.course_map[course_number] = course
                    self.classroom_set[current_course_table].add(classroom_number)
                    self.classroom_sign[classroom_number] = current_course_table
                    self.course_container[current_course_table].append(course)
                else:
                    course = self.course_map[course_number]
                if is_teacher:
                    if str(user_id) in ["1", "4"]:
                        continue
                    teacher_number = user_number
                    if teacher_number:
                        course.teacher_number = teacher_number
                else:
                    student_number = user_number
                    if student_number:
                        course.add_student(student_number)
                    class_name = self.student_section_map.get(student_number)
                    if class_name and class_name in self.class_name_num:
                        exist_class_sign = self.class_sign.get(class_name)
                        if exist_class_sign and current_course_table != exist_class_sign:
                            print("该班级{}已在{}课表出现，请检查数据".format(class_name, exist_class_sign))
                            continue
                        self.class_set[current_course_table].add(self.class_name_num[class_name])
                        self.class_sign[class_name] = current_course_table
                course.add_position(num, week, category, classroom_number)

    def sync(self):
        self.create_course_manager()
        self.extract_course()
        if not self.course_map:
            logger.info("没有课程信息")
            return
        # begin_date, end_date = self.get_date_range(days=60)
        # course_table_name = "{}课表_{}".format(self.semester.name, str(uuid.uuid4())[:4])
        # course_table_number = get_md5_hash(course_table_name)[:20]
        for course_table_name, course_table in self.course_table_managers.items():
            # course_table = CourseTableManagerV2(name=course_table_name, number=course_table_number,
            #                                     rest_name=self.rest_table.name, walking_mode=WalkingModeSet.WALKING,
            #                                     begin_date=begin_date, end_date=end_date, semester_name=self.semester.name)
            course_table.classrooms_num = list(self.classroom_set[course_table_name])
            course_table.sections_num = list(self.class_set[course_table_name])
            course_table.courses = list(self.course_container[course_table_name])
            print(">>> CREATE_COURSE_TABLE': {}".format(course_table_name))
            logger.info(">>> CREATE_COURSE_TABLE")
            self.client.create_course_table(self.school_id, course_table, is_active=True)
        self.client.active_semester(self.school_id, self.semester, delete_other=True)
        self.close_db()
