import datetime
from sync import BaseSync1
from classcard_dataclient.models.course import CourseV1, CourseTableManagerV1
from classcard_dataclient.models.schedule import RestSchedule, RestTable, PeriodSet
from utils.code import b64encode
from utils.loggerutils import logging
from utils.dateutils import str2datetime, time2str

logger = logging.getLogger(__name__)


class CourseSyncV1(BaseSync1):
    def __init__(self, *args, **kwargs):
        super(CourseSyncV1, self).__init__(*args, **kwargs)
        self.is_walking = True
        self.class_member = {}
        self.teach_member = {}
        self.used_course_category = set()
        self.course_map = {}
        self.space_map = {}
        self.classroom_map = {}

    def add_space_slot(self, num, week, location, category, course):
        coordinate = "{}-{}-{}-{}".format(num, week, location, category)
        if coordinate not in self.space_map:
            self.space_map[coordinate] = []
        self.space_map[coordinate].append(course)

    def combine_space(self):
        total_courses, appear_course = [], []
        for coordinate, courses in self.space_map.items():
            subject_map = {}
            for course in courses:
                if course.number in appear_course:
                    continue
                appear_course.append(course.number)
                if course.subject_number not in subject_map:
                    subject_map[course.subject_number] = course
                    total_courses.append(course)
                else:
                    unique_course = subject_map[course.subject_number]
                    new_name = "{},{}".format(course.class_name, unique_course.name)
                    if len(new_name) <= 31:
                        unique_course.name = new_name
                    for student in course.student_list:
                        unique_course.add_student(student)
        return total_courses

    def related_member(self):
        res = self.nice_requester.get_student_list()
        res_data = res.get('studentInfos', [])
        for rd in res_data:
            student_num, class_num = rd['studentEID'], rd['qualifiedClassID']
            if class_num not in self.class_member:
                self.class_member[class_num] = []
            self.class_member[class_num].append(student_num)
            for teach_num in rd['teachingClassFullIDs']:
                if teach_num not in self.teach_member:
                    self.teach_member[teach_num] = []
                self.teach_member[teach_num].append(student_num)
            elective_classes = rd.get('electiveClassFullIDs', []) or []
            for teach_num in elective_classes:
                if teach_num not in self.teach_member:
                    self.teach_member[teach_num] = []
                self.teach_member[teach_num].append(student_num)

    def analyse_schedule(self, schedule_info):
        num = schedule_info['timeslotInDay']
        begin_datetime = str2datetime("2019-12-12 {}:00".format(schedule_info['beginTime']))
        end_datetime = begin_datetime + datetime.timedelta(minutes=schedule_info['duration'])
        pre_datetime = begin_datetime - datetime.timedelta(minutes=10)
        schedule_data = {"num": num, "order": num, "start_time": time2str(begin_datetime),
                         "stop_time": time2str(end_datetime), "pre_time": time2str(pre_datetime)}
        return schedule_data

    def create_school_rest_table(self, rest_table, rest_table_info):
        morning_index = rest_table_info['earlyMorningLessons'] + rest_table_info['morningLessons']
        afternoon_index = morning_index + rest_table_info['afternoonLessons']
        for week in range(1, rest_table_info['daysPerWeek'] + 1):
            for schedule_info in rest_table_info["times"]:
                num = schedule_info['timeslotInDay']
                if num <= morning_index:
                    time_period = PeriodSet.MORNING
                elif num <= afternoon_index:
                    time_period = PeriodSet.AFTERNOON
                else:
                    time_period = PeriodSet.EVENING
                schedule_data = self.analyse_schedule(schedule_info)
                rest_schedule = RestSchedule(week=week, time_period=time_period, **schedule_data)
                rest_table.add_schedule(rest_schedule)

    def create_course(self, course_schedule, forbidden_category=set()):
        used_category = set()
        category_map = {0: 0, 1: 1, 2: 2}
        for course_info in course_schedule:
            category = category_map.get(course_info['oddDual'], 0)
            if category in forbidden_category:
                continue
            num, week = course_info['timeslot'], course_info['weekDay']
            classroom_number = self.classroom_map.get(course_info['locationID'], None)
            class_name, subject_name = course_info['classFullName'], course_info['subjectName']
            is_walking = course_info['classType'] in ["教学班", "选修班"]
            name = class_name if is_walking else class_name + subject_name
            number = "{}-{}".format(course_info['qualifiedClassID'], course_info['subjectID'])
            if number in self.course_map:
                course = self.course_map[number]
            else:
                try:
                    teacher_number = course_info["teachers"][0]["teacherEID"]
                except (Exception,):
                    teacher_number = None
                course_data = {'name': name, 'number': number, 'subject_number': course_info['subjectID'],
                               "subject_name": subject_name, "class_name": class_name,
                               'classroom_number': classroom_number, 'is_walking': is_walking,
                               "teacher_number": teacher_number}
                if is_walking:
                    course_data['student_list'] = self.teach_member.get(course_info['qualifiedClassID'], [])
                else:
                    course_data['class_name'] = course_info['qualifiedClassID']
                    course_data['student_list'] = self.class_member.get(course_info['qualifiedClassID'], [])
                course = CourseV1(**course_data)
                self.course_map[number] = course
                self.add_space_slot(num, week, category, classroom_number, course)
                # manager.add_course(course)
            course.add_position(num, week)
            used_category.add(category)
        return used_category

    def sync(self):
        res = self.nice_requester.get_table(current=False)
        rest_table = RestTable(name="全校作息", number=b64encode("全校作息")[:20])
        rest_table_info = res.get('timeSettings', [])
        if not res.get('schedule', None):
            return
        self.create_school_rest_table(rest_table, rest_table_info)
        self.related_member()
        semester_name = res['semester'] or "当前学期"
        course_table = CourseTableManagerV1(name=semester_name, number=b64encode(semester_name)[:20])
        course_table.is_walking = self.is_walking
        self.create_course(res['schedule'], self.used_course_category)
        total_courses = self.combine_space()
        course_table.courses = total_courses
        print(">>> CREATE_REST_TABLE")
        logger.info(">>> CREATE_REST_TABLE")
        self.client.create_rest_table(self.school_id, rest_table, is_active=True)
        print(">>> CREATE_COURSE_TABLE")
        logger.info(">>> CREATE_COURSE_TABLE")
        self.client.create_course_table(self.school_id, course_table, is_active=True)
