import pymysql
import traceback
import requests
from config import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_CHARSET
from config import CALLBACK_PROTOCOL, CALLBACK_HOST, CALLBACK_PORT
from sync.clas import ClassSync
from sync.course import CourseSync
from sync.organization import OrganizationSync
from sync.semester import SemesterSync
from sync.teacher import TeacherSync
from sync.week import WeekSync
from sync.classroom import ClassroomSync
from utils.exceptions import SyncError
from utils.loggerutils import logging

logger = logging.getLogger(__name__)


class BaseWorker(object):
    @staticmethod
    def clear_data():
        pass

    @staticmethod
    def sync():
        pass

    @staticmethod
    def callback(result, message):
        if CALLBACK_PORT:
            url = "{}://{}:{}/labmgs/datasync/done".format(CALLBACK_PROTOCOL, CALLBACK_HOST, CALLBACK_PORT)
        else:
            url = "{}://{}/labmgs/datasync/done".format(CALLBACK_PROTOCOL, CALLBACK_HOST)
        params = {"message": message, "result": result}
        res = requests.get(url=url, params=params)
        try:
            res.raise_for_status()
        except (Exception,) as e:
            logger.info("error in {}".format(url))
            logger.error(traceback.print_exc())
            logger.info(res.text)
            logger.info("URL:{}, RES:{}".format(url, res.text))
            return None

    @classmethod
    def start(cls):
        try:
            cls.clear_data()
            cls.sync()
            cls.callback("success", "成功")
        except (SyncError,) as e:
            cls.callback("fail", e.message)
        except (Exception,) as e:
            logger.error(traceback.print_exc())


class SyncAllWorker(BaseWorker):
    @staticmethod
    def clear_data():
        logger.info("-------------Clear All Data In MYSQL--------------")
        try:
            conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD,
                                   db=MYSQL_DB, charset=MYSQL_CHARSET)
            cursor = conn.cursor()
            clear_table = ["labmgt.tbl_zf_course", "labmgt.tbl_zf_class", "labmgt.tbl_zf_classroom",
                           "labmgt.tbl_zf_semester", "labmgt.tbl_zf_user", "labmgt.tbl_zf_week",
                           "labmgt.tbl_zf_college"]
            for table in clear_table:
                sql = "DELETE FROM {}".format(table)
                rows = cursor.execute(sql)
            conn.commit()
            cursor.close()
            conn.close()
        except (Exception,):
            logger.error(traceback.print_exc())
            raise SyncError("ClearTableError")

    @staticmethod
    def sync():
        logger.info("-------------Start Sync All Flow--------------")
        sync_flow = [OrganizationSync, ClassSync, SemesterSync, WeekSync, TeacherSync, ClassroomSync, CourseSync]
        for sync_class in sync_flow:
            sync_obj = sync_class()
            sync_obj.start()
        logger.info("-------------Finish Sync All Flow--------------")


class SyncClassroomWorker(BaseWorker):
    @staticmethod
    def clear_data():
        logger.info("-------------Clear Classroom Data In MYSQL--------------")
        try:
            conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD,
                                   db=MYSQL_DB, charset=MYSQL_CHARSET)
            cursor = conn.cursor()
            clear_table = ["labmgt.tbl_zf_classroom"]
            for table in clear_table:
                sql = "DELETE FROM {}".format(table)
                rows = cursor.execute(sql)
                conn.commit()
            cursor.close()
            conn.close()
        except (Exception,):
            logger.error(traceback.print_exc())
            raise SyncError("ClearTableError")

    @staticmethod
    def sync():
        logger.info("-------------Start Sync Classroom Flow--------------")
        sync_flow = [ClassroomSync]
        for sync_class in sync_flow:
            sync_obj = sync_class()
            sync_obj.start()
        logger.info("-------------Finish Sync Classroom Flow--------------")
