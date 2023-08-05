from sync import BaseSync
from classcard_dataclient.models.user import Student, GenderSet
from utils.loggerutils import logging

logger = logging.getLogger(__name__)


class StudentSync(BaseSync):
    def __init__(self, *args, **kwargs):
        class_entrance = kwargs.pop("class_entrance", {})
        super(StudentSync, self).__init__(*args, **kwargs)
        self.class_entrance = class_entrance

    def sync(self):
        gender_map = {"1": GenderSet.MALE, "2": GenderSet.FEMALE}
        code, sections = self.client.get_section_list(school_id=self.school_id)
        if code or not isinstance(sections, list):
            logger.error("Error: get section info, Detail: {}".format(sections))
            sections = []
        # description 实则存放闵行数据下的班级id
        section_dict = {d["description"]: d['uuid'] for d in sections if d.get("number")}
        for k in self.class_entrance.keys():
            student_list = []
            students = self.mh_requester.get_students(self.mh_school_id, k)

            for index, rd in enumerate(students):
                if str(rd["originIsDeleted"]) == "1":
                    # 已删除的学生
                    code, msg = self.client.delete_student({"number": rd['username'], "name": rd['xm']}, school_id=self.school_id)
                    logger.info(">>> delete student {} result-{}-{}".format(rd['xm'], code, msg))
                else:
                    entrance_info = self.class_entrance[k]
                    # MTIzNDU2 BASE64 123456
                    student = Student(number=rd['username'], name=rd['xm'], password="MTIzNDU2",
                                      gender=gender_map.get(rd['xbm'], None), birthday=rd["csrq"],
                                      section=section_dict.get(rd['bjId'], None), phone=rd['yddh'],
                                      classof=entrance_info['classof'], graduateat=entrance_info['graduateat'],
                                      school=self.school_id)
                    student_list.append(student)
            code, data = self.client.create_student(student_list)
            logger.info("Code: {}, Msg: {}".format(code, data))
