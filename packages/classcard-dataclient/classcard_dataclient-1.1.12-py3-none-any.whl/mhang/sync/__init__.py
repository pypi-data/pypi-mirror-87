import time
import traceback
from classcard_dataclient.client.action import DataClientV3
from requester.mhang import MhEdu
from utils.loggerutils import logging

logger = logging.getLogger(__name__)


class BaseSync(object):
    def __init__(self, *args, **kwargs):
        self.client = self.get_data_client()
        self.school_id = None
        # base_data = kwargs.pop("base_data", {})
        school_name = kwargs.pop("school_name", None)
        # 闵行教育局旗下学校id
        self.mh_school_id = kwargs.pop("mh_school_id", None)
        if school_name:
            code, school = self.client.get_school_by_name(school_name)
            if code:
                logger.error("Error: get school info, Detail: {}".format(school))
            # 对应我们系统的学校id
            self.school_id = school.get("uuid")
        self.mh_requester = MhEdu()

    @staticmethod
    def get_data_client():
        return DataClientV3()

    @NotImplementedError
    def sync(self):
        pass

    def start(self):
        print(">>> Start {}".format(self.__class__.__name__))
        logger.info(">>> Start {}".format(self.__class__.__name__))
        try:
            self.sync()
        except (Exception,):
            logger.error("Error: sync error, Detail: {}".format(traceback.print_exc()))
            time.sleep(10)
        print(">>> Finish {}".format(self.__class__.__name__))
        logger.info(">>> Finish {}".format(self.__class__.__name__))

