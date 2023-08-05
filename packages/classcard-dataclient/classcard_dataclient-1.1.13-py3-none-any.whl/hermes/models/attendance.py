from models import BaseSet
from models.base import ExtraBaseModel
from peewee import ForeignKeyField, CharField, SmallIntegerField, DateTimeField, DateField, TimeField, BooleanField
from models.subject import Subject
from models.classroom import Classroom
from models.role import Student, Teacher


class AttendanceStatus(BaseSet):
    STATUS_NO_SIGN = 1
    STATUS_ABSENCE = 2
    STATUS_ATTENDANCE = 3
    STATUS_LATER = 4
    STATUS_EARLIER = 5

    MESSAGE = {
        STATUS_NO_SIGN: "未打卡",
        STATUS_ABSENCE: "请假",
        STATUS_ATTENDANCE: "正常出勤",
        STATUS_LATER: '迟到',
        STATUS_EARLIER: '早退',
    }


class AttendanceType(BaseSet):
    TYPE_DEFAULT = 0
    TYPE_ECARD = 1
    TYPE_FACE = 2
    TYPE_AUTO = 3
    TYPE_QR = 4

    MESSAGE = {
        TYPE_DEFAULT: "默认",
        TYPE_ECARD: "一卡通",
        TYPE_FACE: "人脸打卡",
        TYPE_AUTO: "自动打卡",
        TYPE_QR: "二维码扫码"
    }


class BaseAttendance(ExtraBaseModel):
    category = SmallIntegerField(verbose_name="打卡类型, {}".format(AttendanceType.MESSAGE),
                                 default=AttendanceType.TYPE_DEFAULT)
    record_time = DateTimeField(verbose_name="打卡时间", null=True, default=None)
    record_image = CharField(verbose_name="考勤照片URL", max_length=256, blank=True, null=True)
    record_date = DateField(verbose_name="考勤日期", null=True, default=None)
    name = CharField(verbose_name="课表项名称", max_length=32, null=True, default=None)
    num = SmallIntegerField(verbose_name="序号", null=True, default=None)
    week = SmallIntegerField(verbose_name="星期", null=True, default=None)
    pre_time = TimeField(verbose_name="签到开始时间", null=True, default=None)
    start_time = TimeField(verbose_name="开始时间", null=True, default=None)
    stop_time = TimeField(verbose_name="结束时间", null=True, default=None)
    subject = ForeignKeyField(Subject, to_field="uid", verbose_name="学科",
                              blank=True, null=True, default=None)

    is_later = BooleanField(default=False, verbose_name='is_late')
    is_attendance = BooleanField(default=False, verbose_name='is_attendance')
    is_earlier = BooleanField(default=False, verbose_name='is_earlier')
    is_absence = BooleanField(default=False, verbose_name='is_absence')
    is_filed = BooleanField(default=False, verbose_name='是否归档')
    model = SmallIntegerField(default=0, verbose_name='考勤模式, 0.取第一次数据, 1.取最后一次打卡数据')
    schedule_category = SmallIntegerField(default=0, verbose_name='作息类型')
    status = SmallIntegerField(verbose_name="考勤状态, {}".format(AttendanceStatus.MESSAGE),
                               choices=AttendanceStatus.choices(),
                               default=AttendanceStatus.STATUS_NO_SIGN)  # 教室类型
    enable = BooleanField(verbose_name='enable', default=True)


class Attendance(BaseAttendance):
    student = ForeignKeyField(Student, backref='attendance', to_field="uid", verbose_name="学生",
                              blank=True, null=True)

    teacher = ForeignKeyField(Teacher, to_field="uid", verbose_name="老师", backref="attendance",
                              blank=True, null=True, default=None)
    classroom = ForeignKeyField(Classroom, to_field="uid", verbose_name="教室", backref="attendance",
                                blank=True, null=True)


class TeacherAttendance(BaseAttendance):
    teacher = ForeignKeyField(Teacher, to_field="uid", verbose_name="老师", backref="teacher_attendance",
                              blank=True, null=True, default=None)
    classroom = ForeignKeyField(Classroom, to_field="uid", verbose_name="教室", backref="teacher_attendance",
                                blank=True, null=True)
