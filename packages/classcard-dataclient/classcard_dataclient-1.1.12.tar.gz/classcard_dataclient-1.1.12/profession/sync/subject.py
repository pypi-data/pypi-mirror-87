import time
from sync import BaseSync
from classcard_dataclient.models.subject import Subject
from utils.loggerutils import logging

logger = logging.getLogger(__name__)


class SubjectSync(BaseSync):
    def sync(self):
        res = self.nice_requester.get_subject_list()
        res_data = res
        subject_list = []
        for rd in res_data:
            logger.info("subject: {}".format(rd))
            time.sleep(2)
            subject = Subject(number=rd['id'], name=rd['name'], school=self.school_id)
            subject_list.append(subject)
        self.client.create_subjects(self.school_id, subject_list)

