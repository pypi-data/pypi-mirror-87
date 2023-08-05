from ..requester import Requester
from ..settings import CLASS_CARD_SERVER_TOKEN, CLASS_CARD_SCHOOL
from ..utils.exceptions import RequestError


class NirvanaRequester(Requester):
    def __init__(self, *args, **kwargs):
        super(NirvanaRequester, self).__init__(*args, **kwargs)
        self.school_id = kwargs.get('school_id', CLASS_CARD_SCHOOL)
        self.headers = {"X-Custom-Header-3School": self.school_id,
                        "X-Custom-Header-3App": "classcard",
                        "Authorization": CLASS_CARD_SERVER_TOKEN}

    def check_res(self, data):
        if data['code'] != 0:
            raise RequestError(message=data['message'], code=data['code'])
        return data['data'], data['code']

    def get_subject_list(self, params={}):
        route = "/api/subject/"
        res = self._get_method(route, params=params)
        return res

    def get_classroom_list(self, params={}):
        route = "/api/classroom_mini/"
        res = self._get_method(route, params=params)
        return res

    def get_student_list(self, params={}):
        route = "/api/student_search/"
        res = self._get_method(route, params=params)
        return res

    def get_teacher_list(self, params={}):
        route = "/api/teacher_mini/"
        res = self._get_method(route, params=params)
        return res

    def get_class_list(self, params={}):
        route = "/api/class/"
        res = self._get_method(route, params=params)
        return res

    def create_table_manager(self, data):
        route = "/api/course_table_manager/"
        res = self._post_method(route, data)
        return res

    def set_manager_mode(self, data):
        route = "/api/course_walking_mode/"
        res = self._post_method(route, data)
        return res

    def course_table_bind_rest(self, data):
        route = "/api/course_table_bind_rest/"
        res = self._put_method(route, data)
        return res

    def course_table_bind_section(self, data):
        route = "/api/course_table_bind_section/"
        res = self._put_method(route, data)
        return res

    def course_table_bind_classroom(self, data):
        route = "/api/course_table_bind_classroom/"
        res = self._put_method(route, data)
        return res

    def set_course_position(self, data):
        route = "/api/course_table/"
        res = self._post_method(route, data)
        return res

    def batch_create_course(self, data):
        route = "/api/course_batch/"
        res = self._post_method(route, data)
        return res

    def get_course_list(self, params={}):
        route = "/api/course_list/"
        res = self._get_method(route, params=params)
        return res

    def get_table_manager(self, params):
        route = "/api/course_table_manager/"
        res = self._get_method(route, params)
        return res

    def delete_table_manager(self, uid):
        route = "/api/course_table_manager/{}/".format(uid)
        data = {"soft": False,
                "force": True}
        res = self._delete_method(route, data)
        return res

    def active_table_manager(self, uid):
        route = "/api/course_table_active/"
        data = {"uid": uid}
        res = self._post_method(route, data)
        return res

    def delete_classroom_course(self, classroom_id, manager_id):
        route = "/api/course/?classroom__uid={}&manager__uid={}".format(classroom_id, manager_id)
        res = self._delete_method(route, data={"force": True})
        return res

    def get_active_manager(self):
        route = "/api/course_table_manager/"
        res = self._get_method(route, {"is_active": "true"})
        data = res.get('results', None)
        return data[0]['uid']

    def create_classroom(self, data):
        route = "/api/classroom/"
        res = self._post_method(route, data)
        return res

    def update_classroom(self, uid, data):
        route = "/api/classroom/{}/".format(uid)
        res = self._put_method(route, data)
        return res

    def create_subject(self, data):
        route = "/api/subject/"
        res = self._post_method(route, data)
        return res

    def update_subject(self, uid, data):
        route = "/api/subject/{}/".format(uid)
        res = self._put_method(route, data)
        return res

    def get_rest_table(self, params):
        route = "/api/rest_table/"
        res = self._get_method(route, params)
        return res

    def active_rest_table(self, uid):
        route = "/api/rest_table_active/"
        data = {"uid": uid}
        res = self._post_method(route, data)
        return res

    def get_semester_list(self, params):
        route = "/api/semester/"
        res = self._get_method(route, params)
        return res

    def create_semester(self, data):
        route = "/api/semester/"
        res = self._post_method(route, data)
        return res

    def update_semester(self, uid, data):
        route = "/api/semester/{}/".format(uid)
        res = self._put_method(route, data)
        return res

    def active_semester(self, uid):
        route = "/api/semester_active/"
        data = {"uid": uid}
        res = self._post_method(route, data)
        return res

    def delete_semester(self, uid):
        route = "/api/semester/{}/".format(uid)
        data = {"soft": False,
                "force": True}
        res = self._delete_method(route, data)
        return res

    def create_rest_table(self, data):
        route = "/api/rest_table/"
        res = self._post_method(route, data)
        return res

    def delete_rest_table(self, uid):
        route = "/api/rest_table/{}/".format(uid)
        data = {"soft": False,
                "force": True}
        res = self._delete_method(route, data)
        return res

    def rest_schedule_batch_update(self, data):
        route = "/api/rest_schedule_batch_update/"
        res = self._put_method(route, data)
        return res

    def create_news(self, data):
        route = "/api/news/"
        res = self._post_method(route, data)
        return res

    def create_board(self, data):
        route = "/api/board/"
        res = self._post_method(route, data)
        return res

    def get_album_list(self, params):
        route = "/api/album/"
        res = self._get_method(route, params)
        return res

    def create_album(self, data):
        route = "/api/album/"
        res = self._post_method(route, data)
        return res

    def update_album(self, album_id, data):
        route = "/api/album/{}/".format(album_id)
        res = self._put_method(route, data)
        return res

    def create_image(self, data):
        route = "/api/image_bat/"
        res = self._post_method(route, data)
        return res

    def create_video(self, data):
        route = "/api/video/"
        res = self._post_method(route, data)
        return res

    def modify_classroom_news(self, data):
        route = "/api/classroom_news_modify/"
        res = self._put_method(route, data)
        return res

    def modify_classroom_broad(self, data):
        route = "/api/classroom_broad_modify/"
        res = self._put_method(route, data)
        return res

    def modify_classroom_album(self, data):
        route = "/api/classroom_album_modify/"
        res = self._put_method(route, data)
        return res

    def modify_classroom_video(self, data):
        route = "/api/classroom_video_modify/"
        res = self._put_method(route, data)
        return res

    def upload_file(self, file_path):
        route = "/api/upload/"
        with open(file_path, 'rb') as f:
            res = self._post_file_method(route, {'file': f})
        return res

    def get_exam_classroom_list(self, params={}):
        route = "/api/exam_classroom/"
        res = self._get_method(route, params=params)
        return res

    def get_exam_list(self, params={}):
        route = "/api/exam_list/"
        res = self._get_method(route, params=params)
        return res

    def get_schedule_list(self, params={}):
        route = "/api/rest_schedule/"
        res = self._get_method(route, params=params)
        return res

    def get_meeting_room_list(self, params={}):
        route = "/api/meeting_room/"
        res = self._get_method(route, params=params)
        return res

    def delete_meeting_room(self, uid):
        route = "/api/meeting_room/{}/".format(uid)
        res = self._delete_method(route)
        return res

    def create_meeting_room(self, data):
        route = "/api/meeting_room/"
        res = self._post_method(route, data)
        return res

    def create_meeting_room_rule(self, data):
        route = "/api/attendance_meeting/rule/"
        res = self._post_method(route, data)
        return res

    def bind_meeting_room_user(self, data):
        route = "/api/meeting/conventioneer/bind_by_user/"
        res = self._put_method(route, data)
        return res

    def unbind_meeting_room_user(self, data):
        route = "/api/meeting/conventioneer/unbind/"
        res = self._put_method(route, data)
        return res

    def delete_classroom(self, uid):
        route = "/api/classroom/{}/".format(uid)
        data = {"soft": False,
                "force": True}
        res = self._delete_method(route, data)
        return res

    def delete_subject(self, uid):
        route = "/api/subject/{}/".format(uid)
        data = {"soft": False,
                "force": True}
        res = self._delete_method(route, data)
        return res

    def upload_face_file(self, file_path, data):
        route = "/api/upload_face_img/"
        data["category"] = "face"
        with open(file_path, 'rb') as f:
            res = self._post_file_method(route, {'file': f}, data=data)
        return res
