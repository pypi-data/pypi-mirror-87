from models import ExtraCoreModel
from peewee import CharField, TextField


class School(ExtraCoreModel):
    name = CharField(max_length=64, verbose_name="名称,str(64)")
    description = TextField(null=True, verbose_name="简介")
    phone = CharField(max_length=20, blank=True, null=True, verbose_name="官方电话, str(20)")
    code = CharField(max_length=64, blank=True, null=True, verbose_name="学校唯一标识码, str(64)")

    province = CharField(max_length=20, verbose_name="省, str(20)")
    city = CharField(max_length=20, verbose_name="市, str(20)")
    area = CharField(max_length=20, verbose_name="区, str(20)")

    avatar = CharField(max_length=256, blank=True, null=True, verbose_name="校徽图片访问URL")
    motto = CharField(max_length=256, blank=True, null=True, verbose_name="校训")

    principal_name = CharField(max_length=64, blank=True, null=True, verbose_name="学校责任人姓名")
    principal_email = CharField(blank=True, null=True, verbose_name="学校责任人邮箱")
    principal_phone = CharField(max_length=20, blank=True, null=True, verbose_name="学校责任人电话")

    specific = TextField(null=True, verbose_name="个性化信息")
    brief_img = CharField(max_length=256, blank=True, null=True, verbose_name="简介图片路径")
    face_group = CharField(max_length=128, blank=True, null=True, verbose_name="人脸组")
