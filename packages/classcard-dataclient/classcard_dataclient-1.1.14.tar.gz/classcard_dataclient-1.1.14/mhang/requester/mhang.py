# -*- coding: utf-8 -*-#
from urllib.parse import urljoin
import requests
from config import MHANG_BASE_URL, MHANG_CLIENT_ID, MHANG_CLIENT_SECRET, MHANG_EDU_ID
from utils.dateutils import get_last_update_time, set_update_time
from utils.loggerutils import logging
LOG = logging.getLogger(__name__)


class MhEdu(object):
    def __init__(self):
        # base_url,client_id, client_secret,edu_id针对不同环境需要替换
        self.base_url = MHANG_BASE_URL
        self.client_id = MHANG_CLIENT_ID
        self.client_secret = MHANG_CLIENT_SECRET
        # 教育局机构id
        self.edu_id = MHANG_EDU_ID
        self.token = self.get_token()

    def get_token(self):
        uri = "/oauth-server/oauth/client/token"
        url = urljoin(self.base_url, uri)
        params = {"client_id": self.client_id, 'client_secret': self.client_secret}
        ret = requests.get(url, params=params)
        if ret.status_code == 200:
            data = ret.json()
            token = data.get("value")
            # token_type = data.get("tokenType")
            return token
        return None

    def process_post(self, url, data):
        headers = {"Authorization": "Bearer {}".format(self.token)}
        print("token", self.token)
        ret = requests.post(url, json=data, headers=headers)
        if ret.status_code == 200:
            ret = ret.json()
            total = ret.get("total")
            records = ret.get("records")
            return total, records
        else:
            return None, None

    def process_paging(self, url, data, total, size):
        result = []
        total_page = total // size
        if total % size:
            # 有余数页码+1
            total_page += 1
        for i in range(1, total_page):
            # 从1开始，可以少调一次接口
            data['current'] = i + 1
            records = self.process_post(url, data)
            result += records
        return result

    def get_schools(self, size=100):
        uri = "/openapi/ecp-datacenter-svc/schools"
        url = urljoin(self.base_url, uri)
        data = {"jgId": self.edu_id, "size": size}
        last_update_time = get_last_update_time("schools")
        if last_update_time:
            data["updateTime"] = last_update_time
        schools = []
        try:
            total, records = self.process_post(url, data)

            if total and total > size:
                # 查询分页信息
                schools += self.process_paging(url, data, total, size)

            else:
                # 不需要分页
                schools = records
            if total:
                set_update_time("schools")
        except Exception as e:
            LOG.info("get schools info error -{}".format(e))
        return schools

    def get_org_class(self, school_id=None, size=100):
        uri = "/openapi/ecp-datacenter-svc/orgClasses"
        url = urljoin(self.base_url, uri)
        data = {"jgId": school_id, "size": size}
        last_update_time = get_last_update_time("orgclass")
        if last_update_time:
            data["updateTime"] = last_update_time
        classes = []
        try:
            total, records = self.process_post(url, data)
            if total and total > size:
                # 查询分页信息
                classes += self.process_paging(url, data, total, size)

            else:
                # 不需要分页
                classes = records
            if total:
                set_update_time("orgclass")
        except Exception as e:
            LOG.info("get org classes error -{}".format(e))
        return classes

    def get_students(self, school_id=None, class_id=None, size=100):
        uri = "/openapi/ecp-datacenter-svc/user/student"
        url = urljoin(self.base_url, uri)
        data = {"jgId": school_id, "bjId": class_id, "size": size}
        last_update_time = get_last_update_time("students")
        if last_update_time:
            data["updateTime"] = last_update_time
        students = []
        try:
            total, records = self.process_post(url, data)
            if total and total > size:
                # 查询分页信息
                students += self.process_paging(url, data, total, size)

            else:
                # 不需要分页
                students = records
            if total:
                set_update_time("students")
        except Exception as e:
            LOG.info("get students list error -{}".format(e))
        return students

    def get_teachers(self, school_id=None, size=100):
        uri = "/openapi/ecp-datacenter-svc/user/teacher"
        url = urljoin(self.base_url, uri)
        data = {"jgId": school_id, "size": size}
        last_update_time = get_last_update_time("teachers")
        if last_update_time:
            data["updateTime"] = last_update_time
        teachers = []
        try:
            total, records = self.process_post(url, data)
            if total and total > size:
                # 查询分页信息
                teachers += self.process_paging(url, data, total, size)

            else:
                # 不需要分页
                teachers = records
            if total:
                set_update_time("teachers")
        except Exception as e:
            LOG.info("get teachers list error -{}".format(e))
        return teachers

    def get_edu_org_user(self, jg_id=None, size=100):
        """
        :param jg_id: 学校（机构）id
        :param size:
        :return:
        """
        uri = "/openapi/ecp-datacenter-svc/user/eduorg"
        url = urljoin(self.base_url, uri)
        data = {"jgId": jg_id, "size": size}
        last_update_time = get_last_update_time("org_user")
        if last_update_time:
            data["updateTime"] = last_update_time
        org_user = []
        try:
            total, records = self.process_post(url, data)
            if total and total > size:
                # 查询分页信息
                org_user += self.process_paging(url, data, total, size)

            else:
                # 不需要分页
                org_user = records
            if total:
                set_update_time("org_user")
        except Exception as e:
            LOG.info("get org user list error -{}".format(e))
        return org_user


if __name__ == "__main__":
    # d5e4e513-bcef-414a-a22a-1c9cbf27364c bearer
    c = MhEdu()
    # 2d4aab3927127fba1b8ec2666ee86461
    # 2d4aab3927127fbaa8a54aee797f7a60 school
    cl = c.get_edu_org_user("2d4aab3927127fba1b8ec2666ee86461")
    # cl = c.get_schools()
    print(cl)
    # s = c.get_students("2d4aab3927127fbaa8a54aee797f7a60", "2d4aab3927127fba68e2fc135b302a28")
    # print(s)
    # se = c.get_org_class()
