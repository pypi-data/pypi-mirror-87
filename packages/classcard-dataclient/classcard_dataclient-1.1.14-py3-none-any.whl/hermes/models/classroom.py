import json
from models import BaseSet
from models.base import ExtraBaseModel
from peewee import CharField, SmallIntegerField, ForeignKeyField, TextField
from models.device import ClassDevice
from models.clas import Class


class RoomType(BaseSet):
    TYPE_CLASS = 1
    TYPE_PUBLIC = 2

    MESSAGE = {
        TYPE_CLASS: "班级教室",
        TYPE_PUBLIC: "公共教室",
    }


class ModeType(BaseSet):
    MODE_COMMON = 1
    MODE_EMERGENCY = 2
    MODE_EXAM = 3
    MODE_MEETING = 4
    MODE_VIDEO = 5

    MESSAGE = {
        MODE_COMMON: "普通模式",
        MODE_EMERGENCY: "通知模式",
        MODE_EXAM: "考试模式",
        MODE_MEETING: '会议模式',
        MODE_VIDEO: '视频模式',
    }


class Classroom(ExtraBaseModel):
    name = CharField(max_length=64, verbose_name="教室名称")  # 教室名称
    category = SmallIntegerField(choices=RoomType.choices(), default=RoomType.TYPE_CLASS,
                                 verbose_name="教室类型, {}".format(RoomType.MESSAGE))  # 教室类型
    seats = SmallIntegerField(default=1, verbose_name="教室座位数")  # 教室座位数
    num = CharField(db_index=True, blank=True, null=True, max_length=64, verbose_name="教室编号")
    building = CharField(db_index=True, max_length=10, blank=True, null=True, verbose_name="楼号")  #
    floor = CharField(db_index=True, max_length=10, blank=True, null=True, verbose_name="楼层")  #
    device = ForeignKeyField(ClassDevice, to_field="uid", backref="classroom", blank=True,
                             null=True, verbose_name="班牌")
    section = ForeignKeyField(Class, to_field="uid", backref="classroom", blank=True,
                              null=True, verbose_name="班级")
    mode = SmallIntegerField(choices=ModeType.choices(), default=ModeType.MODE_COMMON,
                             verbose_name="模式: {}".format(ModeType.MESSAGE))
    extra_info = TextField(null=True, verbose_name="额外信息")

    @property
    def extra(self):
        try:
            extra = json.loads(self.extra_info)
        except (Exception,):
            extra = {}
        extra["manager"] = extra.get("manager", "")
        extra["sensor_sn"] = extra.get("sensor_sn", None)
        extra["camera"] = extra.get("camera", [])
        return extra
