import time
import traceback
from classcard_dataclient.client.action import DataClient, DataClientV1, DataClientV2
from config import SCHOOL_NAME
from requester.nice import NiceRequester
from config import NICE_HOST, NICE_PROTOCOL
from utils.loggerutils import logging

logger = logging.getLogger(__name__)


class BaseSync(object):
    def __init__(self, *args, **kwargs):
        self.school_id = None
        self.client = self.get_data_client()
        base_data = kwargs.pop("base_data", {})
        school_name = kwargs.pop("school_name", None)
        school_number = kwargs.pop("school_number", None)
        if school_name:
            code, school = self.client.get_school_by_name(school_name)
            if code:
                logger.error("Error: get school info, Detail: {}".format(school))
            self.school_id = school.get("uuid")
        self.nice_requester = NiceRequester(school_number, host=NICE_HOST, protocol=NICE_PROTOCOL, base_data=base_data)

    @staticmethod
    def get_data_client():
        return DataClient()

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


class BaseSync1(BaseSync):
    @staticmethod
    def get_data_client():
        return DataClientV1()


class BaseSync2(BaseSync):
    @staticmethod
    def get_data_client():
        return DataClientV2()
