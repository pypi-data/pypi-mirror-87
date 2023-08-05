import datetime
import uuid
from copy import deepcopy
from requester.base import Requester
from config import NICE_SECRET_KEY, NICE_APP_KEY
from utils.code import get_md5_hash


class NiceRequester(Requester):
    TOKEN_MAP = {"3552": {"schoolID": "3552", "login": "banpai_shizhong", "token": "dd598079f7ca5a3e16bcf42c711c6863"},
                 "3490": {"schoolID": "3490", "login": "banpai_waiguoyu", "token": "36efbe536ee561349bf5a575bacfcce8"}}

    def __init__(self, school_number, *args, **kwargs):
        base_data = kwargs.pop("base_data", {})
        super(NiceRequester, self).__init__(*args, **kwargs)
        self.school_number = school_number
        default_base_data = {"schoolID": school_number or "3532", "login": "banpai_01",
                             "token": "d0df559761fdd8ad0db754def2f56954"}
        self.base_data = self.TOKEN_MAP.get(school_number, default_base_data)
        self.base_data.update(base_data)

    def get_sign_data(self):
        sys_time = int(datetime.datetime.now().timestamp())
        random_str = str(uuid.uuid4()).replace('-', "")[:6]
        if self.school_number:
            sign_str = "randomStr={}&schoolID={}&sysTime={}&secretKey={}".format(random_str, self.school_number,
                                                                                 sys_time, NICE_SECRET_KEY)
        else:
            sign_str = "randomStr={}&sysTime={}&secretKey={}".format(random_str, sys_time, NICE_SECRET_KEY)
        sign = get_md5_hash(sign_str).lower()
        sign_data = {"appKey": NICE_APP_KEY, "sysTime": sys_time, "randomStr": random_str,
                     "sign": sign}
        if self.school_number:
            sign_data['schoolID'] = self.school_number
        return sign_data

    @property
    def sign_data(self):
        # return self.base_data
        return self.get_sign_data()

    def check_res(self, data):
        if data['status'] != 'success':
            raise ConnectionError(data['errorMessage'])
        return data['result'], True

    def upload_attendance(self, data):
        route = "/classadmin/loadCheckings"
        data.update(self.sign_data)
        res = self._post_method(route, data)
        return res

    def get_school_list(self):
        route = "/scheduler/getSchools/"
        base_data = deepcopy(self.sign_data)
        res = self._post_method(route, base_data)
        return res


nice_requester = NiceRequester("3552", protocol="https", host="xgk.lanzhou.edu.cn:20952/schoolscheduleserv/integration")
nice_res = nice_requester.upload_attendance({'schoolID': '3552', 'data': [
    {'checkingTime': '2020-05-12T00:45:40Z', 'studentEID': '20190006', 'locationID': '1', 'cardID': None}],
                                             'serial': 0})
