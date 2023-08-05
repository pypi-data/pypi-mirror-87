from sync import BaseSync
from classcard_dataclient.models.user import Teacher
from utils.loggerutils import logging

logger = logging.getLogger(__name__)


class TeacherSync(BaseSync):
    def sync(self):
        res = self.nice_requester.get_teacher_list()
        res_data = res.get('teachers', [])
        teacher_list = []
        for index, rd in enumerate(res_data):
            teacher = Teacher(number=rd['teacherEID'], name=rd['teacherName'], password="MTIzNDU2",
                              email="teacher{}@edt.com".format(rd['teacherEID']), birthday="1980-01-01",
                              phone='0000000', school=self.school_id)
            teacher_list.append(teacher)
        code, data = self.client.create_teacher(teacher_list)
        logger.info("Code: {}, Msg: {}".format(code, data))
