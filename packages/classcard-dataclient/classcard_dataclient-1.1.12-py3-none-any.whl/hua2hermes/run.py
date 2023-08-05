from core.mqtt import MQTTSubscribe
from business.pools import MESSAGE_POOLS
from utils.loggerutils import logging

logger = logging.getLogger(__name__)


def start():
    logger.info(">>> -------------------------------")
    logger.info(">>> Start Hermes Server")
    print(">>> Start Hermes Server")
    mqtt_subscribe = MQTTSubscribe()
    for project, message_pool in MESSAGE_POOLS.items():
        message_pool.start_task()
    mqtt_subscribe.server_connect()


if __name__ == '__main__':
    start()
