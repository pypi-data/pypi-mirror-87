import datetime
from sync.base import BaseSync
from utils.loggerutils import logging
from utils.dateutils import date2str
from utils.code import get_md5_hash
from classcard_dataclient.models.semester import SemesterV2
from classcard_dataclient.models.schedule import RestScheduleV2, RestTableV2, PeriodSet
from config import SCHOOL_SEASON, REST_TABLE_KEY1, REST_TABLE_KEY2, REST_TABLE_KEY3
from config import SUMMER_MORNING_LIMIT, SUMMER_AFTERNOON_LIMIT, WINTER_MORNING_LIMIT, WINTER_AFTERNOON_LIMIT
from utils.dateutils import str2datetime

logger = logging.getLogger(__name__)


class ScheduleSync(BaseSync):
    def __init__(self):
        super(ScheduleSync, self).__init__()
        self.offset = 300
        self.slot_map = {}
        self.semester = None
        self.rest_table = None
        self.rest_table_map = {}
        self.rest_table_slot = {}

    def wrap_time(self, ts):
        return "{}:00".format(ts) if len(ts) < 6 else ts

    def get_rest_table_map(self, semester_name):
        key_list = [REST_TABLE_KEY1, REST_TABLE_KEY2, REST_TABLE_KEY3]
        rest_table_map = {}
        for key in key_list:
            rest_table_name = "{}作息".format(key)
            rest_table = RestTableV2(name=rest_table_name, number=get_md5_hash(rest_table_name)[:20],
                                     semester_name=semester_name)
            self.rest_table_slot[rest_table_name] = []
            rest_table_map[key] = rest_table
        return rest_table_map

    def extract_rest_table(self, key, rest_table):
        slot_list = []
        ex_day = "2012-12-12 "
        time_limit_map = {"summer": {"morning": str2datetime(ex_day + SUMMER_MORNING_LIMIT),
                                     "afternoon": str2datetime(ex_day + SUMMER_AFTERNOON_LIMIT)},
                          "winter": {"morning": str2datetime(ex_day + WINTER_MORNING_LIMIT),
                                     "afternoon": str2datetime(ex_day + WINTER_AFTERNOON_LIMIT)}}
        time_com_map = {"summer": ("summerstart", "summerend", "summerstartbefore"),
                        "winter": ("winterstart", "winterend", "winterstartbefore")}
        time_com = time_com_map[SCHOOL_SEASON]
        time_limit = time_limit_map[SCHOOL_SEASON]
        sql = "SELECT id, sectionname, {}, {}, {}, ver, updateflag FROM mid_section " \
              "WHERE sectionname LIKE '{}%' ORDER BY {}" \
            .format(time_com[0], time_com[1], time_com[2], key, time_com[1])
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        num = 0
        for row in rows:
            slot_id, name, start_time, stop_time, pre_time, num_ver = row[0], row[1], row[2], row[3], row[4], row[5]
            start_time = self.wrap_time(start_time)
            stop_time = self.wrap_time(stop_time)
            pre_time = self.wrap_time(pre_time)
            datetime_format = str2datetime(ex_day + start_time)
            updateflag = row[6]
            if updateflag and str(updateflag) == "3":
                continue
            num += 1
            self.rest_table_slot[rest_table.name].append(slot_id)
            self.slot_map[slot_id] = num
            slot_list.append(slot_id)
            if datetime_format <= time_limit["morning"]:
                time_period = PeriodSet.MORNING
            elif datetime_format <= time_limit["afternoon"]:
                time_period = PeriodSet.AFTERNOON
            else:
                time_period = PeriodSet.EVENING
            for week in range(1, 8):
                schedule_data = {"name": name, "num": num, "order": num, "start_time": start_time,
                                 "stop_time": stop_time, "pre_time": pre_time}
                rest_schedule = RestScheduleV2(week=week, time_period=time_period, **schedule_data)
                rest_table.add_schedule(rest_schedule)

    def sync(self):
        begin_datetime = datetime.datetime.now()
        end_datetime = begin_datetime + datetime.timedelta(days=60)
        begin_date, end_date = date2str(begin_datetime.date()), date2str(end_datetime.date())
        semester = SemesterV2(name="当前学期", begin_date=begin_date, end_date=end_date,
                              number=get_md5_hash("当前学期")[:20])
        rest_table_map = self.get_rest_table_map(semester.name)
        # rest_table = RestTableV2(name="全校作息1", number=get_md5_hash("全校作息")[:20], semester_name=semester.name)
        for key, rest_table in rest_table_map.items():
            self.extract_rest_table(key, rest_table)
            print(">>> CREATE_REST_TABLE: {}".format(rest_table.name))
            logger.info(">>> CREATE_REST_TABLE: {}".format(rest_table.name))
            self.client.create_semester(self.school_id, semester)
            self.client.create_rest_table(self.school_id, rest_table, is_active=True)
            self.semester = semester
            self.rest_table = rest_table
        self.close_db()
