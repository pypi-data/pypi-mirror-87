import traceback
import datetime
import logging
from sync.base import BaseSync
from utils.dateutils import date2str

logger = logging.getLogger(__name__)


class CourseSync(BaseSync):

    def __init__(self, *args, **kwargs):
        super(CourseSync, self).__init__(*args, **kwargs)
        self.course_student_count = {}
        self.classroom_map = {}

    def get_classroom_map(self, year_no, term_no):
        term_no_map = {1: 12, 0: 3}
        sql = "SELECT ZCD,XQJ,JCS,JGH_ID,CD_ID FROM school_middle.dbo.JSKB_SJBZK " \
              "WHERE XNM='{}' and XQM='{}'".format(year_no, term_no_map.get(term_no, term_no))
        self.sql_server_cur.execute(sql)
        rows = self.sql_server_cur.fetchall()
        for row in rows:
            week_index, week, period, user_t_no, room_number = row[0], row[1], row[2], row[3], row[4]
            room_key = (week_index, week, period, user_t_no)
            self.classroom_map[room_key] = room_number

    def get_current_semester(self):
        year_no, term_no = None, None
        today = datetime.datetime.now().date()
        str_today = date2str(today)
        sql = "SELECT yearNo,termNo,startDate,endDate,statusNo  FROM school_middle.dbo.r_term " \
              "WHERE statusNo='on'"
        self.sql_server_cur.execute(sql)
        rows = self.sql_server_cur.fetchall()
        for row in rows:
            year_no, term_no = row[0], row[1]
        return year_no, term_no

    def count_student(self, year_no, term_no):
        sql = "SELECT COUNT(DISTINCT 学号),教学班ID FROM school_middle.dbo.学生课表 " \
              "WHERE 学年码='{}' and 学期码='{}' GROUP BY 教学班ID".format(year_no, term_no)
        self.sql_server_cur.execute(sql)
        rows = self.sql_server_cur.fetchall()
        for row in rows:
            student_count, course_code = row[0], row[1]
            self.course_student_count[course_code] = student_count

    def extract_data(self):
        year_no, term_no = self.get_current_semester()
        self.get_classroom_map(year_no, term_no)
        self.count_student(year_no, term_no)
        sql = "SELECT 教工号,学年码,学期码,教学班ID,教学班名称,课程号,课程名称,周次,星期,节次数  " \
              "FROM school_middle.dbo.教师课表 WHERE 学年码='{}' and 学期码='{}'".format(year_no, term_no)
        self.sql_server_cur.execute(sql)
        rows = self.sql_server_cur.fetchall()
        for row in rows:
            user_t_no, school_year, term_num = row[0], row[1], row[2]
            class_num, class_name, course_code, course_name = row[3], row[4], row[5], row[6]
            week_index, week, period = row[7], row[8], row[9]
            room_key = (week_index, week, period, user_t_no)
            room_number = self.classroom_map.get(room_key, "")
            pk = (course_code, school_year, term_num, class_name, user_t_no, week_index, week, period, room_number)
            if pk not in self.pk_list:
                self.pk_list.append(pk)
                self.ori_data.append({"user_t_no": user_t_no, "school_year": school_year, "term_num": term_num,
                                      "class_num": class_num, "class_name": class_name, "course_code": course_code,
                                      "course_name": course_name, "classroom_number": room_number,
                                      "week_index": week_index, "week": week, "period": period})

    def transform_data(self):
        for od in self.ori_data:
            od["student_count"] = self.course_student_count.get(od["course_code"], 0)
            self.new_data.append(od)

    def load_data(self):
        for td in self.new_data:
            try:
                sql = "INSERT INTO labmgt.tbl_zf_course(course_code,school_year,term_num,class_name,user_t_no," \
                      "week_index,week,period,classroom_number,course_name,student_count) " \
                      "VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                    td["course_code"], td["school_year"], td["term_num"], td["class_name"], td["user_t_no"],
                    td["week_index"], td["week"], td["period"], td["classroom_number"], td["course_name"],
                    td["student_count"])
                self.mysql_cur.execute(sql)
                self.mysql_conn.commit()
            except (Exception,):
                print(traceback.print_exc())
