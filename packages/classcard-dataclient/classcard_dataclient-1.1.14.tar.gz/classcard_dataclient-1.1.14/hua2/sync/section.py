import datetime
from sync.base import BaseSync
from utils.loggerutils import logging
from classcard_dataclient.models import Class

logger = logging.getLogger(__name__)


class SectionSync(BaseSync):
    def __init__(self):
        super(SectionSync, self).__init__()
        now = datetime.datetime.now()
        self.offset = 300
        self.create = True
        self.section_map = {}
        self.name_num = {}

    def extract_section(self):
        sql = "SELECT DPCODE1, DPNAME1, DPCODE2, DPNAME2, DPCODE3, DPNAME3, DPCODE4, DPNAME4 FROM BASE_CUSTDEPT ORDER BY DPCODE1"
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        for row in rows:
            code1, name1, code2, name2 = row[0], row[1], row[2], row[3]
            code3, name3, code4, name4 = row[4], row[5], row[6], row[7]
            code_list = [code1, code2, code3, code4]
            name_list = [name1, name2, name3, name4]
            c_code, c_name = [], []
            for ci in code_list:
                if ci != "000":
                    c_code.append(ci)
            for ni in name_list:
                if ni != "000":
                    c_name.append(ni)
            code = "".join(c_code)
            name = "/".join(c_name)
            section = Class(name=name, number=code, grade="高中一年级", school=self.school_id)
            self.section_map[code] = section
            self.name_num[name] = code

    def sync(self):
        self.extract_section()
        if not self.section_map:
            logger.info("没有班级信息")
            return
        # if self.create:
        #     for code, section in self.section_map.items():
        #         code, data = self.client.create_section(sections=section)
        #         if code:
        #             logger.error("Code: {}, Msg: {}".format(code, data))
        self.close_db()
