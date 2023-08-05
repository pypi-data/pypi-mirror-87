import traceback
from utils.loggerutils import logging

logger = logging.getLogger(__name__)


class TaskResult(object):
    FAILED = 'failed'
    SUCCESS = "success"


class Processor(object):
    KIND_FUNC = {}

    @classmethod
    def distribute(cls, topic, payload):
        try:
            data = payload['data']
            kind, content = data["kind"], data["extra"]
        except (Exception,):
            return None
        try:
            if kind in cls.KIND_FUNC:
                getattr(cls, cls.KIND_FUNC[kind])(content)
                return TaskResult.SUCCESS
        except (Exception,):
            logger.error(traceback.print_exc())
            return TaskResult.FAILED
