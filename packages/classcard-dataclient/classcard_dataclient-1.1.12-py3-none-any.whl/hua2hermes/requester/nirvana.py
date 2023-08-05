from requester.base import Requester
from config import CLASS_CARD_SERVER_TOKEN, CLASS_CARD_SCHOOL
from utils.exceptions import RequestError


class NirvanaRequester(Requester):
    def __init__(self, *args, **kwargs):
        super(NirvanaRequester, self).__init__(*args, **kwargs)
        self.headers = {"X-Custom-Header-3School": kwargs.get('school_id', CLASS_CARD_SCHOOL),
                        "X-Custom-Header-3App": "classcard",
                        "Authorization": CLASS_CARD_SERVER_TOKEN}

    def check_res(self, data):
        if data['code'] != 0:
            raise RequestError(message=data['message'], code=data['code'])
        return data['data'], data['code']

    def get_conventioneer_record_info(self, uid):
        route = "/api/attendance_meeting/conventioneer/{}/".format(uid)
        res = self._get_method(route)
        return res

    def get_student_attendance_info(self, uid):
        route = "/api/attendance_student/{}/".format(uid)
        res = self._get_method(route)
        return res

    def get_meeting_room_info(self, uid):
        route = "/api/meeting_room/{}/".format(uid)
        res = self._get_method(route)
        return res

    def get_school_info(self, uid):
        route = "/api/school/{}/".format(uid)
        res = self._get_method(route)
        return res

    def get_student_info(self, uid):
        route = "/api/student/{}/".format(uid)
        res = self._get_method(route)
        return res

    def get_course_info(self, params):
        route = "/api/app/course_table_classroom_list/"
        res = self._get_method(route, params=params)
        return res
