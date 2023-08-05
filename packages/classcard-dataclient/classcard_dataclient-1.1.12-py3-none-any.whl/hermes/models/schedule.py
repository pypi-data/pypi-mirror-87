from models import BaseSet
from models.base import ExtraBaseModel
from peewee import CharField, SmallIntegerField, TextField, BooleanField, ForeignKeyField, TimeField


class PeriodSet(BaseSet):
    MORNING = "morning"
    NOON = "noon"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    NIGHT = "night"

    MESSAGE = {
        MORNING: "上午",
        NOON: "中午",
        AFTERNOON: "下午",
        EVENING: "晚上",
        NIGHT: "午夜",
    }


class RestTable(ExtraBaseModel):
    name = CharField(verbose_name="名称", max_length=64)  # 作息表名称
    number = CharField(verbose_name="助记码", max_length=20, blank=True, null=True)  # 作息表编号
    category = SmallIntegerField(verbose_name="类型", default=0)  # 0 单周 1 双周
    description = TextField(verbose_name="简介", null=True)
    is_active = BooleanField(verbose_name="是否生效", default=False)


class RestSchedule(ExtraBaseModel):
    rest_table = ForeignKeyField(RestTable, backref='schedule', to_field="uid", verbose_name="作息表",
                                 blank=True, null=True)
    category = SmallIntegerField(verbose_name="类型", default=0)  # 0 课程 1 其他
    name = CharField(verbose_name="课表项名称", max_length=64)
    num = SmallIntegerField(verbose_name="课程序号", default=0)
    order = SmallIntegerField(verbose_name="作息序号, 1-n", default=0)
    week = SmallIntegerField(verbose_name="星期, 1-7,8-14")
    pre_time = TimeField(verbose_name="签到开始时间基线, 00:00:00")
    pre_start_time = TimeField(verbose_name="迟到时间基线, 00:00:00", blank=True, null=True)
    pre_stop_time = TimeField(verbose_name="终止签到时间基线, 00:00:00", blank=True, null=True)
    start_time = TimeField(verbose_name="开始时间, 00:00:00")
    stop_time = TimeField(verbose_name="结束时间, 00:00:00")
    time_period = CharField(verbose_name="时间标签, str(20), {}".format(PeriodSet.MESSAGE),
                            choices=PeriodSet.choices(), default=PeriodSet.MORNING, max_length=20)
