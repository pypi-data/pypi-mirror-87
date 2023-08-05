from sync.base import BaseSync
from utils.loggerutils import logging
from utils.code import get_md5_hash
from classcard_dataclient.models.subject import Subject

logger = logging.getLogger(__name__)


class SubjectSync(BaseSync):
    def __init__(self):
        super(SubjectSync, self).__init__()
        self.offset = 300
        self.subject_map = {}

    def clear_subjects(self):
        subject_num_map = self.client.get_subject_num_map(self.school_id)
        for subject_id in list(subject_num_map.values()):
            self.client.delete_subject(self.school_id, subject_id)

    def extract_subject(self):
        today, last_day = self.get_date_range()
        # today, last_day = "2020-11-02", "2020-11-08"
        sql = "SELECT DISTINCT coursedetailid, coursename FROM mid_attendschedule " \
              "WHERE coursedate > '{}' and coursedate <= '{}' ORDER BY coursedetailid".format(today, last_day)
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        for row in rows:
            subject_id, name = row[0], row[1]
            number = get_md5_hash(name)
            subject = Subject(number=number, name=name, school=self.school_id)
            self.subject_map[number] = subject

    def sync(self):
        self.clear_subjects()
        self.extract_subject()
        if not self.subject_map:
            logger.info("没有科目信息")
            return
        # subject_list = list(self.subject_map.values())
        # self.client.create_subjects(self.school_id, subject_list)
        self.close_db()
