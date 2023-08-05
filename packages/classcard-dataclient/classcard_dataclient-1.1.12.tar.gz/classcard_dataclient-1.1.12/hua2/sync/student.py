import datetime
from sync.base import BaseSync
from utils.loggerutils import logging
from classcard_dataclient.models.user import Student, Teacher, GenderSet

logger = logging.getLogger(__name__)


class StudentSync(BaseSync):
    def __init__(self):
        super(StudentSync, self).__init__()
        now = datetime.datetime.now()
        self.offset = 300
        self.student_list = []
        self.student_map = {}
        self.create = True
        self.student_section_map = {}

    def get_section_map(self):
        code, sections = self.client.get_section_list(school_id=self.school_id)
        if code or not isinstance(sections, list):
            logger.error("Error: get section info, Detail: {}".format(sections))
            sections = []
        section_map = {d["number"]: d['uuid'] for d in sections if d.get("number")}
        section_name_map = {d["number"]: d['name'] for d in sections if d.get("number")}
        return section_map, section_name_map

    def extract_student(self):
        section_map, section_name_map = self.get_section_map()
        sex_map = {0: GenderSet.FEMALE, 1: GenderSet.MALE}
        sql = "SELECT CUSTOMERID, OUTID, NAME, Sex, CARDSFID, CUSTDEPT, SCARDSNR FROM BASE_CUSTOMERS " \
              "WHERE CARDSFID=1 ORDER BY OUTID"
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        for row in rows:
            external_id, number, name, sex, role_id = row[0], row[1], row[2], row[3], row[4]
            section_num, ecard = row[5], row[6]
            gender = sex_map.get(sex, GenderSet.MALE)
            if external_id not in self.student_map:
                section_id = section_map.get(section_num)
                self.student_section_map[number] = section_name_map.get(section_num)
                student = Student(number=number, name=name, password="MTIzNDU2", gender=gender,
                                  birthday="1996-01-01", section=section_id, ecard=ecard,
                                  classof=2018, graduateat=2021, school=self.school_id)
                self.student_map[external_id] = number
                self.student_list.append(student)

    def sync(self):
        self.extract_student()
        if not self.student_map:
            logger.info("没有学生信息")
            return
        # if self.create:
        #     code, data = self.client.create_student(self.student_list)
        #     logger.info("Code: {}, Msg: {}".format(code, data))
        self.close_db()
