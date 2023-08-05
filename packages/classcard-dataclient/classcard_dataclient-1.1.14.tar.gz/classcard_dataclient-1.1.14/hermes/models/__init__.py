import uuid
import datetime
from peewee import MySQLDatabase, Model, UUIDField, DateTimeField, IntegerField
from utils.functions import field_to_json
from playhouse.shortcuts import model_to_dict
from config import DB, DB_HOST, DB_PORT, DB_USER, DB_PASSWD

db = MySQLDatabase(DB, host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWD)


class BaseSet(object):
    MESSAGE = {
    }

    @classmethod
    def choices(cls):
        return tuple(cls.MESSAGE.items())

    @classmethod
    def range(cls):
        return tuple(cls.MESSAGE.keys())

    @classmethod
    def check(cls, key):
        return key in cls.MESSAGE.keys()


class PublicLevel(BaseSet):
    ALL = 1
    SELF = 2
    GROUP = 3
    ADMIN = 4
    MESSAGE = {
        ALL: "所有人可访问",
        SELF: "自己可访问",
        GROUP: "同一分组可访问",
        ADMIN: "管理员可见"
    }


class CoreModel(Model):
    default_deleted_at = datetime.datetime.utcfromtimestamp(0)
    id = IntegerField(null=True, primary_key=True)
    deleted_at = DateTimeField(null=True, default=default_deleted_at)

    class Meta:
        database = db

    @classmethod
    def list(cls):
        return cls.select().where(cls.deleted_at == cls.default_deleted_at)

    def to_json(self):
        r = model_to_dict(self)
        r.pop("id", None)
        for k, v in r.items():
            r[k] = field_to_json(v)
        return r


class ExtraCoreModel(CoreModel):
    uid = UUIDField(unique=True, default=uuid.uuid4, index=True, verbose_name="唯一标识uid")
    public_level = IntegerField(choices=PublicLevel.choices(), default=PublicLevel.ALL, verbose_name="展示级别")
    create_time = DateTimeField(auto_now_add=True, verbose_name="创建时间, 2018-1-1T1:1:1.1111")
    update_time = DateTimeField(auto_now=True, verbose_name="修改时间, 2018-1-1T1:1:1.1111")

    @classmethod
    def get_with_uid(cls, uid):
        if not uid:
            return None
        return cls.get_or_none(cls.uid == uid, cls.deleted_at == cls.default_deleted_at)


class ThroughCoreModel(CoreModel):
    uid = UUIDField(unique=True, default=uuid.uuid4, index=True, verbose_name="唯一标识uid")

    @classmethod
    def get_with_uid(cls, uid):
        if not uid:
            return None
        return cls.get_or_none(cls.uid == uid, cls.deleted_at == cls.default_deleted_at)
