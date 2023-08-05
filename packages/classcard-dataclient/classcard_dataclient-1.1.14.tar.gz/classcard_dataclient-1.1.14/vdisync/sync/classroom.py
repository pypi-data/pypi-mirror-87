import traceback
from sync.base import BaseSync


class ClassroomSync(BaseSync):

    def __init__(self, *args, **kwargs):
        super(ClassroomSync, self).__init__(*args, **kwargs)

    def extract_data(self):
        sql = "SELECT CD_ID,CDMC,ZWS  FROM school_middle.dbo.JW_JCDM_CDJBXXB"
        self.sql_server_cur.execute(sql)
        rows = self.sql_server_cur.fetchall()
        for row in rows:
            room_number, name, terminal_amount = row[0], row[1], row[2] or 0
            pk = room_number
            if pk not in self.pk_list:
                self.pk_list.append(pk)
                self.ori_data.append({"room_number": room_number, "name": name, "terminal_amount": terminal_amount})

    def load_data(self):
        for td in self.new_data:
            try:
                sql = "INSERT INTO labmgt.tbl_zf_classroom(room_number,name,terminal_amount) " \
                      "VALUES('{}','{}','{}')".format(td["room_number"], td["name"], td["terminal_amount"])
                self.mysql_cur.execute(sql)
                self.mysql_conn.commit()
            except (Exception, ):
                print(traceback.print_exc())
