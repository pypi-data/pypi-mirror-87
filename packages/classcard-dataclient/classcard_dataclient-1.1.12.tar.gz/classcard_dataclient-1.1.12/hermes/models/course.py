from models.base import ExtraBaseModel, ExtraCoreModel
from peewee import CharField, SmallIntegerField, BooleanField, ForeignKeyField, ManyToManyField
from models.subject import Subject
from models.role import Teacher, Student
from models.classroom import Classroom
from models.clas import Class


class CourseTableManager(ExtraBaseModel):
    name = CharField(verbose_name="名称", max_length=64)  # 课程表名称
    number = CharField(verbose_name="助记码", max_length=20, blank=True, null=True)  # 课程表编号
    category = SmallIntegerField(verbose_name="类型, 0 单周 1 双周", default=0)  # 0 单周 1 双周
    description = CharField(verbose_name='简介', max_length=2048, blank=True, null=True)
    is_active = BooleanField(verbose_name='是否生效', default=False)


class Course(ExtraBaseModel):
    manager = ForeignKeyField(CourseTableManager, backref='course', to_field="uid", verbose_name="课程管理",
                              blank=True, null=True)
    subject = ForeignKeyField(Subject, to_field="uid", verbose_name="学科",
                              blank=True, null=True)
    num = CharField(verbose_name="课程编号", db_index=True, blank=True, null=True, max_length=64)
    name = CharField(verbose_name="课表项名称", max_length=64, blank=True, null=True)
    teacher = ForeignKeyField(Teacher, to_field="uid", verbose_name="老师", backref="course",
                              blank=True, null=True)
    class_hours = SmallIntegerField(verbose_name="课时", default=0, null=True)

    is_walking = BooleanField(verbose_name='是否走班', default=True)
    is_present = BooleanField(verbose_name='是否考勤', default=True)
    section = ForeignKeyField(Class, to_field="uid", verbose_name="班级", backref="course",
                              blank=True, null=True)
    student = ManyToManyField(Student, through_model='CourseMember', backref="course")
    classroom = ForeignKeyField(Classroom, to_field="uid", verbose_name="教室", backref="course",
                                blank=True, null=True)


class CourseMember(ExtraCoreModel):
    course = ForeignKeyField(Course, to_field="uid", verbose_name="课程",
                             blank=True, null=True)
    student = ForeignKeyField(Student, to_field="uid", verbose_name="学生",
                              blank=True, null=True)


class CourseTable(ExtraBaseModel):
    manager = ForeignKeyField(CourseTableManager, backref='item', to_field="uid", verbose_name="课程表",
                              blank=True, null=True)
    num = SmallIntegerField(verbose_name="序号, 1-n")
    week = SmallIntegerField(verbose_name="星期, 1-7")
    course = ForeignKeyField(Course, to_field="uid", verbose_name="课程， uid", backref="course_table",
                             blank=True, null=True)
