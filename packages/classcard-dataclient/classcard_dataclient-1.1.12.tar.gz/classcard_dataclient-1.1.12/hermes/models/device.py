from models.base import ExtraBaseModel
from peewee import CharField, TextField


class ClassDevice(ExtraBaseModel):
    sn = CharField(max_length=64, db_index=True, verbose_name="序列号")  # 班牌的sn号
    model = CharField(max_length=32, blank=True, null=True, verbose_name="型号")  # 班牌的型号
    mac = CharField(max_length=17, blank=True, null=True, verbose_name="mac地址")
    ip = CharField(blank=True, null=True, verbose_name="ip地址")
    version = CharField(max_length=32, blank=True, null=True, verbose_name="版本号")
    soft_version = CharField(max_length=32, blank=True, null=True, verbose_name="版本号")
    extra_info = TextField(null=True, verbose_name="额外信息")


class CardDevice(ExtraBaseModel):
    sn = CharField(max_length=64, db_index=True, verbose_name="序列号")  # 一卡通编号
    model = CharField(max_length=32, blank=True, null=True, verbose_name="型号")  # 一卡通型号
