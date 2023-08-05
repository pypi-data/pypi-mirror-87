import traceback
from sync.base import BaseSync


class TeacherSync(BaseSync):

    def __init__(self, *args, **kwargs):
        super(TeacherSync, self).__init__(*args, **kwargs)

    def extract_data(self):
        sql = "SELECT 工号,姓名,机构名称  FROM school_middle.dbo.教师数据"
        self.sql_server_cur.execute(sql)
        rows = self.sql_server_cur.fetchall()
        for row in rows:
            t_no, username, college_name = row[0], row[1], row[2]
            pk = t_no
            if pk not in self.pk_list:
                self.pk_list.append(pk)
                self.ori_data.append({"t_no": t_no, "username": username, "college_name": college_name})

    def load_data(self):
        for td in self.new_data:
            try:
                sql = "INSERT INTO labmgt.tbl_zf_user(t_no,username,college_name) " \
                      "VALUES('{}','{}','{}')".format(td["t_no"], td["username"], td["college_name"])
                self.mysql_cur.execute(sql)
                self.mysql_conn.commit()
            except (Exception, ):
                print(traceback.print_exc())
