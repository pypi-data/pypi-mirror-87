from ..requester import Requester
from ..settings import EDTECH_SERVER_TOKEN, CLASS_CARD_SCHOOL


class EDTechRequester(Requester):
    def __init__(self, *args, **kwargs):
        super(EDTechRequester, self).__init__(*args, **kwargs)
        self.school_id = kwargs.get('school_id', CLASS_CARD_SCHOOL)
        self.headers = {"X-Custom-Header-3School": self.school_id,
                        "X-Custom-Header-3App": "classcard",
                        "Authorization": EDTECH_SERVER_TOKEN}

    def get_res_count(self, res):
        page = res.get('page', {}) if isinstance(res, dict) else {}
        count = page.get('count', None)
        return count

    def get_res_data(self, res):
        data = res.get('data', None) if isinstance(res, dict) else res
        return data

    def get_class_list(self, params={}):
        route = "/api/v1/schools/{}/sections/simple/".format(self.school_id)
        res = self._get_method(route, params=params)
        return res

    def get_teacher_list(self, params={}):
        route = "/api/v1/schools/{}/teachers/".format(self.school_id)
        res = self._get_method(route, params=params)
        return res

    def get_student_list(self, params={}):
        route = "/api/v1/schools/{}/students/".format(self.school_id)
        res = self._get_method(route, params=params)
        return res

    def upload_user_avatar(self, file_path, user_id):
        route = "/api/v1/users/{}/avatar/".format(user_id)
        with open(file_path, 'rb') as f:
            res = self._post_file_method(route, {'file': f})
        return res

    def get_edu_org_user_list(self, params={}):
        route = "/api/v1/eduorguser/"
        res = self._get_method(route, params=params)
        return res
