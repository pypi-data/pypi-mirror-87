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
        gender_map = {"男": GenderSet.MALE, "女": GenderSet.FEMALE}
        res = self.nice_requester.get_student_list()
        code, sections = self.client.get_section_list(school_id=self.school_id)
        if code or not isinstance(sections, list):
            logger.error("Error: get section info, Detail: {}".format(sections))
            sections = []
        section_dict = {d["number"]: d['uuid'] for d in sections if d.get("number")}
        res_data = res.get('studentInfos', [])
        student_list = []
        for index, rd in enumerate(res_data):
            entrance_info = self.class_entrance[rd['qualifiedClassID']]
            student = Student(number=rd['studentEID'], name=rd['studentName'], password="MTIzNDU2",
                              gender=gender_map.get(rd['gender'], None), birthday="1996-01-01",
                              section=section_dict.get(rd['qualifiedClassID'], None),
                              classof=entrance_info['classof'], graduateat=entrance_info['graduateat'],
                              school=self.school_id)
            student_list.append(student)
        code, data = self.client.create_student(student_list)
        logger.info("Code: {}, Msg: {}".format(code, data))
