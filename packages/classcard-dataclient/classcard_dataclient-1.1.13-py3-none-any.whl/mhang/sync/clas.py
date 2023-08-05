from sync import BaseSync
from classcard_dataclient.models.clas import Class
from utils.loggerutils import logging
from utils.code import get_md5_hash

logger = logging.getLogger(__name__)


class ClassSync(BaseSync):
    def __init__(self, *args, **kwargs):
        super(ClassSync, self).__init__(*args, **kwargs)
        self.class_entrance = {}
        # self.classroom_class = {}

    def sync(self):
        classes_data = self.mh_requester.get_org_class(self.mh_school_id)
        code, res_sections = self.client.get_section_list(school_id=self.school_id)
        if code or not isinstance(res_sections, list):
            logger.error("Error: get section info, Detail: {}".format(res_sections))
            res_sections = []
        section_dict = {d["number"]: d['uuid'] for d in res_sections if d.get("number")}

        sections = []
        for index, rd in enumerate(classes_data):
            if str(rd["originIsDeleted"]) == "1":
                # 已删除班级
                code, msg = self.client.delete_section({"name": rd['bjmc'], "grade": rd['njmc']}, school_id=self.school_id)
                logger.info(">>> delete class {} result-{}-{}".format(rd['bjmc'], code, msg))
            else:
                principal_number = None
                # if rd['locationID']:
                #     self.classroom_class[rd['locationID']] = rd['classFullName']
                section = Class(number=rd['bh'], name=rd['bjmc'], grade=rd['njmc'], description=rd["id"],
                                principal_number=principal_number, school=self.school_id)
                section.uid = section_dict.get(section.number, None)
                if rd['rxnd']:
                    entrance_info = {"classof": int(rd['rxnd']),
                                     "graduateat": int(rd['bynd'])}
                else:
                    entrance_info = {"classof": None, "graduateat": None}
                self.class_entrance[rd['id']] = entrance_info
                sections.append(section)
        code, data = self.client.create_section(sections)
        if code:
            logger.error("Code: {}, Msg: {}".format(code, data))
