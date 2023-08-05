import datetime
from sync.base import BaseSync
from utils.loggerutils import logging
from classcard_dataclient.models.user import Student, Teacher, GenderSet

logger = logging.getLogger(__name__)


class TeacherSync(BaseSync):
    def __init__(self):
        super(TeacherSync, self).__init__()
        now = datetime.datetime.now()
        self.offset = 300
        self.create = True
        self.teacher_list = []
        self.teacher_map = {}

    def extract_teacher(self):
        sex_map = {0: GenderSet.FEMALE, 1: GenderSet.MALE}
        sql = "SELECT CUSTOMERID, OUTID, NAME, Sex, CARDSFID, SCARDSNR FROM BASE_CUSTOMERS " \
              "WHERE CARDSFID=0 ORDER BY OUTID"
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        for row in rows:
            external_id, number, name, sex, role_id, ecard = row[0], row[1], row[2], row[3], row[4], row[5]
            gender = sex_map.get(sex, GenderSet.MALE)
            if external_id not in self.teacher_map:
                teacher = Teacher(number=number, name=name, password="MTIzNDU2", gender=gender, ecard=ecard,
                                  email="teacher{}@edu.com".format(number), birthday="1980-01-01",
                                  phone='0000000', school=self.school_id)
                self.teacher_map[external_id] = number
                self.teacher_list.append(teacher)

    def sync(self):
        self.extract_teacher()
        if not self.teacher_map:
            logger.info("没有老师信息")
            return
        # if self.create:
        #     code, data = self.client.create_teacher(self.teacher_list)
        #     logger.info("Code: {}, Msg: {}".format(code, data))
        self.close_db()
