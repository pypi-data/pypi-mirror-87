import os
import pymssql
import pymysql
import traceback

# SqlServer Config
SQLSERVER_HOST = os.getenv("SQLSERVER_HOST", "127.0.0.1")
SQLSERVER_USER = os.getenv("SQLSERVER_USER", "root")
SQLSERVER_PW = os.getenv("SQLSERVER_PW", "123456")
SQLSERVER_DB = os.getenv("SQLSERVER_DB", "db")

# MySQL Config
MYSQL_HOST = os.getenv("MYSQL_HOST", "10.88.188.229")
MYSQL_PORT = os.getenv("MYSQL_PORT", 13306)
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "nirvana")
MYSQL_DB = os.getenv("MYSQL_DB", "nirvana")
MYSQL_CHARSET = os.getenv("MYSQL_CHARSET", "utf8")


class BaseSync(object):

    @staticmethod
    def extract_data():
        print("-------------Extract Data From SQL SERVER--------------")
        class_list = []
        try:
            conn = pymssql.connect(server=SQLSERVER_HOST, user=SQLSERVER_USER, password=SQLSERVER_PW,
                                   database=SQLSERVER_DB)
            cur = conn.cursor()
            sql = "SELECT 所在班号, 所在班名称 FROM school_middle.班级列表"
            cur.execute(sql)
            rows = cur.fetchall()
            for row in rows:
                number, name = row[0], row[1]
                class_list.append({"number": number, "name": name})
            cur.close()
            conn.close()
        except (Exception,):
            print(traceback.print_exc())
        return class_list

    @staticmethod
    def transform_data(eds):
        return eds

    @staticmethod
    def load_data(tds):
        print("-------------Load Data To MYSQL--------------")
        try:
            conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD,
                                   db=MYSQL_DB, charset=MYSQL_CHARSET)
            cursor = conn.cursor()
            for td in tds:
                sql = "INSERT INTO labmgt.tbl_zf_class(class_no,class_name) " \
                      "VALUES('{}','{}')".format(td["number"], td["name"])
                rows = cursor.execute(sql)
            conn.commit()
            cursor.close()
            conn.close()
        except (Exception,):
            print(traceback.print_exc())

    def start(self):
        eds = self.extract_data()
        tds = self.transform_data(eds)
        self.load_data(tds)


if __name__ == '__main__':
    print("-------------Start--------------")
    sync = BaseSync()
    sync.start()
    print("-------------Finish--------------")
