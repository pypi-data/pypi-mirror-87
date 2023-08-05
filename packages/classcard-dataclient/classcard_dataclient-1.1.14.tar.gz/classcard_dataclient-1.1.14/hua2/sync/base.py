import time
import datetime
import traceback
import pymssql
from classcard_dataclient.client.action import DataClientV2
from config import SCHOOL_NAME
from utils.dateutils import date2str
from utils.loggerutils import logging
from config import SQLSERVER_HOST, SQLSERVER_USER, SQLSERVER_PW, SQLSERVER_DB

logger = logging.getLogger(__name__)


class BaseSync(object):
    def __init__(self):
        self.get_date_range()
        self.client = DataClientV2()
        code, school = self.client.get_school_by_name(SCHOOL_NAME)
        if code:
            logger.error("Error: get school info, Detail: {}".format(school))
        self.school_id = school.get("uuid")
        self.db = pymssql.connect(server=SQLSERVER_HOST, user=SQLSERVER_USER, password=SQLSERVER_PW,
                                  database=SQLSERVER_DB)
        self.cur = self.db.cursor()

    def get_date_range(self, days=7):
        now = datetime.datetime.now()
        now_weekday = now.weekday()
        first_datetime = now - datetime.timedelta(days=now_weekday)
        last_datetime = now + datetime.timedelta(days=6 - now_weekday)
        first_day, last_day = date2str(first_datetime.date()), date2str(last_datetime.date())
        return first_day, last_day

    @NotImplementedError
    def sync(self):
        pass

    def close_db(self):
        self.cur.close()
        self.db.close()

    def start(self):
        try:
            logger.info(">>> Start {} On:".format(self.__class__.__name__, datetime.datetime.now()))
            self.sync()
        except (Exception,):
            logger.error(">>> Error: sync error, Detail: {}".format(traceback.print_exc()))
            time.sleep(10)
        finally:
            logger.info(">>> Finish {} On:".format(self.__class__.__name__, datetime.datetime.now()))
