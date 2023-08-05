from business.profession.action import upload_student_attendance
from utils.loggerutils import logging
from core.processor import Processor

logger = logging.getLogger(__name__)


class ProfessionProcessor(Processor):
    KIND_FUNC = {"OpenStudentAttendance": "upload_student_attendance"}

    @staticmethod
    def upload_student_attendance(content):
        upload_student_attendance(content)
