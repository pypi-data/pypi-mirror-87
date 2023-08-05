import os
import uuid
import requests
from ..requester.nirvana import NirvanaRequester
from ..requester.edtech import EDTechRequester
from ..models.news import TypeSet
from ..settings import CLASS_CARD_SERVER_URL, EDTECH_SERVER_URL, DATA_ROOT
from ..utils.exceptions import RequestError


class Backbone(object):
    def __init__(self, school_id):
        self.course_manager = None  # CourseManager Model
        self.rest_table = None  # RestTable Model
        self.courses = {}  # num -> Course Model
        self.subjects = {}  # num -> Subject Model
        self.classrooms = {}  # num -> Classroom Model
        self.sections = {}  # num -> Section Model
        self.teachers = {}  # number -> Teacher Model
        self.students = {}  # number -> Student Model
        self.course_map = {}  # num -> uid
        self.subject_map = {}  # num -> uid
        self.classroom_map = {}  # num -> uid
        self.teacher_map = {}  # number -> uid
        self.edu_org_user = {} # number -> uid
        self.student_map = {}  # number -> uid
        self.class_map = {}  # name -> uid
        self.album_map = {}  # name-category -> uid
        self.nirvana_requester = NirvanaRequester(server=CLASS_CARD_SERVER_URL, school_id=school_id)
        self.edtech_requester = EDTechRequester(server=EDTECH_SERVER_URL, school_id=school_id)

    def download_file(self, url, name=None):
        if not os.path.exists(DATA_ROOT):
            os.makedirs(DATA_ROOT)
        ext = '.' + url.split('.')[-1]
        file_name = name or str(uuid.uuid4())
        file_path = os.path.join(DATA_ROOT, file_name) + ext
        r = requests.get(url)
        with open(file_path, "wb") as f:
            f.write(r.content)
        f.close()
        return file_path

    def get_teacher_list(self, **params):
        res = self.nirvana_requester.get_teacher_list(params)
        teachers = res.get('results', []) if isinstance(res, dict) else res
        return teachers or []

    def get_student_list(self, **params):
        res = self.nirvana_requester.get_student_list(params)
        students = res.get('results', []) if isinstance(res, dict) else res
        return students or []

    def wrap_course_map(self):
        """
        拉取班牌后台课程(教学班)列表，映射出课程uid
        :return:
        """
        self.course_map = self.nirvana_requester.wrap_map("get_course_list", ["num"], "uid", limit=0)

    def wrap_subject_map(self):
        """
        拉取班牌后台科目列表，映射出科目uid
        :return:
        """
        self.subject_map = self.nirvana_requester.wrap_map("get_subject_list", ["num"], "uid")

    def wrap_classroom_map(self):
        """
        拉取班牌后台教室列表，映射出教室uid
        :return:
        """
        self.classroom_map = self.nirvana_requester.wrap_map("get_classroom_list", ["num"], "uid")

    def wrap_class_map(self, key="name", origin="nirvana"):
        """
        拉取班牌后台行政班列表，映射出行政班uid
        :return:
        """
        if origin == "edtech":
            self.class_map = self.edtech_requester.wrap_map("get_class_list", ["number"], "uuid")
        else:
            self.class_map = self.nirvana_requester.wrap_map("get_class_list", [key], "uid")

    def wrap_teacher_map(self, origin="nirvana"):
        """
        拉取班牌后台教师列表，映射出教师uid
        :return:
        """
        if origin == "edtech":
            self.teacher_map = self.edtech_requester.wrap_map("get_teacher_list", ["number"], "uuid")
        else:
            self.teacher_map = self.nirvana_requester.wrap_map("get_teacher_list", ["number"], "uid")

    def wrap_student_map(self, origin="nirvana"):
        """
        拉取班牌后台学生列表，映射出学生uid
        :return:
        """
        if origin == "edtech":
            self.student_map = self.edtech_requester.wrap_map("get_student_list", ["number"], "uuid")
        else:
            self.student_map = self.nirvana_requester.wrap_map("get_student_list", ["number"], "uid")

    def wrap_album_map(self):
        """
        拉取班牌后台相册列表，映射出相册uid
        :return:
        """
        self.album_map = self.nirvana_requester.wrap_map("get_album_list", ["name", "category"], "uid")

    def delete_classroom(self, classroom_id):
        """
        删除教室
        :param classroom_id: 教室id
        :return:
        """
        print(">>> Delete classroom")
        self.nirvana_requester.delete_classroom(classroom_id)

    def delete_table_manager(self, manager_id):
        """
        删除整张课程表
        :param manager_id: 课程表id
        :return:
        """
        print(">>> Delete course table")
        self.nirvana_requester.delete_table_manager(manager_id)

    def get_course_manager_list(self, key=None, value=None):
        """
        获取旧的相同课程表id
        :param key:  判定相同课程表的唯一标识字段
        :param value: 唯一标识字段值
        :return:
        """
        print(">>> Get table by {}".format(key))
        if key and value is None:
            value = getattr(self.course_manager, key)
        param = {key: value} if key else {}
        res = self.nirvana_requester.get_table_manager(param)
        data = res.get('results', [])
        return data

    def get_rest_table_list(self, key=None, value=None):
        """
        获取旧的相同作息id
        :param key:  判定相同作息的唯一标识字段
        :param value: 唯一标识字段值
        :return:
        """
        print(">>> Get rest table by {}".format(key))
        if key and value is None:
            value = getattr(self.rest_table, key)
        param = {key: value} if key else {}
        res = self.nirvana_requester.get_rest_table(param)
        data = res.get('results', [])
        return data

    def create_course_manager(self, is_active=True):
        """
        创建课程表
        :param is_active: 创建完是否立即激活
        :return:
        """
        print(">>> Create Course Table Manager")
        # delete old manager
        old_manager = self.get_course_manager_list(key='number')
        if old_manager:
            old_manager_id = old_manager[0]['uid']
            self.delete_table_manager(old_manager_id)

        # create new manager
        manager_data = self.course_manager.nirvana_data
        manager = self.nirvana_requester.create_table_manager(manager_data)
        self.course_manager.uid = manager["uid"]
        manager_mode = {"course_manager_id": self.course_manager.uid, "is_walking": self.course_manager.is_walking}
        self.nirvana_requester.set_manager_mode(manager_mode)

        # active new manager
        if is_active:
            self.nirvana_requester.active_table_manager(self.course_manager.uid)

    def active_table_manager(self):
        managers = self.get_course_manager_list(key='number')
        if managers:
            manager_id = managers[0]['uid']
            self.nirvana_requester.active_table_manager(manager_id)

    def delete_other_table_manager(self, *args, **kwargs):
        managers = self.get_course_manager_list()
        for manager in managers:
            if manager['number'] != self.course_manager.number:
                self.delete_table_manager(manager['uid'])

    def create_courses(self):
        """
        创建课程(教学班)，需要通过course_manager
        该创建不包含课程表的课位
        :return:
        """
        print(">>> Batch Create Course")
        batch_data = {"manager": self.course_manager.uid, "item": []}
        index, total = 0, len(self.course_manager.courses)
        for course in self.course_manager.courses:
            if course.required_student and not course.student_ids:
                continue
            course.is_walking = self.course_manager.is_walking
            batch_data["item"].append(course.nirvana_data)
            if len(batch_data["item"]) >= 50:
                index += len(batch_data["item"])
                self.nirvana_requester.batch_create_course(batch_data)
                batch_data["item"] = []
                print(">>> Already create {} courses, total {}".format(index, total))
        if batch_data["item"]:
            self.nirvana_requester.batch_create_course(batch_data)
            print(">>> Already create {} courses, total {}".format(index + len(batch_data["item"]), total))

    def create_table(self):
        """
        创建课程表上的课位
        :return:
        """
        print(">>>Create Course Table")
        index, total = 0, len(self.course_manager.courses)
        for course in self.course_manager.courses:
            index += 1
            for position in course.schedule:
                course_id = self.course_map.get(str(course.number), None)
                if course_id:
                    table_data = {"course": {"uid": self.course_map[str(course.number)]},
                                  "manager": {"uid": self.course_manager.uid},
                                  "num": position[0], "week": position[1],
                                  "category": position[2]}
                    self.nirvana_requester.set_course_position(table_data)
            print("##### already create {}/{} course position ####".format(index, total))

    def create_subjects(self, subjects, new_name=False):
        """
        同步科目信息
        :return:
        """
        print(">>>Create Subject")
        index = 0
        for subject in subjects:
            index += 1
            subject_id = self.subject_map.get(str(subject.number), None)
            if subject_id:
                res_data = self.nirvana_requester.update_subject(subject_id, subject.nirvana_data)
                subject.uid = subject_id
            else:
                print(">>>Create Subject {}/{}".format(subject.number, subject.name))
                res_data = self.nirvana_requester.create_subject(subject.nirvana_data)
                if not res_data and new_name:
                    while True:
                        subject.name = "{}.".format(subject.name)
                        res_data = self.nirvana_requester.create_subject(subject.nirvana_data)
                        if res_data:
                            break
                subject.uid = res_data['uid']
            print("##### already create {} {}/{} subject ####".format(subject.name, index, len(subjects)))

    def delete_subject(self, subject_id):
        """
        删除科目
        :param subject_id: 科目id
        :return:
        """
        print(">>> Delete subject")
        self.nirvana_requester.delete_subject(subject_id)

    def create_news(self, news):
        """
        同步新闻信息
        :param news:
        :return:
        """
        print(">>>Create News")
        news.class_id = self.class_map.get(news.class_name, None)
        if news.category == TypeSet.CLASSROOM_TYPE:
            for classroom_number in news.classroom_numbers:
                if classroom_number not in self.classroom_map:
                    raise KeyError("classroom_number should be correct!")
                news.classroom_ids.append(self.classroom_map.get(classroom_number))
        res_data = self.nirvana_requester.create_news(news.nirvana_data)
        news.uid = res_data['uid']
        if news.category == TypeSet.CLASSROOM_TYPE:
            self.nirvana_requester.modify_classroom_news({"news": news.uid, "ids": [news.classroom_ids]})

    def create_notice(self, notice):
        """
        同步通知信息
        :param notice: Notice
        :return:
        """
        print(">>>Create Notice")
        notice.class_id = self.class_map.get(notice.class_name, None)
        if notice.category == TypeSet.CLASSROOM_TYPE:
            for classroom_number in notice.classroom_numbers:
                if classroom_number not in self.classroom_map:
                    raise KeyError("classroom_number should be correct!")
                notice.classroom_ids.append(self.classroom_map.get(classroom_number))
        res_data = self.nirvana_requester.create_board(notice.nirvana_data)
        notice.uid = res_data['uid']
        if notice.category == TypeSet.CLASSROOM_TYPE:
            self.nirvana_requester.modify_classroom_broad({"broad": notice.uid, "ids": [notice.classroom_ids]})

    def create_video(self, video):
        """
        同步视频信息
        :param video: Video
        :return:
        """
        print(">>>Create Video")
        video.class_id = self.class_map.get(video.class_name, None)
        if video.need_down:
            video_path = self.download_file(video.path)
            res_data = self.nirvana_requester.upload_file(video_path)
            video.path = res_data['path']
            os.remove(video_path)
        if video.category == TypeSet.CLASSROOM_TYPE:
            for classroom_number in video.classroom_numbers:
                if classroom_number not in self.classroom_map:
                    raise KeyError("classroom_number should be correct!")
                video.classroom_ids.append(self.classroom_map.get(classroom_number))
        res_data = self.nirvana_requester.create_video(video.nirvana_data)
        video.uid = res_data['uid']
        if video.category == TypeSet.CLASSROOM_TYPE:
            self.nirvana_requester.modify_classroom_video({"video": video.uid, "ids": [video.classroom_ids]})

    def create_album(self, album):
        """
        同步相册信息
        :param album: Album
        :return:
        """
        print(">>>Create Album")
        key = "{}-{}".format(album.name, album.category)
        album_id = self.album_map.get(key, None)
        album.class_id = self.class_map.get(album.class_name, None)
        if album.category == TypeSet.CLASSROOM_TYPE:
            if not album.all_classroom:
                for classroom_number in album.classroom_numbers:
                    if classroom_number not in self.classroom_map:
                        raise KeyError("classroom_number should be correct!")
                    album.classroom_ids.append(self.classroom_map.get(classroom_number))
            else:
                album.classroom_ids = list(self.classroom_map.values())
        if album_id:
            res_data = self.nirvana_requester.update_album(album_id, album.nirvana_data)
        else:
            res_data = self.nirvana_requester.create_album(album.nirvana_data)
        album.uid = res_data['uid']
        if album.category == TypeSet.CLASSROOM_TYPE:
            self.nirvana_requester.modify_classroom_album({"album": album.uid, "ids": album.classroom_ids})

    def create_image(self, images, album_id):
        """
        同步图片信息
        :param images: [Image, Image]
        :param album_id:
        :return:
        """
        for image in images:
            image.album_id = album_id
            if image.need_down:
                img_path = self.download_file(image.path)
                res_data = self.nirvana_requester.upload_file(img_path)
                image.path = res_data['path']
                os.remove(img_path)
        data = [img.nirvana_data for img in images]
        self.nirvana_requester.create_image(data)

    def arrange_images(self, images):
        """
        整理图片信息，把同一个相册的放在一起
        :param images: [Image, Image]
        :return:
        """
        img_set = {}
        for img in images:
            key = "{}-{}".format(img.album_name, img.album_category)
            album_id = self.album_map[key]
            if album_id not in img_set:
                img_set[album_id] = []
            img_set[album_id].append(img)
        return img_set

    def create_classrooms(self, classrooms):
        """
        同步教室信息
        :return:
        """
        print(">>>Create Classroom")
        index = 0
        for classroom in classrooms:
            index += 1
            classroom.section_id = self.class_map.get(classroom.section_name, None)
            classroom_id = self.classroom_map.get(str(classroom.number), None)
            if classroom_id:
                res_data = self.nirvana_requester.update_classroom(classroom_id, classroom.nirvana_data)
                classroom.uid = classroom_id
            else:
                res_data = self.nirvana_requester.create_classroom(classroom.nirvana_data)
                if not res_data:
                    print("创建教室{}失败".format(classroom.nirvana_data))
                classroom.uid = res_data['uid']
            print("##### already create {} {}/{} classroom ####".format(classroom.name, index, len(classrooms)))

    def clear_meeting_rooms(self):
        """
        清除未开始的会议室
        :return:
        """
        future_meeting_rooms = self.nirvana_requester.get_meeting_room_list(params={"state": 3})
        if future_meeting_rooms:
            for f_room in future_meeting_rooms.get("results", []):
                self.nirvana_requester.delete_meeting_room(f_room["uid"])

    def create_meeting_rooms(self, meeting_rooms):
        """
        同步会议室信息
        :return:
        """
        print(">>>Create MeetingRoom")
        index = 0
        for m_room in meeting_rooms:
            index += 1
            m_room.classroom_id = self.classroom_map.get(str(m_room.classroom_number))
            for user_number in m_room.user_numbers:
                user_id = self.teacher_map.get(user_number) or self.student_map.get(user_number)
                if user_id:
                    m_room.user.append(user_id)
            res_data = self.nirvana_requester.create_meeting_room(m_room.nirvana_data)
            m_room.uid = res_data['uid']
            role_data = m_room.nirvana_rule_data
            if role_data:
                self.nirvana_requester.create_meeting_room_rule(role_data)
            user_data = m_room.get_user_data()
            bind_user_data = {"meeting": res_data['uid'], "user": user_data["new_user"]}
            self.nirvana_requester.bind_meeting_room_user(bind_user_data)
            print("##### already create {} {}/{} meeting_rooms ####".format(m_room.name, index, len(meeting_rooms)))

    def relate_course_field(self):
        """
        将模型Course中的字段通过映射，转换为uid。(班牌后台接口结构)
        :return:
        """
        for course in self.course_manager.courses:
            course.subject_id = self.subject_map.get(str(course.subject_number), None)
            if not course.subject_id:
                print(">>>ERROR: subject_number{}错误，无法找到对应的科目".format(course.subject_number))
            course.classroom_id = self.classroom_map.get(str(course.classroom_number), None)
            course.teacher_id = self.teacher_map.get(course.teacher_number, None)
            course.class_id = self.class_map.get(course.class_name, None)
            for student_number in course.student_list:
                student_id = self.student_map.get(student_number, None)
                if not student_id:
                    print(">>>ERROR: student_number{}错误，无法找到对应的学生".format(student_number))
                course.student_ids.append(student_id)

    def get_old_rest_table(self, key='number', value=None):
        """
        获取旧的相同作息表id
        :param key:  判定相同作息表的唯一标识字段
        :param value: 唯一标识字段值
        :return:
        """
        print(">>> Get table by {}".format(key))
        if value is None:
            value = getattr(self.rest_table, key)
        param = {key: value}
        res = self.nirvana_requester.get_rest_table(param)
        data = res.get('results', None)
        rest_table_id = data[0]['uid'] if data else None
        return rest_table_id

    def create_rest_table(self, is_active=False):
        """
        创建作息表
        :param is_active: 创建好作息表后是否立即激活，不建议立即激活
        :return:
        """
        # delete old rest table
        old_rest_table_id = self.get_old_rest_table()
        if old_rest_table_id:
            self.delete_rest_table(old_rest_table_id)

        upload_data = self.rest_table.nirvana_data
        res_data = self.nirvana_requester.create_rest_table(upload_data)
        self.rest_table.uid = res_data['uid']

        if is_active:
            self.nirvana_requester.active_rest_table(res_data['uid'])

    def delete_rest_table(self, rest_table_id):
        """
        删除作息表
        :param rest_table_id:
        :return:
        """
        print(">>> Delete rest table")
        self.nirvana_requester.delete_rest_table(rest_table_id)

    def upload_rest_table(self, rest_table=None, is_active=False):
        """
        用于client调用，创建作息表
        :param rest_table: instance of RestTable for create
        :param is_active: 创建好作息表后是否立即激活，不建议立即激活
        :return:
        """
        self.rest_table = rest_table or self.rest_table
        self.create_rest_table(is_active)

    def upload_course_table(self, course_manager=None, is_active=False, create_manager=True):
        """
        用于client调用，创建课程表
        :param course_manager: instance of CourseTableManager for create
        :param is_active: 创建好课程表后是否立即激活，不建议立即激活
        :param create_manager: create course table manager or not
        :return:
        """
        self.course_manager = course_manager or self.course_manager
        self.wrap_subject_map()
        self.wrap_classroom_map()
        self.wrap_teacher_map()
        self.wrap_class_map()
        self.wrap_student_map()
        self.relate_course_field()
        if create_manager:
            self.create_course_manager(is_active)
        self.create_courses()
        self.wrap_course_map()
        self.create_table()

    def active_course_table(self, course_manager=None, delete_other=False):
        self.course_manager = course_manager or self.course_manager
        self.active_table_manager()
        if delete_other:
            self.delete_other_table_manager()

    def upload_subjects(self, subjects, new_name=False):
        """
        用于client调用，创建科目
        :param subjects: [Subject, Subject]
        :param new_name: False
        :return:
        """
        self.wrap_subject_map()
        self.create_subjects(subjects, new_name)

    def upload_classrooms(self, classrooms):
        """
        用于client调用，创建教室
        :param classrooms: [Classroom, Classroom]
        :return:
        """
        self.wrap_classroom_map()
        self.wrap_class_map()
        self.create_classrooms(classrooms)

    def upload_news(self, news):
        """
        用于client调用，创建新闻
        :param news: News
        :return:
        """
        if news.category == TypeSet.CLASS_TYPE:
            self.wrap_class_map()
        elif news.category == TypeSet.CLASSROOM_TYPE:
            self.wrap_classroom_map()
        self.create_news(news)

    def upload_notice(self, notice):
        """
        用于client调用，创建通知
        :param notice: Notice
        :return:
        """
        if notice.category == TypeSet.CLASS_TYPE:
            self.wrap_class_map()
        elif notice.category == TypeSet.CLASSROOM_TYPE:
            self.wrap_classroom_map()
        self.create_notice(notice)

    def upload_video(self, video):
        """
        用于client调用，创建视频
        :param video: Video
        :return:
        """
        if video.category == TypeSet.CLASS_TYPE:
            self.wrap_class_map()
        elif video.category == TypeSet.CLASSROOM_TYPE:
            self.wrap_classroom_map()
        try:
            self.create_video(video)
        except (RequestError,) as e:
            if e.code == 8:
                print("视频名称已存在")
            else:
                raise e

    def upload_album(self, album):
        """
        用于client调用，创建相册
        :param album: Album
        :return:
        """
        self.wrap_album_map()
        if album.category == TypeSet.CLASS_TYPE:
            self.wrap_class_map()
        elif album.category == TypeSet.CLASSROOM_TYPE:
            self.wrap_classroom_map()
        self.create_album(album)
        self.create_image(album.images, album.uid)

    def upload_image(self, images):
        """
        用于client调用，创建相册
        :param images: [Image, Image, Image]
        :return:
        """
        self.wrap_album_map()
        img_set = self.arrange_images(images)
        for album_id, imgs in img_set.items():
            self.create_image(imgs, album_id)

    def get_active_schedule(self):
        """
        获取已激活的作息
        :return:
        """
        res = self.nirvana_requester.get_schedule_list(params={"rest_table__is_active": "true"})
        schedule = res.get('results', []) if isinstance(res, dict) else res
        return schedule or []

    def get_active_table(self):
        """
        获取已激活的作息
        :return:
        """
        res = self.nirvana_requester.get_table_manager(params={"is_active": "true"})
        table = res.get('results', []) if isinstance(res, dict) else res
        return table or []

    def get_future_exam_classroom(self):
        exam_res = self.nirvana_requester.get_exam_list(params={"state": "3"})
        exam = exam_res.get('results', []) if isinstance(exam_res, dict) else exam_res
        room_list = []
        if exam:
            for e in exam:
                room_res = self.nirvana_requester.get_exam_classroom_list(params={"exam": e["uid"]})
                if isinstance(room_res, dict):
                    room = room_res.get('results', [])
                    room_list.extend(room)
        return room_list

    def upload_user_avatar(self, file_path, user_id):
        return self.edtech_requester.upload_user_avatar(file_path, user_id)

    def upload_user_face(self, file_path, data):
        return self.nirvana_requester.upload_face_file(file_path, data)

    def upload_meeting_rooms(self, meeting_rooms):
        self.wrap_student_map()
        self.wrap_teacher_map()
        self.wrap_classroom_map()
        self.clear_meeting_rooms()
        self.create_meeting_rooms(meeting_rooms)

    def wrap_edu_org_user_map(self):
        """
        拉取行政管理人员列表，映射出uid
        :return:
        """
        self.edu_org_user_map = self.edtech_requester.wrap_map("get_edu_org_user_list", ["number"], "uuid")


class BackboneV1(Backbone):
    def __init__(self, school_id):
        super(BackboneV1, self).__init__(school_id)

    def create_table(self):
        """
        创建课程表上的课位
        :return:
        """
        print(">>>Create Course Table")
        index, total = 0, len(self.course_manager.courses)
        for course in self.course_manager.courses:
            index += 1
            for position in course.schedule:
                course_id = self.course_map.get(str(course.number), None)
                if course_id:
                    table_data = {"course": {"uid": self.course_map[str(course.number)]},
                                  "manager": {"uid": self.course_manager.uid},
                                  "num": position[0], "week": position[1]}
                    self.nirvana_requester.set_course_position(table_data)
            print("##### already create {}/{} course position ####".format(index, total))


class BackboneV2(Backbone):
    def __init__(self, school_id):
        super(BackboneV2, self).__init__(school_id)

    def get_semester_list(self, params={}):
        """
        获取学期列表
        """
        res = self.nirvana_requester.get_semester_list(params)
        data = res.get('results', [])
        return data

    def get_rest_list(self, params={}):
        """
        获取学期列表
        """
        res = self.nirvana_requester.get_rest_table(params)
        data = res.get('results', [])
        return data

    def create_semester(self, semester):
        """
        创建学期
        :param semester:
        :return:
        """
        old_semester = self.get_semester_list(params={"name": semester.name})
        if old_semester:
            semester.uid = old_semester[0]['uid']
            self.nirvana_requester.update_semester(semester.uid, semester.nirvana_data)
        else:
            res_data = self.nirvana_requester.create_semester(semester.nirvana_data)
            semester.uid = res_data['uid']

    def active_semester(self, semester, delete_other=False):
        """
        激活学期
        :param semester:
        :param delete_other:
        :return:
        """
        old_semester = self.get_semester_list(params={"name": semester.name})
        if old_semester[0]['is_active']:
            return
        semester.uid = old_semester[0]['uid']
        self.nirvana_requester.active_semester(semester.uid)
        if delete_other:
            self.delete_other_semester([semester.name])

    def delete_other_semester(self, remain_names):
        """
        删除其他学期
        :param remain_names: [name, name]
        :return:
        """
        semesters = self.get_semester_list()
        for semester in semesters:
            if semester['name'] not in remain_names:
                self.delete_other_table_manager(semester_id=semester['uid'])
                for rest_table in semester['rest_table']:
                    self.nirvana_requester.delete_rest_table(rest_table['uid'])
                self.nirvana_requester.delete_semester(semester['uid'])

    def delete_other_table_manager(self, *args, **kwargs):
        semester_id = kwargs.get("semester_id")
        remain = kwargs.get("remain", [])
        managers = self.get_course_manager_list(key="semester", value=semester_id)
        for manager in managers:
            if manager['number'] not in remain:
                self.delete_table_manager(manager['uid'])

    def create_rest_table(self, is_active=False):
        """
        创建作息表
        """
        semester = self.get_semester_list(params={"name": self.rest_table.semester_name})
        self.rest_table.semester_id = semester[0]['uid']
        is_created = False
        for old_rest_table in semester[0]['rest_table']:
            if self.rest_table.name == old_rest_table["name"]:
                is_created = True
                self.rest_table.uid = old_rest_table["uid"]
                break
        if not is_created:
            upload_data = self.rest_table.nirvana_data
            res_data = self.nirvana_requester.create_rest_table(upload_data)
            self.rest_table.uid = res_data['uid']
        schedule_data = self.rest_table.schedule_nirvana_data
        self.nirvana_requester.rest_schedule_batch_update(schedule_data)

    def relate_course_manager_field(self):
        """
        关联课程表所需字段
        :return:
        """
        semester = self.get_semester_list(params={"name": self.course_manager.semester_name})
        self.course_manager.semester_id = semester[0]['uid']
        rest = self.get_rest_list(params={"name": self.course_manager.rest_name, "semester": semester[0]['uid']})
        self.course_manager.rest_id = rest[0]['uid']
        for class_num in self.course_manager.sections_num:
            section_id = self.class_map.get(class_num, None)
            if section_id:
                self.course_manager.sections.append(section_id)
        for room_num in self.course_manager.classrooms_num:
            room_id = self.classroom_map.get(room_num, None)
            if room_id:
                self.course_manager.classrooms.append(room_id)

    def create_course_manager(self, is_active=True):
        res_data = self.nirvana_requester.create_table_manager(self.course_manager.nirvana_data)
        self.course_manager.uid = res_data['uid']
        self.nirvana_requester.course_table_bind_rest(self.course_manager.rest_data)
        self.nirvana_requester.course_table_bind_section(self.course_manager.section_data)
        self.nirvana_requester.course_table_bind_classroom(self.course_manager.classroom_data)

    def create_table(self):
        """
        创建课程表上的课位
        :return:
        """
        print(">>>Create Course Table")
        index, total = 0, len(self.course_manager.courses)
        for course in self.course_manager.courses:
            index += 1
            for classroom_num, positions in course.schedule.items():
                course_id = self.course_map.get(str(course.number), None)
                classroom_id = self.classroom_map.get(classroom_num, None)
                if course_id and classroom_id:
                    for position in positions:
                        table_data = {"course": {"uid": self.course_map[str(course.number)]},
                                      "manager": {"uid": self.course_manager.uid},
                                      "num": position[0], "week": position[1],
                                      "classroom": classroom_id,
                                      "category": position[2]}
                        self.nirvana_requester.set_course_position(table_data)
            print("##### already create {}/{} course position ####".format(index, total))

    def upload_semester(self, semester):
        self.create_semester(semester)

    def relate_course_field(self):
        """
        将模型Course中的字段通过映射，转换为uid。(班牌后台接口结构)
        :return:
        """
        for course in self.course_manager.courses:
            course.subject_id = self.subject_map.get(str(course.subject_number), None)
            if not course.subject_id:
                print(">>>ERROR: subject_number{}错误，无法找到对应的科目".format(course.subject_number))
            classroom_id = self.classroom_map.get(str(course.classroom_number), None)
            if classroom_id:
                course.classrooms = [classroom_id]
            course.teacher_id = self.teacher_map.get(course.teacher_number, None)
            course.class_id = self.class_map.get(course.class_name, None)
            for student_number in course.student_list:
                student_id = self.student_map.get(student_number, None)
                if not student_id:
                    print(">>>ERROR: student_number{}错误，无法找到对应的学生".format(student_number))
                course.student_ids.append(student_id)

    def upload_course_table(self, course_manager=None, is_active=False, create_manager=True):
        """
        用于client调用，创建课程表
        :param course_manager: instance of CourseTableManager for create
        :param is_active: 创建好课程表后是否立即激活，不建议立即激活
        :param create_manager: create course table manager or not
        :return:
        """
        self.course_manager = course_manager or self.course_manager
        if not create_manager and not self.course_manager.uid:
            raise AttributeError("Course manager must have uid or create one")
        self.wrap_subject_map()
        self.wrap_classroom_map()
        self.wrap_teacher_map(origin="edtech")
        self.wrap_class_map(origin="edtech")
        self.wrap_student_map(origin="edtech")
        self.relate_course_manager_field()
        self.relate_course_field()
        if create_manager:
            # self.delete_other_table_manager(semester_id=self.course_manager.semester_id,
            #                                 remain=[self.course_manager.number])
            self.create_course_manager(is_active)
        self.create_courses()
        self.wrap_course_map()
        self.create_table()

    def active_course_table(self, course_manager=None, delete_other=False):
        self.course_manager = course_manager or self.course_manager
        semester = self.get_semester_list(params={"name": self.course_manager.semester_name})
        self.delete_other_table_manager(semester_id=semester[0]['uid'], remain=[self.course_manager.number])

    def delete_all_table_manager(self, semester_name):
        semester = self.get_semester_list(params={"name": semester_name})
        semester_id = semester[0]['uid'] if semester else None
        if not semester_id:
            return
        managers = self.get_course_manager_list(key="semester", value=semester_id)
        for manager in managers:
            self.delete_table_manager(manager['uid'])
        rest_tables = self.get_rest_table_list(key="semester", value=semester_id)
        for rest_table in rest_tables:
            self.delete_rest_table(rest_table['uid'])
