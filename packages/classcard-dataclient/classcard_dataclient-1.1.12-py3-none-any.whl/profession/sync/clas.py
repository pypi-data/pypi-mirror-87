from sync import BaseSync
from classcard_dataclient.models.clas import Class
from utils.loggerutils import logging
from utils.code import get_md5_hash

logger = logging.getLogger(__name__)


class ClassSync(BaseSync):
    def __init__(self, *args, **kwargs):
        super(ClassSync, self).__init__(*args, **kwargs)
        self.class_entrance = {}
        self.classroom_class = {}

    def sync(self):
        study_year = {"小学": 6, "初中": 3, "高中": 3}
        res = self.nice_requester.get_class_list()
        code, res_sections = self.client.get_section_list(school_id=self.school_id)
        if code or not isinstance(res_sections, list):
            logger.error("Error: get section info, Detail: {}".format(res_sections))
            res_sections = []
        section_dict = {d["number"]: d['uuid'] for d in res_sections if d.get("number")}
        res_data = res.get('classes', [])
        sections = []
        for index, rd in enumerate(res_data):
            try:
                principal_number = rd['classTeacher']['teacherEID']
            except (Exception,):
                principal_number = None
            if rd['locationID']:
                self.classroom_class[rd['locationID']] = rd['classFullName']
            section = Class(number=rd['qualifiedClassID'], name=rd['classFullName'], grade=rd['gradeName'],
                            principal_number=principal_number, school=self.school_id)
            section.uid = section_dict.get(section.number, None)
            if rd['entranceYear'] and rd['entranceYear'].isdigit():
                entrance_info = {"classof": int(rd['entranceYear']),
                                 "graduateat": int(rd['entranceYear']) + study_year[rd["eduStage"]]}
            else:
                entrance_info = {"classof": None, "graduateat": None}
            self.class_entrance[rd['qualifiedClassID']] = entrance_info
            sections.append(section)
        code, data = self.client.create_section(sections)
        if code:
            logger.error("Code: {}, Msg: {}".format(code, data))
