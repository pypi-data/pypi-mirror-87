import traceback
from sync.base import BaseSync
from utils.dateutils import date2str


class SemesterSync(BaseSync):

    def __init__(self, *args, **kwargs):
        super(SemesterSync, self).__init__(*args, **kwargs)

    def extract_data(self):
        sql = "SELECT yearNo,termNo,startDate,endDate,statusNo  FROM school_middle.dbo.r_term"
        self.sql_server_cur.execute(sql)
        rows = self.sql_server_cur.fetchall()
        for row in rows:
            school_year, term_num, start_date, end_date = row[0], row[1], row[2], row[3]
            pk = (school_year, term_num)
            if pk not in self.pk_list:
                self.pk_list.append(pk)
                self.ori_data.append({"school_year": school_year, "term_num": term_num,
                                      "start_date": date2str(start_date), "end_date": date2str(end_date)})

    def load_data(self):
        for td in self.new_data:
            try:
                sql = "INSERT INTO labmgt.tbl_zf_semester(school_year,term_num,start_date,end_date) " \
                      "VALUES('{}','{}','{}','{}')". \
                    format(td["school_year"], td["term_num"], td["start_date"], td["end_date"])
                self.mysql_cur.execute(sql)
                self.mysql_conn.commit()
            except (Exception, ):
                print(traceback.print_exc())
