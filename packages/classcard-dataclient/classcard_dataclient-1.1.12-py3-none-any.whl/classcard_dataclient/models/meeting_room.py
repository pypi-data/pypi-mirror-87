from ..models.base import BaseModel


class AttendanceCategory(object):
    ATTENDANCE_TYPE_LATER = 1
    ATTENDANCE_TYPE_NORMAL = 2

    MESSAGE = {
        ATTENDANCE_TYPE_LATER: "迟到模式",
        ATTENDANCE_TYPE_NORMAL: "签到模式",
    }


class RoomType(object):
    TYPE_CLASS = 1
    TYPE_PUBLIC = 2

    MESSAGE = {
        TYPE_CLASS: "班级教室",
        TYPE_PUBLIC: "公共教室",
    }


class MeetingRoom(BaseModel):
    def __init__(self, *args, **kwargs):
        self.uid = ""
        self.name = ""
        self.host = ""
        self.remarks = None
        self.start_time = None
        self.end_time = None
        self.active_start = None
        self.active_end = None
        self.attendance = True
        self.is_active = True
        self.extra_info = {}
        self.school = None
        self.classroom_number = None
        self.rule = None
        self.user_numbers = []
        super(MeetingRoom, self).__init__(*args, **kwargs)
        self.classroom_id = None
        self.user = []
        self.required_filed = ["name", "classroom_number", "start_time", "end_time", "active_start", "active_end"]

    def add_user(self, user_number):
        if user_number not in self.user_numbers:
            self.user_numbers.append(user_number)

    @property
    def nirvana_data(self):
        self.extra_info["attendance"] = self.attendance
        data = {"name": self.name,
                "host": self.host,
                "remarks": self.remarks,
                "start_time": self.start_time,
                "end_time": self.end_time,
                "active_start": self.active_start,
                "active_end": self.active_end,
                "is_active": self.is_active,
                "school": self.school,
                "classroom": {"uid": self.classroom_id},
                "extra_info": self.extra_info}
        return data

    @property
    def nirvana_rule_data(self):
        if self.rule:
            self.rule.school = self.school
            self.rule.meeting = self.uid
            return self.rule.nirvana_data
        return None

    def get_user_data(self, current_user=None):
        current_user = current_user or []
        if self.user is not None:
            new_user = list(filter(lambda u: u not in current_user, self.user))
            delete_user = list(filter(lambda u: u not in self.user, current_user))
            data = {"new_user": new_user, "delete_user": delete_user}
            return data
        return None


class MeetingRoomRule(BaseModel):
    def __init__(self, *args, **kwargs):
        self.category = AttendanceCategory.ATTENDANCE_TYPE_NORMAL
        self.level = 1
        self.left = -15
        self.mid = 15
        self.right = 0
        self.enable = True
        self.meeting = None
        self.school = None
        super(MeetingRoomRule, self).__init__(*args, **kwargs)
        self.required_filed = []

    @property
    def nirvana_data(self):
        data = {"category": self.category,
                "level": self.level,
                "left": int(self.left),
                "mid": int(self.mid),
                "right": int(self.right),
                "enable": self.enable,
                "meeting": self.meeting,
                "school": self.school}
        return data
