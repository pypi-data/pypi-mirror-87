import os

# sqlserver
SQLSERVER_HOST = os.getenv("SQLSERVER_HOST", "10.51.67.54")
SQLSERVER_DB = os.getenv("SQLSERVER_DB", "SmartClass")
SQLSERVER_USER = os.getenv("SQLSERVER_USER", "sa")
SQLSERVER_PW = os.getenv("SQLSERVER_PW", "ccense.2020")

# edtech
EDTECH_SERVER_URL = os.getenv("EDTECH_SERVER_URL", "http://10.88.190.74:12363")
EDTECH_SERVER_TOKEN = os.getenv("EDTECH_SERVER_TOKEN", "Token 6c5a192e3e161342489971b10d36dee5250e64dd")

# classcard
CLASS_CARD_SERVER_URL = os.getenv("CLASS_CARD_SERVER_URL", "http://10.88.190.74:14001")
CLASS_CARD_SERVER_TOKEN = os.getenv("CLASS_CARD_SERVER_TOKEN", "Skeleton gjtxsjtyjsxqsl Z2p0eHNqdHlqc3hxc2w=")
# school config
TABLE_BEGIN_DATE = os.getenv("TABLE_BEGIN_DATE", "2019-08-26")
TABLE_END_DATE = os.getenv("TABLE_END_DATE", "2020-01-12")
TABLE_SEMESTER = os.getenv("TABLE_SEMESTER", "1")
TABLE_YJS_SEMESTER = os.getenv("TABLE_YJS_SEMESTER", "第一学期")
TABLE_YEAR = os.getenv("TABLE_YEAR", "2019-2020")
SCHOOL_NAME = os.getenv("SCHOOL_NAME", "五楼229环境")
SCHOOL_SEASON = os.getenv("SCHOOL_SEASON", "winter")
SEMESTER_NAME = os.getenv("SEMESTER_NAME", "当前学期")
REST_TABLE_NAME = os.getenv("REST_TABLE_NAME", "全校作息")
REST_TABLE_KEY1 = os.getenv("REST_TABLE_KEY1", "E-")
REST_TABLE_KEY2 = os.getenv("REST_TABLE_KEY2", "M-")
REST_TABLE_KEY3 = os.getenv("REST_TABLE_KEY3", "U-")
SUMMER_MORNING_LIMIT = os.getenv("SUMMER_MORNING_LIMIT", "12:30:00")
SUMMER_AFTERNOON_LIMIT = os.getenv("SUMMER_AFTERNOON_LIMIT", "17:00:00")
WINTER_MORNING_LIMIT = os.getenv("WINTER_MORNING_LIMIT", "12:30:00")
WINTER_AFTERNOON_LIMIT = os.getenv("WINTER_AFTERNOON_LIMIT", "17:00:00")

# redis
REDIS_HOST = os.getenv("REDIS_HOST", "10.51.67.67")
REDIS_PORT = int(os.getenv("REDIS_PORT", 36379))
