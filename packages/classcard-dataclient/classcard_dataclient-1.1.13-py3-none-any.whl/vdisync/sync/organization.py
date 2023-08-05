import traceback
from sync.base import BaseSync


class OrganizationSync(BaseSync):

    def __init__(self, *args, **kwargs):
        super(OrganizationSync, self).__init__(*args, **kwargs)

    def extract_data(self):

        sql = "SELECT 机构号,机构名称 FROM school_middle.dbo.机构表"
        self.sql_server_cur.execute(sql)
        rows = self.sql_server_cur.fetchall()
        for row in rows:
            number, name = row[0], row[1]
            pk = number
            if pk not in self.pk_list:
                self.pk_list.append(pk)
                self.ori_data.append({"number": number, "name": name})

    def load_data(self):
        for td in self.new_data:
            try:
                sql = "INSERT INTO labmgt.tbl_zf_college(college_no,college_name) " \
                      "VALUES('{}','{}')".format(td["number"], td["name"])
                self.mysql_cur.execute(sql)
                self.mysql_conn.commit()
            except (Exception, ):
                print(traceback.print_exc())
