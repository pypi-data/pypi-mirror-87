from models import CoreModel, ExtraCoreModel
from models.school import School
from peewee import ForeignKeyField, CharField


class BaseModel(CoreModel):
    school = ForeignKeyField(School, to_field="uid", blank=True, null=True, verbose_name="学校")


class ExtraBaseModel(ExtraCoreModel):
    school = ForeignKeyField(School, to_field="uid", blank=True, null=True, verbose_name="学校")


class NameBaseModel(BaseModel):
    name = CharField(max_length=64, db_index=True, verbose_name="名称")


class NameExtraBaseModel(ExtraBaseModel):
    name = CharField(max_length=64, db_index=True, verbose_name="名称")
