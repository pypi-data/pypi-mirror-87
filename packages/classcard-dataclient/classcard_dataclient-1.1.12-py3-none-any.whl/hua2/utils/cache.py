import json
import redis
from utils.loggerutils import logging
from config import REDIS_HOST, REDIS_PORT

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
logger = logging.getLogger(__name__)


def set_cache(key, value, timeout=0):
    if isinstance(value, (dict, list, tuple)):
        try:
            value = json.dumps(value)
        except Exception as e:
            print(e)
    r.set(key, value, ex=60 * 1440)


def clear_cache(key):
    r.delete(key)


def get_cache(key):
    value = r.get(key)
    # set_cache(key=key, value=value)
    return value.decode("utf-8") if value else value


def get_cache_json(key):
    value = r.get(key)
    if isinstance(value, (str, bytes)):
        try:
            val_json = json.loads(value)
            set_cache(key=key, value=value)
            return val_json
        except Exception as e:
            print(e)
    else:
        logger.info("字符串转 json 错误", extra={"value": value, "type": type(value)})
    return None
