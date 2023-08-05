import os

# oracle
ORACLE_SERVER = os.getenv("ORACLE_SERVER", "usr_third/sdnuthird@172.23.0.19/urpdb")
AVATAR_ORACLE_SERVER = os.getenv("AVATAR_ORACLE_SERVER", "ssd_dzbp_xhs/dpW!@#@210.44.8.77:1521/dwdb")

# edtech
EDTECH_SERVER_URL = os.getenv("EDTECH_SERVER_URL", "http://10.88.190.100:12363")
EDTECH_SERVER_TOKEN = os.getenv("EDTECH_SERVER_TOKEN", 'Token 6c5a192e3e161342489971b10d36dee5250e64dd')

# school config
TABLE_BEGIN_DATE = os.getenv("TABLE_BEGIN_DATE", "2019-08-26")
TABLE_END_DATE = os.getenv("TABLE_END_DATE", "2020-01-12")
TABLE_SEMESTER = os.getenv("TABLE_SEMESTER", '1')
TABLE_YJS_SEMESTER = os.getenv("TABLE_YJS_SEMESTER", '第一学期')
TABLE_YEAR = os.getenv("TABLE_YEAR", '2019-2020')

# classcard
CLASS_CARD_SERVER_URL = os.getenv("CLASS_CARD_SERVER_URL", "http://10.88.190.100:14001")
CLASS_CARD_SERVER_TOKEN = os.getenv("CLASS_CARD_SERVER_TOKEN", 'Skeleton gjtxsjtyjsxqsl Z2p0eHNqdHlqc3hxc2w=')

SDTU_SERVER = os.getenv("SDTU_SERVER", "http://210.44.8.70:8888")
SDTU_APP_ID = os.getenv("SDTU_APP_ID", "ssd_dzbp_xhs_1602215213577")
SDTU_SECRET_KEY = os.getenv("SDTU_SECRET_KEY", "a71ecfb4-6d5f-432b-9aa2-714870c294ae")
SDTU_PAGE_SIZE = int(os.getenv("SDTU_PAGE_SIZE", 200))

AVATAR_PATH = "/root/data/avatar"
JSON_PATH = ""

SCHOOL_NAME = os.getenv("SCHOOL_NAME", "山东师范大学")
