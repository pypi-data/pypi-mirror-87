from sync.base import BaseSync
from utils.loggerutils import logging

logger = logging.getLogger(__name__)


class PreSync(BaseSync):
    def _delete_all_course_table(self):
        self.client.delete_all_course_table(self.school_id, "当前学期")

    def sync(self):
        self._delete_all_course_table()
