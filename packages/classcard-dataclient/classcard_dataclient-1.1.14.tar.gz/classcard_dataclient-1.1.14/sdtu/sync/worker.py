import time
from sync.album import AlbumSync
from sync.board import NoticeSync
from sync.course import CourseTableSync
from sync.news import NewsSync
from sync.video import VideoSync
from sync.exam import ExamSync
from utils.loggerutils import logging

logger = logging.getLogger(__name__)


def table_sync():
    start_time = time.time()
    course_table_sync = CourseTableSync()
    course_table_sync.need_relate_student = False
    course_table_sync.start()
    logger.info("course table sync used: {}s".format(round(time.time() - start_time, 4)))
    start_exam_sync()


def start_crawl():
    start_time = time.time()
    for sync_class in [AlbumSync, VideoSync, NoticeSync, NewsSync]:
        crawler = sync_class()
        crawler.start()
    logger.info("info crawl used: {}s".format(round(time.time() - start_time, 4)))


def start_exam_sync():
    start_time = time.time()
    exam_sync = ExamSync()
    exam_sync.start()
    logger.info("exam sync used: {}s".format(round(time.time() - start_time, 4)))
