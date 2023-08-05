from requester import Requester
from config import SDTU_SERVER, SDTU_APP_ID, SDTU_SECRET_KEY


class SDTURequester(Requester):
    def __init__(self, *args, **kwargs):
        headers = {"applyId": SDTU_APP_ID,
                   "secretKey": SDTU_SECRET_KEY}
        server = SDTU_SERVER
        super(SDTURequester, self).__init__(headers=headers, server=server, *args, **kwargs)

    def check_res(self, data):
        if data["status"] == 200:
            return data, 0
        else:
            return None, None

    def get_yj_student_list(self, **data):
        route = "/REST/YJSXXZX/WC"
        res = self._post_method(route, data=data)
        return res

    def get_bk_student_list(self, **data):
        route = "/REST/JWXSJBXX/WC"
        res = self._post_method(route, data=data)
        return res

    def get_teacher_list(self, **data):
        route = "/REST/JZGJBXX/WC"
        res = self._post_method(route, data=data)
        return res

    def get_ecard_list(self, **data):
        route = "/REST/YKTKH/WC"
        res = self._post_method(route, data=data)
        return res

    def get_section_list(self, **data):
        route = "/REST/JWXZB/WC"
        res = self._post_method(route, data=data)
        return res

    def get_bks_classroom_list(self, **data):
        route = "/REST/JWJSXXB/WC"
        res = self._post_method(route, data=data)
        return res

    def get_yjs_classroom_list(self, **data):
        route = "/getREST_YJSJSJBXX_8f0aa2ef73c842098cedc8c745a8c18e"
        res = self._post_method(route, data=data)
        return res

    def get_rent_classroom_list(self, **data):
        route = "/REST/JWJSJYB/XNXQ"
        res = self._post_method(route, data=data)
        return res

    def get_yjs_course_table(self, **data):
        route = "/REST/YJSPKXX/WC"
        res = self._post_method(route, data=data)
        return res

    def get_bks_course_table(self, **data):
        route = "/REST/JWXSKB/XNXQ"
        res = self._post_method(route, data=data)
        return res

    def get_teacher_course_table(self, **data):
        route = "/REST/JWJSKB/XNXQ"
        res = self._post_method(route, data=data)
        return res

    def get_bks_semester(self, **data):
        route = "/getREST_JWXNXQ_15810dffe97a41f68b1babb0da779736"
        res = self._post_method(route, data=data)
        return res

    def get_yjs_semester(self, **data):
        route = "/getREST_YJSXL_83cc62e7ab9243f39a07cb0fcc69fd75"
        res = self._post_method(route, data=data)
        return res
