import traceback
from sync.base import BaseSync
from utils.dateutils import date2str


class WeekSync(BaseSync):

    def __init__(self, *args, **kwargs):
        super(WeekSync, self).__init__(*args, **kwargs)

    def extract_data(self):
        sql = "SELECT yearNo,termNo,weekIndex,startDate,endDate  FROM school_middle.dbo.r_week"
        self.sql_server_cur.execute(sql)
        rows = self.sql_server_cur.fetchall()
        for row in rows:
            school_year, term_num, week_index, start_date, end_date = row[0], row[1], row[2], row[3], row[4]
            self.ori_data.append({"school_year": school_year, "term_num": term_num, "week_index": week_index,
                                  "start_date": date2str(start_date), "end_date": date2str(end_date)})

    def load_data(self):
        for td in self.new_data:
            try:
                sql = "INSERT INTO labmgt.tbl_zf_week(school_year,term_num,week_index,start_date,end_date) " \
                      "VALUES('{}','{}','{}','{}','{}')". \
                    format(td["school_year"], td["term_num"], td["week_index"], td["start_date"], td["end_date"])
                self.mysql_cur.execute(sql)
                self.mysql_conn.commit()
            except (Exception, ):
                print(traceback.print_exc())
