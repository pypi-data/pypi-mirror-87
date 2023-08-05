from sync import BaseSync
from classcard_dataclient.models.school import School

from utils.loggerutils import logging
from utils.address_utils import get_province_name, get_city_name, get_area_name
logger = logging.getLogger(__name__)


class SchoolSync(BaseSync):
    def __init__(self, *args, **kwargs):
        super(SchoolSync, self).__init__(*args, **kwargs)
        self.school_map = {}

    def sync(self):
        schools = self.mh_requester.get_schools()

        logger.info(schools)
        for index, rd in enumerate(schools):
            name, number = rd['jgmc'], rd['jgbm']
            if str(rd["originIsDeleted"]) == "1":
                # 已删除
                code, msg = self.client.delete_school(name)
                logger.info(">>> delete school {} result-{}-{}".format(name, code, msg))
            else:
                phone_number = "12345678910"
                email_number = "school{}@edt.com".format(number)
                school = School(name=name, number=number, description=name, phone=phone_number,
                                province=get_province_name(str(rd["xzqhdmSheng"])), city=get_city_name(str(rd["xzqhdmShi"])),
                                area=get_area_name(str(rd["xzqhdmQu"])), address=rd["txdz"], motto=name,
                                principal_name=name, principal_email=email_number, principal_phone=phone_number)
                logger.info(">>> Already add {}/{} school".format(index + 1, len(schools)))
                print(">>> Already add {}/{} school".format(index + 1, len(schools)))
                self.client.create_school(school)

                self.school_map[name] = rd["id"]
