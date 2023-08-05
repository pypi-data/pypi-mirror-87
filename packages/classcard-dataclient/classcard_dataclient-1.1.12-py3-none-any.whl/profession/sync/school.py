from sync import BaseSync
from classcard_dataclient.models.school import School
from utils.loggerutils import logging
from config import SCHOOL_NAME

logger = logging.getLogger(__name__)


class SchoolSync(BaseSync):
    def __init__(self, *args, **kwargs):
        super(SchoolSync, self).__init__(*args, **kwargs)
        self.school_map = {}
        self.special_number = kwargs.get('special_number', None)

    def map_name(self, code):
        code_name = {"1153": "北京市第一六六中学(QA)",
                     "1165": "北京市第二中学(QA)",
                     "1481": "深圳市福田区外国语高级中学(QA)",
                     "3400": "好专业大数据（QA）",
                     "3532": "班牌对接测试"}
        return code_name[code]

    def sync(self):
        res = self.nice_requester.get_school_list()
        res_data = res.get('schools', [])
        logger.info(res_data)
        for index, rd in enumerate(res_data):
            # school_res = self.nice_requester.get_school_info(rd['schoolID'])
            # school_info = school_res['schoolInfo']
            name, number = rd['schoolName'], rd['schoolID']
            # name = self.map_name(number)
            if self.special_number and number != self.special_number:
                continue
            phone_number = "123456{}".format(number)
            email_number = "school{}@edt.com".format(number)
            school = School(name=name, number=number, description=name, phone=phone_number,
                            province="甘肃省", area='市辖区', city="兰州市", address=name, motto=name,
                            principal_name=name, principal_email=email_number, principal_phone=phone_number)
            logger.info(">>> Already add {}/{} school".format(index + 1, len(res_data)))
            print(">>> Already add {}/{} school".format(index + 1, len(res_data)))
            # self.client.create_school(school)
            self.school_map[name] = number
