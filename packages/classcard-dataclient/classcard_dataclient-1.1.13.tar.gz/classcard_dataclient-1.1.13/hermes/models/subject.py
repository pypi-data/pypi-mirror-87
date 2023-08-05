from models.base import ExtraBaseModel
from peewee import CharField


class Subject(ExtraBaseModel):
    name = CharField(verbose_name="学科名称", max_length=64)
    num = CharField(verbose_name="学科编号", blank=True, null=True, max_length=64)
