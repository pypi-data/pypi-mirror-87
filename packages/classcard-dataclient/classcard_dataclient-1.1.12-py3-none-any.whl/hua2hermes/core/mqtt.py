# -*- coding: utf-8 -*-
import paho.mqtt.publish as pub
import paho.mqtt.subscribe as sub
import paho.mqtt.client as mqtt
import json
from config import MQTT_HOST, MQTT_PORT, CLIENT_PUB_ID, CLIENT_SUB_ID, MQTT_USERNAME, MQTT_PASSWORD, \
    MQTT_MESSAGE_TYPE, MQTT_SUBSCRIBE_TOPIC
from business.router import ProjectRouter
from business.pools import MESSAGE_POOLS
from utils.loggerutils import logging

logger = logging.getLogger(__name__)


def loads_message(message):
    return json.loads(message)


def dumps_message(message):
    sn = message.pop("member", None)
    data = {
        "type": MQTT_MESSAGE_TYPE,
        "sn": sn,
        "data": message
    }
    logger.info(data)
    return json.dumps(data)


def _on_connect(client, userdata, flags, rc):
    print('connected to mqtt with resurt code ', rc)
    client.subscribe(MQTT_SUBSCRIBE_TOPIC)


def _on_publish(client, userdata, mid):
    logger.info("on publish:{}".format(mid))


def _on_message(client, userdata, msg):
    try:
        print("{} :> {}".format(msg.topic, msg.payload))
        logger.info("{} :> {}".format(msg.topic, msg.payload))
        payload = loads_message(msg.payload.decode('utf-8'))
        kind = payload['data']['kind']
        projects = ProjectRouter.direction.get(kind, [])
        for project in projects:
            if project in MESSAGE_POOLS:
                # school_id = str(msg.topic).replace("school:", "")
                task_content = {"topic": msg.topic, "payload": payload}
                MESSAGE_POOLS[project].add_task(task_content)
    except (Exception,):
        return


class MQTTPublish(object):

    def __init__(self, keepalive=60, clean_session=False, protocol=mqtt.MQTTv311, transport="tcp", **kwargs):
        self.mqtt_params = {
            "keepalive": keepalive,
            "clean_session": clean_session,
            "protocol": protocol,
            "transport": transport,
            "client_id": CLIENT_PUB_ID,
            "username": MQTT_USERNAME,
            "password": MQTT_PASSWORD,
            "host": MQTT_HOST,
            "port": MQTT_PORT
        }
        self.mqtt_params.update(kwargs)
        self.client = self.init_client()

    def init_client(self):
        client = mqtt.Client(client_id=self.mqtt_params["client_id"], clean_session=self.mqtt_params["clean_session"],
                             protocol=self.mqtt_params["protocol"],
                             transport=self.mqtt_params["transport"])
        client.on_publish = _on_publish
        client.username_pw_set(self.mqtt_params["username"], self.mqtt_params["password"])
        client.connect(self.mqtt_params["host"], self.mqtt_params["port"], self.mqtt_params["keepalive"])
        client.loop_start()
        return client

    def __getattr__(self, attr):
        if attr not in self.__dict__:
            return getattr(self.client, attr)
        return self.__dict__[attr]

    def publish(self, topic, message, qos=0, retain=False):
        if self._state != mqtt.mqtt_cs_connected:
            self.disconnect()
            logger.info("close old client:{}".format(self.client))
            self.client = self.init_client()
        payload = dumps_message(message)
        logger.info("topic: {} -- {}".format(topic, payload))
        return self.client.publish(topic, payload, qos=qos, retain=retain)


class MQTTSubscribe(object):
    def __init__(self, keepalive=60, clean_session=False, protocol=mqtt.MQTTv311, transport="tcp", **kwargs):
        self.topic = kwargs.pop("topic", MQTT_SUBSCRIBE_TOPIC)
        self.mqtt_params = {
            "keepalive": keepalive,
            "clean_session": clean_session,
            "protocol": protocol,
            "transport": transport,
            "client_id": CLIENT_SUB_ID,
            "username": MQTT_USERNAME,
            "password": MQTT_PASSWORD,
            "host": MQTT_HOST,
            "port": MQTT_PORT
        }
        self.mqtt_params.update(kwargs)
        self.client = None

    def server_connect(self):
        client = mqtt.Client(client_id=self.mqtt_params["client_id"], clean_session=self.mqtt_params["clean_session"],
                             protocol=self.mqtt_params["protocol"],
                             transport=self.mqtt_params["transport"])
        client.on_connect = _on_connect
        client.on_message = _on_message
        client.username_pw_set(self.mqtt_params["username"], self.mqtt_params["password"])
        client.connect(self.mqtt_params["host"], self.mqtt_params["port"], self.mqtt_params["keepalive"])
        print(">>>Connected MQTT Server on {}:{}".format(self.mqtt_params["host"], self.mqtt_params["port"]))
        logger.info(">>>Connected MQTT Server on {}:{}".format(self.mqtt_params["host"], self.mqtt_params["port"]))
        client.loop_forever()

    def init_client(self):
        client = mqtt.Client(client_id=self.mqtt_params["client_id"], clean_session=self.mqtt_params["clean_session"],
                             protocol=self.mqtt_params["protocol"],
                             transport=self.mqtt_params["transport"])
        client.on_connect = _on_connect
        client.on_message = _on_message
        client.username_pw_set(self.mqtt_params["username"], self.mqtt_params["password"])
        client.connect(self.mqtt_params["host"], self.mqtt_params["port"], self.mqtt_params["keepalive"])
        client.loop_start()
        return client

    def __getattr__(self, attr):
        if attr not in self.__dict__:
            return getattr(self.client, attr)
        return self.__dict__[attr]

    def subscribe(self, topic, qos=0):
        if self._state != mqtt.mqtt_cs_connected:
            self.disconnect()
            logger.info("close old client:{}".format(self.client))
            self.client = self.init_client()
        # LOG.info("topic: {} -- {}".format(topic, payload))
        message = self.client.subscribe(topic, qos=qos)
        return message
