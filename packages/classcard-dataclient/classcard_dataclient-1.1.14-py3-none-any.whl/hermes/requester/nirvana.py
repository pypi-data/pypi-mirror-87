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

    def get_student_attendance_info(self, uid):
        route = "/api/attendance_student/{}/".format(uid)
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


import datetime
from requester.profession import NiceRequester
from utils.dateutils import datetime2str_z, str2datetime
from config import CLASS_CARD_HOST, CLASS_CARD_PORT, NICE_HOST, NICE_PROTOCOL
from utils.redis_utils import RedisCache
from utils.loggerutils import logging

nirvana_requester = NirvanaRequester(school_id="6955f5c0-e988-4792-b219-5a3c89b8fb87",
                                     host="125.75.1.13", port=14001)
course_data = nirvana_requester.get_course_info(params={"classroom": "48808052-3d1b-46a3-88ce-b0ddc1c97d5c"})
print(course_data)
school_data = nirvana_requester.get_school_info("6955f5c0e9884792b2195a3c89b8fb87")
print(school_data)
attendance_data = nirvana_requester.get_student_attendance_info("bca79428-a586-4358-a818-e4d40355efdb")
record_time = attendance_data['record_time']
print(attendance_data)
record_time = str2datetime(record_time)
checking_time = datetime2str_z(record_time - datetime.timedelta(hours=8))
school_number = school_data['code'] or "1499"
student_data = nirvana_requester.get_student_info("6bb88751-cbe1-4cfb-ae99-d41ac27ad046")
attendance_data = {"checkingTime": checking_time, "studentEID": student_data['number'],
                   "locationID": attendance_data['classroom']['num'],
                   "cardID": student_data['ecard']['sn'] if student_data['ecard'] else None}
print(attendance_data)