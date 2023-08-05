# -*- coding: utf-8 -*-
"""
Created By Murray(m18527) on 2019/9/4 16:48
"""
from copy import deepcopy
from .backbone import Backbone, BackboneV1, BackboneV2
from ..models import Teacher, Student, Class, Classroom, Subject, CourseTableManager, RestTable, News, Notice, Album, \
    Video, Image, School, MeetingRoom, EduOrgUser
from ..models import CourseTableManagerV1
from ..models import RestTableV2, CourseTableManagerV2, SemesterV2
from ..utils.constants import ERROR_PARAMS, SUCCESS, MSG
from ..utils.core import config
from ..utils.data_req import *
from ..utils.loggerutils import logging

logger = logging.getLogger(__name__)


class DataClient(object):
    """Data client as data transfer be used for saving data to class card server"""

    def __init__(self, config_module=None):
        """
        init DataClient
        :param config_module: config module
        """
        if config_module:
            try:
                config.from_obj(config_module)
            except Exception as e:
                logger.error("Error: set config fail, Detail: {}".format(e))

    @staticmethod
    def set_config_module(module):
        try:
            config.from_obj(module)
        except Exception as e:
            logger.error("Error: set config fail, Detail: {}".format(e))

    @staticmethod
    def create_school(school, uk="name"):
        """
        创建学校
        :param school: School
        :param uk: school unique key,name or number
        :return:
        """
        if not isinstance(school, School):
            logger.error("TypeError: school must be a models.School instance.")
            return ERROR_PARAMS, "数据类型不正确。"
        code, ori_school = get_school_by_name(school.name) if uk == "name" else get_school_by_code(school.number)
        if ori_school:
            update_data = deepcopy(school.sso_data)
            update_data.pop('principal_email', None)
            update_school_req(ori_school.get('uuid'), update_data)
        else:
            create_school_req(school.sso_data)

    @staticmethod
    def create_teacher(teachers):
        """
        create teacher of edtech user server.
        :param teachers:  teacher list or instance
        :return: code, msg
        """
        is_multi, teacher_map = True, {}
        if not isinstance(teachers, Teacher) and not isinstance(teachers, list):
            logger.error("Error: No data or wrong teacher instance type.")
            return ERROR_PARAMS, "数据为空或格式不正确。"
        if isinstance(teachers, Teacher):
            teachers = [teachers]
            is_multi = False
        if teachers and is_multi:
            backbone = Backbone(teachers[0].school)
            backbone.wrap_teacher_map(origin="edtech")
            teacher_map = backbone.teacher_map

        code_list, msg_list = [], []
        for index, t in enumerate(teachers):
            if t.uid:
                code, rlt = update_teacher_req(t.uid, t.sso_data, school_id=t.school)
            elif t.number in teacher_map:
                code, rlt = update_teacher_req(teacher_map[t.number], t.sso_data, school_id=t.school)
            else:
                code, rlt = create_teacher_req(t.sso_data, school_id=t.school)
            if code:
                logger.error("Error, create teacher fail, Detail: {}, Data: {}".format(rlt, t.sso_data))
            code_list.append(code)
            msg_list.append(rlt)
            print(">>> Already create {}/{} teacher".format(index + 1, len(teachers)))

        if is_multi:
            return code_list, msg_list
        return code_list[0], msg_list[0]

    @staticmethod
    def get_teacher_number_map(school_id):
        backbone = Backbone(school_id)
        backbone.wrap_teacher_map()
        teacher_map = backbone.teacher_map
        return teacher_map

    @staticmethod
    def get_student_number_map(school_id):
        backbone = Backbone(school_id)
        backbone.wrap_student_map()
        student_map = backbone.student_map
        return student_map

    @staticmethod
    def create_student(students):
        """
        create student of edtech user server.
        :param students:  student list or instance
        :return: code, msg
        """
        is_multi, student_map = True, {}
        if not isinstance(students, Student) and not isinstance(students, list):
            logger.error("Error: No data or wrong student instance.")
            return ERROR_PARAMS, "数据为空或格式不正确。"
        if isinstance(students, Student):
            students = [students]
            is_multi = False
        if students and is_multi:
            backbone = Backbone(students[0].school)
            backbone.wrap_student_map(origin="edtech")
            student_map = backbone.student_map

        code_list, msg_list = [], []
        for index, s in enumerate(students):
            if s.uid:
                code, rlt = update_student_req(s.uid, s.sso_data, school_id=s.school)
            elif s.number in student_map:
                code, rlt = update_student_req(student_map[s.number], s.sso_data, school_id=s.school)
            else:
                code, rlt = create_student_req(s.sso_data, school_id=s.school)
            if code:
                logger.error("Error, create student fail, Detail: {}, Data: {}".format(rlt, s.sso_data))
            code_list.append(code)
            msg_list.append(rlt)
            print(">>> Already create {}/{} student".format(index + 1, len(students)))

        if is_multi:
            return code_list, msg_list
        return code_list[0], msg_list[0]

    @staticmethod
    def create_section(sections):
        """
        create section of edtech user server.
        :param sections:  section list or instance
        :return: code, msg
        """
        is_multi, class_map = True, {}
        if not isinstance(sections, Class) and not isinstance(sections, list):
            logger.error("Error: No data or wrong Class type.")
            return ERROR_PARAMS, "数据为空或格式不正确。"
        if isinstance(sections, Class):
            sections = [sections]
            is_multi = False
        if sections and is_multi:
            backbone = Backbone(sections[0].school)
            backbone.wrap_class_map(key="number", origin="edtech")
            class_map = backbone.class_map

        code_list, msg_list = [], []
        for index, d in enumerate(sections):
            if d.uid:
                code, rlt = update_section_req(d.uid, d.sso_data, school_id=d.school)
            elif d.number in class_map:
                code, rlt = update_section_req(class_map[d.number], d.sso_data, school_id=d.school)
            else:
                code, rlt = create_section_req(d.sso_data, school_id=d.school)
            if code:
                logger.error("Error, create section fail, Detail: {}, Data: {}".format(rlt, d.sso_data))
            code_list.append(code)
            msg_list.append(rlt)
            print(">>> Already create {}/{} section".format(index + 1, len(sections)))

        if is_multi:
            return code_list, msg_list
        return code_list[0], msg_list[0]

    @staticmethod
    def get_class_device_info(school_id, sn):
        """get class device info"""
        code, data = get_device_info(school_id=school_id, sn=sn)
        if code:
            logger.error("Error, query class device info, Detail: {}".format(data))
        return code, data

    @staticmethod
    def get_section_list(school_id):
        """get class device info"""
        code, data = get_section_by_school(school_id=school_id)
        if code:
            logger.error("Error, query section info, Detail: {}".format(data))
        return code, data

    @staticmethod
    def get_school_by_id(school_id):
        """get school info by school_id"""
        if not school_id:
            logger.error("Error: No query params.")
            return ERROR_PARAMS, MSG[ERROR_PARAMS]

        code, data = get_school_by_id(school_id=school_id)
        if code:
            logger.error("Error, query school info fail, Detail: {}".format(data))
        return code, data

    @staticmethod
    def get_school_by_name(name):
        """get school info by school name"""
        if not name:
            logger.error("Error: No query params.")
            return ERROR_PARAMS, MSG[ERROR_PARAMS]

        code, data = get_school_by_name(name)
        if code:
            logger.error("Error, query school info fail, Detail: {}".format(data))
        return code, data

    @staticmethod
    def get_school_by_number(number):
        """get school info by school number"""
        if not number:
            logger.error("Error: No query params.")
            return ERROR_PARAMS, MSG[ERROR_PARAMS]

        code, data = get_school_by_code(number)
        if code:
            logger.error("Error, query school info fail, Detail: {}".format(data))
        return code, data

    @staticmethod
    def create_classroom(classrooms):
        """
        create classroom of class card server.
        :param classrooms:  classroom list or instance
        :return: code, msg
        """
        is_multi = True
        if not isinstance(classrooms, Classroom) and not isinstance(classrooms, list):
            logger.error("Error: No data or wrong classroom type.")
            return ERROR_PARAMS, "数据为空或格式不正确。"
        if isinstance(classrooms, Classroom):
            classrooms = [classrooms]
            is_multi = False

        code_list, msg_list = [], []
        for d in classrooms:
            code, rlt = create_classroom_req(d.nirvana_data, school_id=d.school)
            if code:
                logger.error("Error, create classroom fail, Detail: {}, Data: {}".format(rlt, d))
            code_list.append(code)
            msg_list.append(rlt if code else MSG[SUCCESS])

        if is_multi:
            return code_list, msg_list
        return code_list[0], msg_list[0]

    @staticmethod
    def create_subject(subjects):
        """
        create subject of class card server.
        :param subjects:  subject list or instance
        :return: code, msg
        """
        is_multi = True
        if not isinstance(subjects, Subject) and not isinstance(subjects, list):
            logger.error("Error: No data or wrong subject type.")
            return ERROR_PARAMS, "数据为空或格式不正确。"
        if isinstance(subjects, Subject):
            subjects = [subjects]
            is_multi = False

        code_list, msg_list = [], []
        for d in subjects:
            code, rlt = create_subject_req(d.nirvana_data, school_id=d.school)
            if code:
                logger.error("Error, create subject fail, Detail: {}, Data: {}".format(rlt, d))
            code_list.append(code)
            msg_list.append(rlt if code else MSG[SUCCESS])

        if is_multi:
            return code_list, msg_list
        return code_list[0], msg_list[0]

    @staticmethod
    def create_course_table(school_id, course_table_manager, is_active=True, create_manager=True):
        """
        创建课程表
        :param school_id: school_id
        :param course_table_manager: Type -> models.CourseTableManager
        :param is_active: active course table right now after create it
        :param create_manager: create course table manager or not
        :return:
        """
        if not isinstance(course_table_manager, CourseTableManager):
            logger.error("TypeError: course_table_manager must be a models.CourseTableManager instance.")
            return ERROR_PARAMS, "数据类型不正确。"
        course_table_manager.validate()
        backbone = Backbone(school_id)
        backbone.upload_course_table(course_manager=course_table_manager, is_active=is_active,
                                     create_manager=create_manager)
        return True

    @staticmethod
    def active_course_table(school_id, course_table_manager, delete_other=True):
        """
        创建课程表
        :param school_id: school_id
        :param course_table_manager: Type -> models.CourseTableManager
        :param delete_other: delete other course table right now after active it
        :return:
        """
        if not isinstance(course_table_manager, CourseTableManager):
            logger.error("TypeError: course_table_manager must be a models.CourseTableManager instance.")
            return ERROR_PARAMS, "数据类型不正确。"
        backbone = Backbone(school_id)
        backbone.active_course_table(course_manager=course_table_manager, delete_other=delete_other)
        return True

    @staticmethod
    def create_rest_table(school_id, rest_table, is_active=False):
        """
        创建作息表
        :param school_id: school_id
        :param rest_table: Type -> models.RestTable
        :param is_active: active rest table right now after create it
        :return:
        """
        if not isinstance(rest_table, RestTable):
            logger.error("TypeError: rest_table must be a models.RestTable instance.")
            return ERROR_PARAMS, "数据类型不正确。"
        rest_table.validate()
        backbone = Backbone(school_id)
        backbone.upload_rest_table(rest_table=rest_table, is_active=is_active)
        return True

    @staticmethod
    def create_subjects(school_id, subjects, new_name=False):
        """
        同步科目
        :param school_id: school_id
        :param subjects: Type -> [models.Subject, models.Subject]
        :param new_name: new_name
        :return:
        """
        for sub in subjects:
            if not isinstance(sub, Subject):
                logger.error("TypeError: subject must be a models.Subject instance.")
                return ERROR_PARAMS, "数据类型不正确。"
            sub.validate()
        backbone = Backbone(school_id)
        backbone.upload_subjects(subjects, new_name=new_name)
        return True

    @staticmethod
    def create_classrooms(school_id, classrooms):
        """
        同步教室
        :param school_id: school_id
        :param classrooms: Type -> [models.Classroom, models.Classroom]
        :return:
        """
        for room in classrooms:
            if not isinstance(room, Classroom):
                logger.error("TypeError: classroom must be a models.Classroom instance.")
                return ERROR_PARAMS, "数据类型不正确。"
            room.validate()
        backbone = Backbone(school_id)
        backbone.upload_classrooms(classrooms)
        return True

    @staticmethod
    def create_meeting_rooms(school_id, meeting_rooms):
        """
        同步会议室
        :param school_id: school_id
        :param meeting_rooms: Type -> [models.MeetingRoom, models.MeetingRoom]
        :return:
        """
        for room in meeting_rooms:
            if not isinstance(room, MeetingRoom):
                logger.error("TypeError: meeting_room must be a models.MeetingRoom instance.")
                return ERROR_PARAMS, "数据类型不正确。"
            room.validate()
        backbone = Backbone(school_id)
        backbone.upload_meeting_rooms(meeting_rooms)
        return True

    @staticmethod
    def create_news(school_id, news):
        """
        同步新闻
        :param school_id: school_id
        :param news: News
        :return:
        """
        if not isinstance(news, News):
            logger.error("TypeError: news must be a models.News instance.")
            return ERROR_PARAMS, "数据类型不正确。"
        news.validate()
        backbone = Backbone(school_id)
        backbone.upload_news(news)
        return True

    @staticmethod
    def create_notice(school_id, notice):
        """
        同步通知
        :param school_id: school_id
        :param notice: Notice
        :return:
        """
        if not isinstance(notice, Notice):
            logger.error("TypeError: notice must be a models.Notice instance.")
            return ERROR_PARAMS, "数据类型不正确。"
        notice.validate()
        backbone = Backbone(school_id)
        backbone.upload_notice(notice)
        return True

    @staticmethod
    def create_video(school_id, video):
        """
        同步通知
        :param school_id: school_id
        :param video: Video
        :return:
        """
        if not isinstance(video, Video):
            logger.error("TypeError: video must be a models.Video instance.")
            return ERROR_PARAMS, "数据类型不正确。"
        video.validate()
        backbone = Backbone(school_id)
        backbone.upload_video(video)
        return True

    @staticmethod
    def create_album(school_id, album):
        """
        同步通知
        :param school_id: school_id
        :param album: Album
        :return:
        """
        if not isinstance(album, Album):
            logger.error("TypeError: album must be a models.Album instance.")
            return ERROR_PARAMS, "数据类型不正确。"
        album.validate()
        backbone = Backbone(school_id)
        backbone.upload_album(album)
        return True

    @staticmethod
    def create_image(school_id, images):
        """
        同步通知
        :param school_id: school_id
        :param images: [Image, Image]
        :return:
        """
        for img in images:
            if not isinstance(img, Image):
                logger.error("TypeError: img must be a models.Image instance.")
                return ERROR_PARAMS, "数据类型不正确。"
            img.validate()
        backbone = Backbone(school_id)
        backbone.upload_image(images)
        return True

    @staticmethod
    def get_active_schedule(school_id):
        """
        获取已激活的作息
        :param school_id:
        :return:
        """
        backbone = Backbone(school_id)
        schedule = backbone.get_active_schedule()
        return schedule

    @staticmethod
    def get_active_table(school_id):
        """
        获取已激活的课程表
        :param school_id:
        :return:
        """
        backbone = Backbone(school_id)
        table = backbone.get_active_table()
        return table

    @staticmethod
    def get_future_exam_classroom(school_id):
        """
        获取已激活的作息
        :param school_id:
        :return:
        """
        backbone = Backbone(school_id)
        room = backbone.get_future_exam_classroom()
        return room

    @staticmethod
    def get_classroom_num_map(school_id):
        """
        获取教室编号映射表
        :param school_id:
        :return:
        """
        backbone = Backbone(school_id)
        backbone.wrap_classroom_map()
        return deepcopy(backbone.classroom_map)

    @staticmethod
    def delete_classroom(school_id, uid):
        backbone = Backbone(school_id)
        backbone.delete_classroom(uid)
        return

    @staticmethod
    def get_subject_num_map(school_id):
        """
        获取科目编号映射表
        :param school_id:
        :return:
        """
        backbone = Backbone(school_id)
        backbone.wrap_subject_map()
        return deepcopy(backbone.subject_map)

    @staticmethod
    def delete_subject(school_id, uid):
        backbone = Backbone(school_id)
        backbone.delete_subject(uid)
        return

    @staticmethod
    def upload_user_avatar(school_id, file_path, user_id):
        backbone = Backbone(school_id)
        return backbone.upload_user_avatar(file_path, user_id)

    @staticmethod
    def upload_user_face(school_id, file_path, student_id=None, teacher_id=None):
        if not (student_id and teacher_id):
            return None
        data = {"student_id": student_id} if student_id else {"teacher_id": teacher_id}
        backbone = Backbone(school_id)
        return backbone.upload_user_face(file_path, data)


class DataClientV1(DataClient):
    @staticmethod
    def create_course_table(school_id, course_table_manager, is_active=True, create_manager=True):
        """
        创建课程表
        :param school_id: school_id
        :param course_table_manager: Type -> models.CourseTableManagerV1
        :param is_active: active course table right now after create it
        :param create_manager: create course table manager or not
        :return:
        """
        if not isinstance(course_table_manager, CourseTableManagerV1):
            logger.error("TypeError: course_table_manager must be a models.CourseTableManager instance.")
            return ERROR_PARAMS, "数据类型不正确。"
        course_table_manager.validate()
        backbone = BackboneV1(school_id)
        backbone.upload_course_table(course_manager=course_table_manager, is_active=is_active,
                                     create_manager=create_manager)
        return True


class DataClientV2(DataClient):

    @staticmethod
    def create_semester(school_id, semester):
        """
        创建作息表
        :param school_id: school_id
        :param semester: Type -> models.SemesterV2
        :return:
        """
        if not isinstance(semester, SemesterV2):
            logger.error("TypeError: rest_table must be a models.RestTable instance.")
            return ERROR_PARAMS, "数据类型不正确。"
        semester.validate()
        backbone = BackboneV2(school_id)
        backbone.upload_semester(semester=semester)
        return True

    @staticmethod
    def create_rest_table(school_id, rest_table, is_active=False):
        """
        创建作息表
        :param school_id: school_id
        :param rest_table: Type -> models.RestTableV2
        :param is_active: active rest table right now after create it
        :return:
        """
        if not isinstance(rest_table, RestTableV2):
            logger.error("TypeError: rest_table must be a models.RestTable instance.")
            return ERROR_PARAMS, "数据类型不正确。"
        rest_table.validate()
        backbone = BackboneV2(school_id)
        backbone.upload_rest_table(rest_table=rest_table, is_active=is_active)
        return True

    @staticmethod
    def create_course_table(school_id, course_table_manager, is_active=True, create_manager=True):
        if not isinstance(course_table_manager, CourseTableManagerV2):
            logger.error("TypeError: course_table_manager must be models.CourseTableManagerV2 instance.")
            return ERROR_PARAMS, "数据类型不正确。"
        course_table_manager.validate()
        backbone = BackboneV2(school_id)
        backbone.upload_course_table(course_manager=course_table_manager, is_active=is_active,
                                     create_manager=create_manager)
        return True

    @staticmethod
    def active_semester(school_id, semester, delete_other=True):
        """
        激活学期
        :param school_id:
        :param semester:
        :param delete_other:
        :return:
        """
        if not isinstance(semester, SemesterV2):
            logger.error("TypeError: rest_table must be a models.RestTable instance.")
            return ERROR_PARAMS, "数据类型不正确。"
        semester.validate()
        backbone = BackboneV2(school_id)
        backbone.active_semester(semester=semester, delete_other=delete_other)
        return True

    @staticmethod
    def active_course_table(school_id, course_table_manager, delete_other=True):
        if not isinstance(course_table_manager, CourseTableManagerV2):
            logger.error("TypeError: course_table_manager must be a models.CourseTableManagerV2 instance.")
            return ERROR_PARAMS, "数据类型不正确。"
        backbone = BackboneV2(school_id)
        backbone.active_course_table(course_manager=course_table_manager, delete_other=delete_other)
        return True

    @staticmethod
    def delete_all_course_table(school_id, semester_name):
        backbone = BackboneV2(school_id)
        backbone.delete_all_table_manager(semester_name)
        return True


class DataClientV3(DataClient):
    @staticmethod
    def get_teacher_info(params, school_id):
        """
        :param params: {"number":"xx", "name":"xx"}
        :param school_id:
        :return:
        """
        code, data = get_teacher_req(params, school_id)
        if code:
            logger.error("Error, query teacher info, Detail: {}".format(data))
        return data

    def delete_teacher(self, params, school_id):
        data = self.get_teacher_info(params, school_id)
        if len(data) > 1:
            return ERROR_PARAMS, "查询老师信息不唯一"
        elif len(data) == 1:
            teacher_id = data[0]['uuid']
            code, data = delete_teacher_req(teacher_id, school_id)
            return code, data
        else:
            return ERROR_PARAMS, "未查询到老师信息"

    @staticmethod
    def get_student_info(params, school_id):
        """
        :param params: {"number":"xx", "name":"xx", "description":"xx", "section_id":"xx"}
        :param school_id:
        :return:
        """
        code, data = get_student_req(params, school_id)
        if code:
            logger.error("Error, query student info, Detail: {}".format(data))
        return data

    def delete_student(self, params, school_id):
        data = self.get_student_info(params, school_id)
        if len(data) > 1:
            return ERROR_PARAMS, "查询学生信息不唯一"
        elif len(data) == 1:
            student_id = data[0]['uuid']
            code, data = delete_student_req(student_id, school_id)
            return code, data
        else:
            return ERROR_PARAMS, "未查询到学生信息"

    def delete_school(self, name):
        code, data = self.get_school_by_name(name)
        if code:
            logger.error("Error, query school info, Detail: {}".format(data))
            return ERROR_PARAMS, data
        else:
            school_id = data["uuid"]
            code, data = delete_school_req(school_id)
            return code, data

    @staticmethod
    def get_section_info(params, school_id):
        """
        :param params: {"num":"xx", "name":"xx", "grade":"xx"}
        :param school_id:
        :return:
        """
        code, data = get_section_req(params, school_id)
        if code:
            logger.error("Error, query section info, Detail: {}".format(data))
        return data

    def delete_section(self, params, school_id):
        section = self.get_section_info(params, school_id)
        count = section.get("count")
        if count > 1:
            return ERROR_PARAMS, "查询班级信息不唯一"
        elif count == 1:
            section_id = section["results"][0]["uid"]
            code, data = delete_section_req(section_id=section_id, school_id=school_id)
            return code, data
        else:
            return ERROR_PARAMS, "未查询到班级信息"

    @staticmethod
    def create_edu_org_user(edu_org_users):
        """
        create edu_org_user of edtech user server.
        :param edu_org_users:  edu_org_user list or instance
        :return: code, msg
        """
        is_multi, edu_org_user_map = True, {}
        if not isinstance(edu_org_users, EduOrgUser) and not isinstance(edu_org_users, list):
            logger.error("Error: No data or wrong student instance.")
            return ERROR_PARAMS, "数据为空或格式不正确。"
        if isinstance(edu_org_users, EduOrgUser):
            edu_org_users = [edu_org_users]
            is_multi = False
        if edu_org_users and is_multi:
            backbone = Backbone(school_id=None)
            backbone.wrap_edu_org_user_map()
            edu_org_user_map = backbone.edu_org_user_map

        code_list, msg_list = [], []
        for index, s in enumerate(edu_org_users):
            if s.uid:
                code, rlt = update_edu_org_user_req(s.uid, s.sso_data)
            elif s.number in edu_org_user_map:
                code, rlt = update_edu_org_user_req(edu_org_user_map[s.number], s.sso_data)
            else:
                code, rlt = create_edu_org_user_req(s.sso_data)
            if code:
                logger.error("Error, create edu org user fail, Detail: {}, Data: {}".format(rlt, s.sso_data))
            code_list.append(code)
            msg_list.append(rlt)
            print(">>> Already create {}/{} edu org user".format(index + 1, len(edu_org_users)))

        if is_multi:
            return code_list, msg_list
        return code_list[0], msg_list[0]

    @staticmethod
    def get_edu_org_user_info(params):
        """
        :param params: {"number":"xx", "name":"xx", "outer_id": ""}
        :return:
        """
        code, data = get_edu_org_user_req(params)
        if code:
            logger.error("Error, query org_user info, Detail: {}".format(data))
        return data

    def delete_edu_org_user(self, params):
        data = self.get_edu_org_user_info(params)
        if len(data) > 1:
            return ERROR_PARAMS, "查询行政管理人员信息不唯一"
        elif len(data) == 1:
            edu_user_id = data[0]['uuid']
            code, data = delete_edu_org_user_req(edu_user_id)
            return code, data
        else:
            return ERROR_PARAMS, "未查询到行政管理人员信息"
