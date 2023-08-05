import threading
import traceback
from redis.exceptions import ConnectionError
from utils.redis_utils import RedisQueue
from core.processor import TaskResult
from utils.loggerutils import logging

logger = logging.getLogger(__name__)


class MessageThreadPool(object):
    def __init__(self, project, thread_num, processor):
        self.project = project
        self.processor = processor
        self.threads = []
        self.recall_threads = []
        self.running = 0
        self.thread_num = int(thread_num)
        self.recall_event = threading.Event()
        self._init_pool()

    def start_recall(self):
        if not self.is_recall:
            if self.recall_size != 0:
                logger.info(">>>Project {} Start Recall".format(self.project))
                self.recall_event.set()
                once_recall = OnceRecallMessageWorker(self, self.processor)
                once_recall.start()

    def stop_recall(self):
        if self.is_recall:
            logger.info(">>>Project {} Stop Recall".format(self.project))
            self.recall_event.clear()

    @property
    def is_recall(self):
        return self.recall_event.isSet()

    @property
    def recall_size(self):
        return self.recall_queue.qsize()

    @property
    def recall_queue(self):
        queue_name = "{}_RECALL".format(self.project)
        return RedisQueue(queue_name)

    def add_recall(self, content):
        self.recall_queue.put(content)

    def get_recall(self):
        content = self.recall_queue.get(timeout=10)
        return content

    @property
    def task_queue(self):
        return RedisQueue(self.project)

    def add_task(self, content):
        self.task_queue.put(content)

    def get_task(self):
        content = self.task_queue.get()
        return content

    def _init_pool(self):
        for _ in range(self.thread_num):
            self.threads.append(MessageWorker(self, self.processor))
        self.start_recall()

    def start_task(self):
        for item in self.threads:
            item.start()
        for rt in self.recall_threads:
            rt.start()

    def increase_running(self):
        self.running += 1

    def decrease_running(self):
        self.running -= 1


class MessageWorker(threading.Thread):
    def __init__(self, thread_pool, processor):
        super(MessageWorker, self).__init__()
        self.thread_pool = thread_pool
        self.processor = processor

    def run(self):
        logger.info(">>> Start Worker for project{}".format(self.thread_pool.project))
        print(">>> Start Worker for project{}".format(self.thread_pool.project))
        while True:
            try:
                content = self.thread_pool.get_task()
                self.thread_pool.increase_running()
                print("get task {}".format(content))
                result = self.processor.distribute(content['topic'], content['payload'])
                if result == TaskResult.FAILED:
                    logger.info(">>>Failed Task {}, Input Recall".format(content))
                    self.thread_pool.stop_recall()
                    self.thread_pool.add_recall(content)
                elif result == TaskResult.SUCCESS:
                    self.thread_pool.start_recall()
            except (ConnectionError,):
                pass
            except (Exception,) as e:
                logger.error(traceback.print_exc())
            finally:
                self.thread_pool.decrease_running()


class OnceRecallMessageWorker(threading.Thread):
    def __init__(self, thread_pool, processor):
        super(OnceRecallMessageWorker, self).__init__()
        self.thread_pool = thread_pool
        self.processor = processor

    def run(self):
        logger.info(">>> Start OnceRecallWorker for project{}".format(self.thread_pool.project))
        while True:
            try:
                if not self.thread_pool.is_recall:
                    break
                content = self.thread_pool.get_recall()
                if not content:
                    self.thread_pool.stop_recall()
                    break
                logger.info(">>>Get Recall Task {}".format(content))
                result = self.processor.distribute(content['topic'], content['payload'])
                if result == TaskResult.FAILED:
                    logger.info(">>>Failed Task {}, Input Recall".format(content))
                    self.thread_pool.stop_recall()
                    self.thread_pool.add_recall(content)
                logger.info(">>>Remain Recall Task :{}".format(self.thread_pool.recall_size))
            except (ConnectionError,):
                pass
            except (Exception,) as e:
                logger.error(traceback.print_exc())
        logger.info(">>> Finish OnceRecallWorker for project{}".format(self.thread_pool.project))

# class RecallMessageWorker(threading.Thread):
#     def __init__(self, thread_pool, recall_event):
#         super(RecallMessageWorker, self).__init__()
#         self.thread_pool = thread_pool
#         self.processors = {NICE_PROJECT: ProfessionProcessor}
#         self.recall_event = recall_event
# 
#     def run(self):
#         logger.info(">>> Start RecallWorker for project{}".format(self.thread_pool.project))
#         print(">>> Start RecallWorker for project{}".format(self.thread_pool.project))
#         while True:
#             try:
#                 self.recall_event.wait()
#                 content = self.thread_pool.get_recall()
#                 if not content:
#                     self.thread_pool.stop_recall()
#                     continue
#                 logger.info(">>>Get Recall Task {}".format(content))
#                 processor = self.processors.get(self.thread_pool.project, None)
#                 if processor:
#                     result = processor.distribute(content['topic'], content['payload'])
#                     if result == TaskResult.FAILED:
#                         logger.info(">>>Failed Task {}, Input Recall".format(content))
#                         self.thread_pool.stop_recall()
#                         self.thread_pool.add_recall(content)
#                     logger.info(">>>Remain Recall Task {}".format(self.thread_pool.recall_size))
#             except (ConnectionError,):
#                 pass
#             except (Exception,) as e:
#                 logger.error(traceback.print_exc())
