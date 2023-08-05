import os

DB = os.environ.get("DB", "partysvc")
DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
DB_PORT = int(os.environ.get("DB_PORT", 54321))
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWD = os.environ.get("DB_PASSWD", "1q2w3e")

MQTT_HOST = os.environ.get('MQTT_HOST', "10.88.190.210")
MQTT_PORT = int(os.environ.get('MQTT_PORT', 13125))
MQTT_USERNAME = os.environ.get('MQTT_USER', "mtpub")
MQTT_PASSWORD = os.environ.get('MQTT_PASSWORD', "G67*@99XfjJ3")
MQTT_MESSAGE_TYPE = "classcard"
MQTT_SUBSCRIBE_TOPIC = os.environ.get('MQTT_SUBSCRIBE_TOPIC', "+")
CLIENT_PUB_ID = "publish_nirvana_pub{}".format(os.environ.get('MQTT_CLIENT', "hermes"))
CLIENT_SUB_ID = "publish_nirvana_sub{}".format(os.environ.get('MQTT_CLIENT', "hermes"))

CLASS_CARD_HOST = os.environ.get('CLASS_CARD_HOST', "10.88.190.210")
CLASS_CARD_PORT = int(os.environ.get('CLASS_CARD_PORT', 14001))
CLASS_CARD_SERVER_TOKEN = os.environ.get('CLASS_CARD_SERVER_TOKEN', "Skeleton gjtxsjtyjsxqsl Z2p0eHNqdHlqc3hxc2w=")
CLASS_CARD_SCHOOL = os.environ.get('CLASS_CARD_SCHOOL', "mtpub")

REDIS_HOST = os.environ.get('REDIS_HOST', "10.88.188.229")
REDIS_PORT = int(os.environ.get('REDIS_PORT', 16379))
REDIS_DB = int(os.environ.get('REDIS_DB', 4))
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', None)

THREAD_NUM = int(os.environ.get('THREAD_NUM', 1))

SCHOOL_NAME = os.environ.get("SCHOOL_NAME", "北京好专业考勤管理学校")
NICE_SECRET_KEY = os.environ.get("NICE_SECRET_KEY", "ff48dec875cc56f330b28f14388b05e9")
NICE_APP_KEY = os.environ.get("NICE_APP_KEY", "21b190d5785837695e8cade16410be3a")
NICE_PROTOCOL = os.environ.get("NICE_PROTOCOL", "http")
# NICE_HOST = os.environ.get("NICE_HOST", "dockertest.nicezhuanye.com/schoolscheduleserv/integration")
NICE_HOST = os.environ.get("NICE_HOST", "connect.nicezhuanye.com/schoolscheduleserv/integration")
NICE_PROJECT = 'profession'
