import os

MQTT_HOST = os.environ.get('MQTT_HOST', "10.88.188.229")
MQTT_PORT = int(os.environ.get('MQTT_PORT', 13125))
MQTT_USERNAME = os.environ.get('MQTT_USER', "mtpub")
MQTT_PASSWORD = os.environ.get('MQTT_PASSWORD', "G67*@99XfjJ3")
MQTT_MESSAGE_TYPE = "classcard"
MQTT_SUBSCRIBE_TOPIC = os.environ.get('MQTT_SUBSCRIBE_TOPIC', "+")
CLIENT_PUB_ID = "publish_nirvana_pub{}".format(os.environ.get('MQTT_CLIENT', "hua2hermes"))
CLIENT_SUB_ID = "publish_nirvana_sub{}".format(os.environ.get('MQTT_CLIENT', "hua2hermes"))

CLASS_CARD_HOST = os.environ.get('CLASS_CARD_HOST', "10.88.188.229")
CLASS_CARD_PORT = int(os.environ.get('CLASS_CARD_PORT', 14001))
CLASS_CARD_SERVER_TOKEN = os.environ.get('CLASS_CARD_SERVER_TOKEN', "Skeleton gjtxsjtyjsxqsl Z2p0eHNqdHlqc3hxc2w=")
CLASS_CARD_SCHOOL = os.environ.get('CLASS_CARD_SCHOOL', "mtpub")

REDIS_HOST = os.environ.get('REDIS_HOST', "10.88.188.229")
REDIS_PORT = int(os.environ.get('REDIS_PORT', 16379))
REDIS_DB = int(os.environ.get('REDIS_DB', 4))
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', None)

THREAD_NUM = int(os.environ.get('THREAD_NUM', 1))
HUA2_PROJECT = "hua2"

# sqlserver
SQLSERVER_HOST = os.getenv("SQLSERVER_HOST", "10.51.67.54")
SQLSERVER_DB = os.getenv("SQLSERVER_DB", "SmartClass")
SQLSERVER_USER = os.getenv("SQLSERVER_USER", "sa")
SQLSERVER_PW = os.getenv("SQLSERVER_PW", "ccense.2020")
