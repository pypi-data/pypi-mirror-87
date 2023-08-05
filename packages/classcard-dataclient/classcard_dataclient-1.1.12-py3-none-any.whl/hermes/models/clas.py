from models.base import ExtraBaseModel, ExtraCoreModel
from peewee import CharField, ForeignKeyField, TextField, IntegerField, SmallIntegerField, ManyToManyField
from models.role import Teacher, Student


class Class(ExtraBaseModel):
    name = CharField(verbose_name="班级名称", max_length=64)
    teacher = ForeignKeyField(Teacher, to_field="uid", verbose_name="班主任", backref="section",
                              blank=True, null=True)
    num = IntegerField(verbose_name="班级编号", default=11901)
    description = TextField(verbose_name="简介", null=True)
    declaration = TextField(verbose_name="班级宣言", null=True)
    slogan = CharField(verbose_name="班级口号", max_length=256, blank=True, null=True)
    entrance = SmallIntegerField(verbose_name="级", null=True)  # 2018
    export = SmallIntegerField(verbose_name="届", null=True)  # 2018
    student = ManyToManyField(Student, through_model='ClassMember', backref="section")
    category = SmallIntegerField(verbose_name="类型, 0 行政班 1 其他班", default=0)  # 0 课程 1 其他
    grade = CharField(verbose_name="年级名称", max_length=64, default="NA")
    education = CharField(verbose_name="学历", max_length=64, default="NA")


class ClassMember(ExtraCoreModel):
    position = CharField(verbose_name="职位", max_length=32, blank=True, null=True)  # 班长
    student = ForeignKeyField(Student, to_field="uid", verbose_name="学生", blank=True, null=True)
    clas = ForeignKeyField(Class, to_field="uid", verbose_name="班级号", blank=True, null=True)
