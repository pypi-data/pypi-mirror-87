import os
import cx_Oracle
import datetime
from sync.base import BaseSync
from config import AVATAR_ORACLE_SERVER, AVATAR_PATH
from utils.dateutils import datetime2str
from utils.loggerutils import logging

logger = logging.getLogger(__name__)


class AvatarSync(BaseSync):
    def __init__(self):
        super(AvatarSync, self).__init__()
        db = cx_Oracle.connect(AVATAR_ORACLE_SERVER, encoding="UTF-8", nencoding="UTF-8")  # 连接数据库
        now = datetime.datetime.now()
        self.offset = 10
        self.cur = db.cursor()

    @property
    def last_modify(self):
        last_modify_tag = os.path.join(AVATAR_PATH, "last_modify_tag.txt")
        if os.path.exists(AVATAR_PATH) and os.path.exists(last_modify_tag):
            with open(last_modify_tag, "r") as f:
                last_modify_time = f.readline()
                f.close()
            return last_modify_time
        return None

    def set_last_modify(self):
        last_modify_time = datetime2str(datetime.datetime.now())
        last_modify_tag = os.path.join(AVATAR_PATH, "last_modify_tag.txt")
        if os.path.exists(AVATAR_PATH):
            if os.path.exists(last_modify_tag):
                os.remove(last_modify_tag)
            with open(last_modify_tag, "w") as f:
                f.write(last_modify_time)
                f.close()

    @classmethod
    def write_file(cls, data, filename):
        with open(filename, 'wb') as f:
            f.write(data)
            f.close()

    def extract_avatar(self):
        if not os.path.exists(AVATAR_PATH):
            os.makedirs(AVATAR_PATH)
        student_number_map = self.client.get_student_number_map(self.school_id)
        teacher_number_map = self.client.get_teacher_number_map(self.school_id)
        if self.last_modify:
            count_sql = "SELECT COUNT(*) FROM T_YKT_PHOTO WHERE ZHXGSJ >= '{}'".format(self.last_modify)
        else:
            count_sql = "SELECT COUNT(*) FROM T_YKT_PHOTO"
        self.cur.execute(count_sql)
        try:
            total = self.cur.fetchall()[0][0]
        except (Exception,):
            total = 1
        total_page = total // self.offset if total % self.offset == 0 else total // self.offset + 1
        row_index = 1
        for index in range(total_page):
            si, ei = index * self.offset + 1, (index + 1) * self.offset
            if self.last_modify:
                sql = "SELECT k.XGH, k.XM, k.ZP, k.ZHXGSJ, k.r " \
                      "FROM (SELECT x.*, rownum r FROM T_YKT_PHOTO x " \
                      "WHERE ZHXGSJ >= '{}' ORDER BY XGH) " \
                      "k WHERE k.r BETWEEN {} and {}".format(self.last_modify, si, ei)
            else:
                sql = "SELECT k.XGH, k.XM, k.ZP, k.ZHXGSJ, k.r " \
                      "FROM (SELECT x.*, rownum r FROM T_YKT_PHOTO x " \
                      "ORDER BY XGH) " \
                      "k WHERE k.r BETWEEN {} and {}".format(si, ei)
            self.cur.execute(sql)
            rows = self.cur.fetchall()
            for row in rows:
                number, name, avatar = row[0], row[1], row[2].read()
                if not (number and name and avatar):
                    continue
                file_name = "{}-{}.jpg".format(name, number)
                file_path = os.path.join(AVATAR_PATH, file_name)
                self.write_file(avatar, file_path)
                avatar_res, face_res = None, None
                if number in student_number_map:
                    user_id = student_number_map[number]
                    avatar_res = self.client.upload_user_avatar(self.school_id, file_path, user_id)
                    face_res = self.client.upload_user_face(self.school_id, file_path, student_id=user_id)
                if number in teacher_number_map:
                    user_id = teacher_number_map[number]
                    avatar_res = self.client.upload_user_avatar(self.school_id, file_path, user_id)
                    face_res = self.client.upload_user_face(self.school_id, file_path, teacher_id=user_id)
                os.remove(file_path)
                logger.info(avatar_res)
                logger.info(face_res)
                logger.info("already upload {}/{} avatar".format(row_index, total))
                row_index += 1

    def sync(self):
        self.extract_avatar()
        self.set_last_modify()
