from config import HUA2_PROJECT


class ProjectRouter(object):
    direction = {"OpenConventioneerRecord": [HUA2_PROJECT],
                 "ConventioneerRecord": [HUA2_PROJECT],
                 "OpenStudentAttendance": [HUA2_PROJECT],
                 "StudentAttendance": [HUA2_PROJECT]}
