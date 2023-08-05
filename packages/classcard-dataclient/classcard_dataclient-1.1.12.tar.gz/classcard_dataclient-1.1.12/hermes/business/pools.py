from config import THREAD_NUM, NICE_PROJECT
from core.worker_pool import MessageThreadPool
from business.profession.processor import ProfessionProcessor

profession_message_pool = MessageThreadPool(NICE_PROJECT, THREAD_NUM, ProfessionProcessor)
MESSAGE_POOLS = {NICE_PROJECT: profession_message_pool}
