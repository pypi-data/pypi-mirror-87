import pymssql
import pymysql
import traceback
from config import SQLSERVER_HOST, SQLSERVER_USER, SQLSERVER_PW, SQLSERVER_DB, SQLSERVER_PORT
from config import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_CHARSET
from utils.exceptions import SyncError
from utils.loggerutils import logging

logger = logging.getLogger(__name__)


class BaseSync(object):
    def __init__(self, *args, **kwargs):
        self.sql_server_conn = pymssql.connect(server=SQLSERVER_HOST, user=SQLSERVER_USER, password=SQLSERVER_PW,
                                               database=SQLSERVER_DB, port=SQLSERVER_PORT)
        self.sql_server_cur = self.sql_server_conn.cursor()
        self.mysql_conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD,
                                          db=MYSQL_DB, charset=MYSQL_CHARSET)
        self.mysql_cur = self.mysql_conn.cursor()
        self.ori_data = []
        self.new_data = []
        self.pk_list = []

    def extract_data(self):
        pass

    def transform_data(self):
        self.new_data = self.ori_data

    def load_data(self):
        pass

    def start(self):
        try:
            logger.info("-------------{} Extract Data From SQL SERVER--------------".format(self.__class__.__name__))
            self.extract_data()
            logger.info("-------------{} Transform Data--------------".format(self.__class__.__name__))
            self.transform_data()
            logger.info("-------------{} Load Data To MYSQL--------------".format(self.__class__.__name__))
            self.load_data()
        except (Exception,):
            logger.error(traceback.print_exc())
            raise SyncError("{}SyncError".format(self.__class__.__name__))
        finally:
            self.sql_server_cur.close()
            self.sql_server_conn.close()
            self.mysql_cur.close()
            self.mysql_conn.close()
