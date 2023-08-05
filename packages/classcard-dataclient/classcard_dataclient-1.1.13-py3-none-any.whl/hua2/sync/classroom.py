import datetime
from sync.base import BaseSync
from utils.loggerutils import logging
from utils.code import get_md5_hash
from classcard_dataclient.models.classroom import Classroom, RoomType

logger = logging.getLogger(__name__)


class ClassroomSync(BaseSync):
    def __init__(self):
        super(ClassroomSync, self).__init__()
        now = datetime.datetime.now()
        self.offset = 300
        self.appeared_number = []
        self.classroom_list = []
        self.classroom_map = {}
        self.name_num = {}
        self.building_map = {}
        self.building_list = set()
        self.fullname_section = {}

    def get_exist_classroom_map(self):
        exist_classroom_map = self.client.get_classroom_num_map(self.school_id)
        return exist_classroom_map

    def cleared_classroom(self):
        exist_classroom_map = self.get_exist_classroom_map()
        sql = "SELECT id, areaname, fullname, pid, levf FROM mid_areainfo WHERE updateflag='3' ORDER BY levf"
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        for row in rows:
            external_id, name, fullname, parent_id, level = row[0], row[1], row[2], row[3], row[4]
            number = str(external_id)
            classroom_id = exist_classroom_map.get(number)
            if classroom_id:
                self.client.delete_classroom(self.school_id, classroom_id)

    def extract_section_map(self):
        sql = "SELECT fullname, dpname FROM mid_term ORDER BY fullname"
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        for row in rows:
            fullname, dpname = row[0], row[1]
            self.fullname_section[fullname] = dpname

    def extract_building(self):
        sql = "SELECT id, areaname, fullname, pid, levf FROM mid_areainfo ORDER BY levf"
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        for row in rows:
            external_id, name, fullname, parent_id, level = row[0], row[1], row[2], row[3], row[4]
            self.building_map[external_id] = fullname
            self.building_list.add(parent_id)

    def extract_classroom(self):
        sql = "SELECT id, areaname, fullname, pid, levf FROM mid_areainfo WHERE updateflag='2' ORDER BY levf"
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        for row in rows:
            external_id, name, fullname, parent_id, level = row[0], row[1], row[2], row[3], row[4]
            if external_id in self.building_list:
                continue
            building = self.building_map.get(parent_id, None)
            # number = get_md5_hash(name)
            number = str(external_id)
            try:
                name_info = name.split("-")
                floor = name_info[-1][0] if len(name_info[-1]) <= 3 else name_info[-1][:2]
            except (Exception,):
                floor = None
            room_info_list = self.get_double_map(name, number)
            for room_info in room_info_list:
                self.add_classroom(room_info[0], room_info[1], fullname, building, floor)

    def add_classroom(self, name, number, fullname, building, floor):
        if name not in self.name_num:
            self.name_num[name] = number
            if building:
                building = building.split("/")[0]
            classroom = Classroom(number=number, name=name, building=building,
                                  floor=floor, school=self.school_id, category=RoomType.TYPE_PUBLIC)
            if fullname in self.fullname_section:
                classroom.category = RoomType.TYPE_CLASS
                classroom.section_name = self.fullname_section[fullname]
            self.classroom_list.append(classroom)
        self.classroom_map[number] = self.name_num[name]

    def get_double_map(self, name, number):
        double_sign = []
        if number in double_sign:
            room_a_name, room_a_number = "{}_A".format(name), "{}_A".format(number)
            room_b_name, room_b_number = "{}_B".format(name), "{}_B".format(number)
            return [(room_a_name, room_a_number), (room_b_name, room_b_number)]
        else:
            return [(name, number)]

    def sync(self):
        self.cleared_classroom()
        self.extract_building()
        self.extract_classroom()
        if not self.classroom_map:
            logger.info("没有教室信息")
            return
        # self.client.create_classrooms(self.school_id, self.classroom_list)
        self.close_db()
