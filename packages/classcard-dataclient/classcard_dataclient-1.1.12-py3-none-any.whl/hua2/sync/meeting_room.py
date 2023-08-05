import datetime
from sync.base import BaseSync
from utils.loggerutils import logging
from utils.code import get_md5_hash
from utils.dateutils import datetime2str, datetime2str_z, str2datetime, date2str
from classcard_dataclient.models.classroom import Classroom, RoomType
from classcard_dataclient.models.meeting_room import MeetingRoom, MeetingRoomRule
from classcard_dataclient.client.backbone import BackboneV2
from utils.cache import set_cache, get_cache_json

logger = logging.getLogger(__name__)


class MeetingRoomSync(BaseSync):
    def __init__(self):
        super(MeetingRoomSync, self).__init__()
        now = datetime.datetime.now()
        self.datetime_line = datetime2str(now)
        self.offset = 300
        self.place_appeared_number = []
        self.place_list = []
        self.meeting_map = {}
        self.host_map = {}
        self.meeting_user_map = {}
        self.meeting_room_list = []
        self.classroom_name_num = {}
        self.classroom_num_name = {}
        self.classroom_fullname_name = {}

    def get_double_map(self):
        double_number = {"1xx": ["1_A", "1_B"],
                         "2xx": ["2_A", "2_B"],
                         "3xx": ["3_A", "3_B"],
                         "4xx": ["4_A", "4_B"]}
        return double_number

    def extract_classroom_info(self):
        sql = "SELECT id, areaname, fullname, pid, levf FROM mid_areainfo ORDER BY levf"
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        for row in rows:
            external_id, name, fullname, parent_id, level = row[0], row[1], row[2], row[3], row[4]
            self.classroom_num_name[str(external_id)] = name
            self.classroom_name_num[name] = str(external_id)
            self.classroom_fullname_name[fullname] = name

    def extract_meeting_user(self):
        sql = "SELECT OutID, MeetNo FROM M_Meeting_Man_Out ORDER BY MeetNo"
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        for row in rows:
            user_num, meet_no = row[0], row[1]
            if meet_no not in self.meeting_user_map:
                self.meeting_user_map[meet_no] = set()
            self.meeting_user_map[meet_no].add(user_num)

    def extract_host_map(self):
        sql = "SELECT OUTID, NAME FROM BASE_CUSTOMERS ORDER BY OUTID"
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        for row in rows:
            number, name = row[0], row[1]
            self.host_map[number] = name

    def extract_meeting_room(self):
        sql = "SELECT MeetNo,MeetName,MeetContent,Moderator,PlaceID,PlaceName," \
              "StAfter,StBefore,EndAfter,PlanStart,PlanEnd " \
              "FROM M_Meeting_Info_Out WHERE StBefore > '{}' ORDER BY PlaceID".format(self.datetime_line)
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        double_number_map = self.get_double_map()
        for row in rows:
            meet_no, name, remarks, host_number = row[0], row[1], row[2], row[3]
            place_id, place_name, later_time = row[4], row[5], row[6]
            active_start, active_end = row[7], row[8]
            start_time, end_time = row[9], row[10]
            if place_name in self.classroom_name_num:
                place_id = self.classroom_name_num[place_name]
            else:
                place_id = "hy_{}".format(place_id)
            left_seconds = (start_time - active_start).seconds
            right_seconds = (active_end - end_time).seconds
            mid_seconds = (later_time - start_time).seconds
            left = -(left_seconds % 60 + left_seconds // 60)
            right = right_seconds % 60 + right_seconds // 60
            mid = mid_seconds % 60 + mid_seconds // 60
            classroom_numbers = double_number_map.get(place_id, [place_id])
            for classroom_number in classroom_numbers:
                place_num = self.add_meeting_place(place_name, number=classroom_number)
                host = self.host_map.get(host_number, None)
                meeting_room = MeetingRoom(name=name, host=host or "主持人", remarks=remarks, school=self.school_id,
                                           start_time=datetime2str_z(start_time), end_time=datetime2str_z(end_time),
                                           active_start=datetime2str_z(active_start),
                                           active_end=datetime2str_z(active_end),
                                           classroom_number=place_num, extra_info={"meet_no": meet_no})
                meeting_rule = MeetingRoomRule(left=left, right=right, mid=mid, school=self.school_id)
                meeting_room.rule = meeting_rule
                meeting_user = self.meeting_user_map.get(str(meet_no), [])
                meeting_room.user_numbers = list(meeting_user)
                if host:
                    meeting_room.user_numbers.append(host_number)
                self.meeting_room_list.append(meeting_room)

    def add_meeting_place(self, name, number=None):
        # number = get_md5_hash(name)
        if number not in self.place_appeared_number:
            self.place_appeared_number.append(number)
            classroom = Classroom(number=number, name=name, school=self.school_id, category=RoomType.TYPE_PUBLIC)
            self.place_list.append(classroom)
        return number

    def extract_meeting_place(self):
        sql = "SELECT PlaceID,PlaceName FROM M_Meeting_Place_Out ORDER BY PlaceID"
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        for row in rows:
            number, name = str(row[0]), row[1]
            number = get_md5_hash(name)
            if number not in self.place_appeared_number:
                self.place_appeared_number.append(number)
                classroom = Classroom(number=number, name=name, school=self.school_id, category=RoomType.TYPE_CLASS)
                self.place_list.append(classroom)

    def extract_multi_room(self):
        double_number_map = self.get_double_map()
        now = datetime.datetime.now()
        str_now = datetime2str(now)
        sql = "SELECT AreaName, AreaId, ApplyOutId,ApplyUserName, ApplyDate, StartDate, EndDate FROM bs_BookingApply " \
              "WHERE EndDate>='{}' AND ApplyStatusEnum=1 ORDER BY Id ".format(str_now)
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        for row in rows:
            place_name, place_id, host_number, host_name = row[0], row[1], row[2], row[3]
            apply_date, start_date, end_date = row[4], row[5], row[6]
            apply_date = str2datetime(apply_date[:19])
            start_date = str2datetime(start_date[:19])
            end_date = str2datetime(end_date[:19])
            # place_name = self.classroom_fullname_name.get(place_name)
            # if not place_name:
            #     continue
            classroom_numbers = double_number_map.get(place_id, [place_id])
            for classroom_number in classroom_numbers:
                place_num = self.add_meeting_place(place_name, number=classroom_number)
                host = self.host_map.get(host_number, None)
                name = "{}预约教室".format(host)
                current_date = start_date
                while True:
                    if current_date.date() > end_date.date():
                        break
                    if current_date.date() == start_date.date():
                        start_time = start_date
                    else:
                        start_time = "{} 00:00:00".format(date2str(current_date.date()))
                        start_time = str2datetime(start_time)
                    if current_date.date() == end_date.date():
                        if "00:00:00" in datetime2str(end_date):
                            break
                        end_time = end_date
                    else:
                        end_time = "{} 23:59:59".format(date2str(current_date.date()))
                        end_time = str2datetime(end_time)
                    if start_time <= now:
                        if apply_date.date() == now.date():
                            today_cache_key = "DGN_MR_{}_{}".format(place_num, date2str(now.date()))
                            is_create = get_cache_json(today_cache_key)
                            if is_create and is_create["result"]:
                                current_date = current_date + datetime.timedelta(days=1)
                                continue
                            else:
                                set_cache(today_cache_key, {"result": 1})
                        else:
                            current_date = current_date + datetime.timedelta(days=1)
                            continue
                    # current_end_date = start_date + datetime.timedelta(hours=23, minutes=59)
                    meeting_room = MeetingRoom(name=name, host=host or "主持人", remarks=name, school=self.school_id,
                                               start_time=datetime2str_z(start_time),
                                               end_time=datetime2str_z(end_time),
                                               active_start=datetime2str_z(start_time),
                                               active_end=datetime2str_z(end_time),
                                               classroom_number=place_num, extra_info={"meet_no": None})
                    if host:
                        meeting_room.user_numbers.append(host_number)
                    self.meeting_room_list.append(meeting_room)
                    current_date = current_date + datetime.timedelta(days=1)
                    # start_date = start_date + datetime.timedelta(days=1)

    def clear_finished_meeting_room(self):
        backbone = BackboneV2(self.school_id)
        finished_meeting_rooms = backbone.nirvana_requester.get_meeting_room_list(params={"state": 2})
        if finished_meeting_rooms:
            for f_room in finished_meeting_rooms.get("results", []):
                backbone.nirvana_requester.delete_meeting_room(f_room["uid"])

    def sync(self):
        self.clear_finished_meeting_room()
        self.extract_classroom_info()
        self.extract_host_map()
        self.extract_multi_room()
        self.extract_meeting_user()
        self.extract_meeting_room()
        if not self.place_list:
            logger.info("没有会议室信息")
            return
        self.client.create_classrooms(self.school_id, self.place_list)
        self.client.create_meeting_rooms(self.school_id, self.meeting_room_list)
        self.close_db()
