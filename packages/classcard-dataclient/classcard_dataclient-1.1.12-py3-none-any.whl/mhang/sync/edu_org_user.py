from sync import BaseSync
from classcard_dataclient.models.user import EduOrgUser, GenderSet
from utils.loggerutils import logging

logger = logging.getLogger(__name__)


class EduOrgUserSync(BaseSync):
    def sync(self):
        gender_map = {"1": GenderSet.MALE, "2": GenderSet.FEMALE}
        org_users = self.mh_requester.get_edu_org_user(self.mh_school_id)

        org_user_list = []
        for index, rd in enumerate(org_users):
            if str(rd["originIsDeleted"]) == "1":
                # 已删除的行政管理人员
                code, msg = self.client.delete_edu_org_user({"outer_id": rd['id']})
                logger.info(">>> delete org user {} result-{}-{}".format(rd['xm'], code, msg))
            else:
                org_user = EduOrgUser(number=rd['username'], name=rd['xm'], password="MTIzNDU2",
                                      description=rd['username'], email="{}@edt.com".format(rd['username']),
                                      birthday=rd['csrq'], phone=rd['yddh'], gender=gender_map.get(rd['xbm'], None),
                                      outer_id=rd['id'], job=rd['xzzumc'])
                org_user_list.append(org_user)
        code, data = self.client.create_edu_org_user(org_user_list)
        logger.info("Code: {}, Msg: {}".format(code, data))
