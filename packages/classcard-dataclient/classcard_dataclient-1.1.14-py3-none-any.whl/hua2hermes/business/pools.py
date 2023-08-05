from config import THREAD_NUM, HUA2_PROJECT
from core.worker_pool import MessageThreadPool
from business.processor import BusinessProcessor

hua2_message_pool = MessageThreadPool(HUA2_PROJECT, THREAD_NUM, BusinessProcessor)
MESSAGE_POOLS = {HUA2_PROJECT: hua2_message_pool}
