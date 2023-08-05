import datetime
import uuid
from sync import BaseSync2
from classcard_dataclient.models.course import CourseV2, CourseTableManagerV2, TableCategory, WalkingModeSet
from classcard_dataclient.models.schedule import RestScheduleV2, RestTableV2, PeriodSet
from classcard_dataclient.models.semester import SemesterV2
from utils.code import get_md5_hash
from utils.loggerutils import logging
from utils.dateutils import str2datetime, time2str, date2str

logger = logging.getLogger(__name__)


class CourseSyncV2(BaseSync2):
    def __init__(self, *args, **kwargs):
        super(CourseSyncV2, self).__init__(*args, **kwargs)
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
                rest_schedule = RestScheduleV2(week=week, time_period=time_period, **schedule_data)
                rest_table.add_schedule(rest_schedule)

    def create_course(self, course_schedule):
        used_classroom = set()
        category_map = {0: 0, 1: 1, 2: 2}
        for course_info in course_schedule:
            category = TableCategory.ALL
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
                               'classroom_number': classroom_number, 'is_walking': self.is_walking,
                               "teacher_number": teacher_number, "begin_week": 1, "end_week": 9}
                if is_walking:
                    course_data['student_list'] = self.teach_member.get(course_info['qualifiedClassID'], [])
                else:
                    course_data['class_name'] = course_info['qualifiedClassID']
                    course_data['student_list'] = self.class_member.get(course_info['qualifiedClassID'], [])
                course = CourseV2(**course_data)
                used_classroom.add(classroom_number)
                self.course_map[number] = course
                self.add_space_slot(num, week, category, classroom_number, course)
            course.add_position(num, week, category, classroom_number)
        return used_classroom

    def sync(self):
        response = self.nice_requester.get_table(current=False)
        begin_datetime = datetime.datetime.now()
        end_datetime = begin_datetime + datetime.timedelta(days=60)
        begin_date, end_date = date2str(begin_datetime.date()), date2str(end_datetime.date())
        semester_name = response['semester'] or "当前学期"
        semester = SemesterV2(name=semester_name, begin_date=begin_date, end_date=end_date,
                              number=get_md5_hash(semester_name)[:20])
        rest_table = RestTableV2(name="全校作息", number=get_md5_hash("全校作息")[:20], semester_name=semester.name)
        rest_table_info = response.get('timeSettings', [])
        if not response.get('schedule', None):
            return
        self.create_school_rest_table(rest_table, rest_table_info)
        self.related_member()
        course_table_name = "{}课表_{}".format(semester_name, str(uuid.uuid4())[:4])
        course_table_number = get_md5_hash(course_table_name)[:20]
        walking_mode = WalkingModeSet.WALKING if self.is_walking else WalkingModeSet.NOT_WALKING
        course_table = CourseTableManagerV2(name=course_table_name, number=course_table_number,
                                            rest_name=rest_table.name, walking_mode=walking_mode,
                                            is_walking=self.is_walking, semester_name=semester.name,
                                            begin_date=begin_date, end_date=end_date)
        for class_num in list(self.class_member.keys()):
            course_table.add_class(class_num)
        used_classroom = self.create_course(response['schedule'])
        course_table.classrooms_num = used_classroom
        total_courses = self.combine_space()
        course_table.courses = total_courses
        print(">>> CREATE_REST_TABLE")
        logger.info(">>> CREATE_REST_TABLE")
        self.client.create_semester(self.school_id, semester)
        self.client.create_rest_table(self.school_id, rest_table, is_active=True)
        print(">>> CREATE_COURSE_TABLE")
        logger.info(">>> CREATE_COURSE_TABLE")
        self.client.create_course_table(self.school_id, course_table, is_active=True)
        self.client.active_semester(self.school_id, semester, delete_other=True)
