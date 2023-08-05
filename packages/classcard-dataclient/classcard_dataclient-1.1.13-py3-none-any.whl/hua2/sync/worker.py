import time
from sync.classroom import ClassroomSync
from sync.course import CourseSync
from sync.meeting_room import MeetingRoomSync
from sync.schedule import ScheduleSync
from sync.section import SectionSync
from sync.subject import SubjectSync
from sync.student import StudentSync
from sync.teacher import TeacherSync
from sync.pre import PreSync
from utils.cache import set_cache, get_cache_json
from utils.loggerutils import logging

logger = logging.getLogger(__name__)


def start_table_sync():
    table_sync_key = "TABLE_SYNC_KEY"
    sync_status = get_cache_json(table_sync_key)
    if not sync_status or not sync_status.get("result", False):
        logger.info("当前无课表同步进行，开始同步")
        set_cache(table_sync_key, {"result": True})
    else:
        logger.info("当前有课表同步进行，退出")
        return
    pre_sync = PreSync()
    pre_sync.start()
    teacher_sync = TeacherSync()
    teacher_sync.start()
    section_sync = SectionSync()
    section_sync.start()
    student_sync = StudentSync()
    student_sync.start()
    subject_sync = SubjectSync()
    subject_sync.start()
    schedule_sync = ScheduleSync()
    schedule_sync.start()
    classroom_sync = ClassroomSync()
    classroom_sync.start()
    course_sync = CourseSync()
    course_sync.slot_map = schedule_sync.slot_map
    course_sync.semester = schedule_sync.semester
    course_sync.rest_table = schedule_sync.rest_table
    course_sync.student_map = student_sync.student_map
    course_sync.student_section_map = student_sync.student_section_map
    course_sync.teacher_map = teacher_sync.teacher_map
    course_sync.classroom_map = classroom_sync.classroom_map
    course_sync.class_name_num = section_sync.name_num
    course_sync.rest_table_slot = schedule_sync.rest_table_slot
    course_sync.start()
    # meeting_room_sync = MeetingRoomSync()
    # meeting_room_sync.start()
    set_cache(table_sync_key, {"result": False})


def start_meeting_sync():
    meeting_sync_key = "MEETING_SYNC_KEY"
    sync_status = get_cache_json(meeting_sync_key)
    if not sync_status or not sync_status.get("result", False):
        logger.info("当前无会议同步进行，开始同步")
        set_cache(meeting_sync_key, {"result": True})
    else:
        logger.info("当前有会议同步进行，退出")
        return
    teacher_sync = TeacherSync()
    teacher_sync.create = False
    teacher_sync.start()
    section_sync = SectionSync()
    section_sync.create = False
    section_sync.start()
    student_sync = StudentSync()
    student_sync.create = False
    student_sync.start()
    meeting_room_sync = MeetingRoomSync()
    meeting_room_sync.start()
    set_cache(meeting_sync_key, {"result": False})


if __name__ == '__main__':
    start_table_sync()
