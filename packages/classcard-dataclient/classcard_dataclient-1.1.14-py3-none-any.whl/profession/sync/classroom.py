from sync import BaseSync
from classcard_dataclient.models.classroom import Classroom, RoomType
from utils.loggerutils import logging
from utils.code import get_md5_hash

logger = logging.getLogger(__name__)


class ClassroomSync(BaseSync):
    def __init__(self, *args, **kwargs):
        super(ClassroomSync, self).__init__(*args, **kwargs)
        self.is_walking = True
        self.id_num_map = {}
        self.classroom_class = {}

    def sync(self):
        total = 0
        res = self.nice_requester.get_classroom_list()
        res_data = res.get('locations', [])
        classroom_list = []
        logging.info(self.classroom_class)
        for rd in res_data:
            building = rd['building'] or "教学楼"
            try:
                floor = int(rd['building'][-3])
            except (Exception, ):
                floor = 0
            number = get_md5_hash(rd['locationName'])
            self.id_num_map[rd['locationID']] = number
            category = RoomType.TYPE_PUBLIC if self.is_walking else RoomType.TYPE_CLASS
            classroom = Classroom(number=number, name=rd['locationName'], building=building,
                                  floor=floor, school=self.school_id)
            if rd['locationID'] in self.classroom_class:
                classroom.section_name = self.classroom_class[rd['locationID']]
                classroom.category = RoomType.TYPE_CLASS
                total += 1
                logger.info("classroom {} class is {}".format(rd['locationName'], classroom.section_name))
            else:
                classroom.category = RoomType.TYPE_PUBLIC
                logger.info("classroom {} has no name".format(rd['locationName']))
            classroom_list.append(classroom)
        self.client.create_classrooms(self.school_id, classroom_list)
        logging.info("{}/{} has class".format(total, len(classroom_list)))
