from sync import BaseSync
from classcard_dataclient.models.user import Teacher, GenderSet
from utils.loggerutils import logging

logger = logging.getLogger(__name__)


class TeacherSync(BaseSync):
    def sync(self):
        gender_map = {"1": GenderSet.MALE, "2": GenderSet.FEMALE}
        teachers = self.mh_requester.get_teachers(self.mh_school_id)

        teacher_list = []
        for index, rd in enumerate(teachers):
            if str(rd["originIsDeleted"]) == "1":
                # 已删除的老师
                code, msg = self.client.delete_teacher({"number": rd['username'], "name": rd["xm"]}, school_id=self.school_id)
                logger.info(">>> delete student {} result-{}-{}".format(rd['xm'], code, msg))
            else:
                teacher = Teacher(number=rd['username'], name=rd['xm'], password="MTIzNDU2", description=rd['username'],
                                  email="{}@edt.com".format(rd['username']), birthday=rd['csrq'],
                                  phone=rd['yddh'], school=self.school_id, gender=gender_map.get(rd['xbm'], None))
                teacher_list.append(teacher)
        code, data = self.client.create_teacher(teacher_list)
        logger.info("Code: {}, Msg: {}".format(code, data))
