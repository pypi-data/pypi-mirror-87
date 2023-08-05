from business.action import upload_meeting_attendance, upload_student_attendance
from utils.loggerutils import logging
from core.processor import Processor

logger = logging.getLogger(__name__)


class BusinessProcessor(Processor):
    KIND_FUNC = {"OpenConventioneerRecord": "upload_meeting_attendance",
                 "ConventioneerRecord": "upload_meeting_attendance",
                 "OpenStudentAttendance": "upload_student_attendance",
                 "StudentAttendance": "upload_student_attendance"}

    @staticmethod
    def upload_meeting_attendance(*args, **kwargs):
        upload_meeting_attendance(*args, **kwargs)

    @staticmethod
    def upload_student_attendance(*args, **kwargs):
        upload_student_attendance(*args, **kwargs)
