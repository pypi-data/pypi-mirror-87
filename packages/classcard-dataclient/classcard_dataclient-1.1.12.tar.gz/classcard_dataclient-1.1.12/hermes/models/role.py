from models import BaseSet
from models.base import ExtraBaseModel
from peewee import ForeignKeyField, UUIDField, CharField, SmallIntegerField, DateField
from models.school import School
from models.device import CardDevice


class GenderSet(BaseSet):
    MALE = 'M'
    FEMALE = 'F'
    UNKNOWN = 'U'

    MESSAGE = {
        MALE: "男",
        FEMALE: "女",
        UNKNOWN: "未知",
    }


class Teacher(ExtraBaseModel):
    user = UUIDField(verbose_name="账号", unique=True, null=True)
    number = CharField(verbose_name="职工号", db_index=True, max_length=20)
    entrance = SmallIntegerField(verbose_name="级", null=True)  # 2018
    school = ForeignKeyField(School, to_field="uid", verbose_name="学校", backref='teacher', null=True)
    ecard = ForeignKeyField(CardDevice, to_field="uid", verbose_name="一卡通", backref='teacher', null=True)
    birthday = DateField(verbose_name="生日", blank=True, null=True)
    name = CharField(verbose_name="姓名", max_length=64)
    gender = CharField(verbose_name="性别", max_length=2, choices=GenderSet.choices(), default=GenderSet.UNKNOWN)
    face = CharField(verbose_name="人脸识别图像", max_length=128, blank=True, null=True)
    phone = CharField(verbose_name="电话", max_length=20, blank=True, null=True)
    description = CharField(verbose_name="简介", max_length=1024, blank=True, null=True)
    face_code = CharField(verbose_name="人脸识别码", max_length=128, blank=True, null=True)


class Student(ExtraBaseModel):
    user = UUIDField(verbose_name="账号", unique=True, null=True)
    number = CharField(verbose_name="职工号", db_index=True, max_length=20)
    entrance = SmallIntegerField(verbose_name="级", null=True)  # 2018
    school = ForeignKeyField(School, to_field="uid", verbose_name="学校", backref='teacher', null=True)
    ecard = ForeignKeyField(CardDevice, to_field="uid", verbose_name="一卡通", backref='teacher', null=True)
    birthday = DateField(verbose_name="生日", blank=True, null=True)
    name = CharField(verbose_name="姓名", max_length=64)
    gender = CharField(verbose_name="性别", max_length=2, choices=GenderSet.choices(), default=GenderSet.UNKNOWN)
    face = CharField(verbose_name="人脸识别图像", max_length=128, blank=True, null=True)
    phone = CharField(verbose_name="电话", max_length=20, blank=True, null=True)
    description = CharField(verbose_name="简介", max_length=1024, blank=True, null=True)
    face_code = CharField(verbose_name="人脸识别码", max_length=128, blank=True, null=True)
