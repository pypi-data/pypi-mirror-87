import datetime
import pymssql
from requester.nirvana import NirvanaRequester
from utils.dateutils import datetime2str_z, str2datetime, date2str
from config import CLASS_CARD_HOST, CLASS_CARD_PORT
from utils.loggerutils import logging
from config import SQLSERVER_HOST, SQLSERVER_USER, SQLSERVER_PW, SQLSERVER_DB

logger = logging.getLogger(__name__)


def get_mssql_connection():
    conn = pymssql.connect(server=SQLSERVER_HOST, user=SQLSERVER_USER, password=SQLSERVER_PW,
                           database=SQLSERVER_DB)
    cur = conn.cursor()
    return conn, cur


def upload_meeting_attendance(content):
    status_map = {1: 0, 2: 3, 3: 1, 4: 2}
    logger.info(">>> Process upload_meeting_attendance")
    # attendance_id = content['original']["id"] if 'original' in content else content["id"]
    attendance_id, school_id = content['attendance_id'], content['school_id']
    nirvana_requester = NirvanaRequester(school_id=school_id, host=CLASS_CARD_HOST, port=CLASS_CARD_PORT)
    attendance_data = nirvana_requester.get_conventioneer_record_info(attendance_id)
    meeting_extra_info = attendance_data["meeting"]["extra_info"]
    meet_no = meeting_extra_info.get("meet_no")
    user_num = attendance_data["conventioneer"]["number"]
    record_time = attendance_data['record_time']
    status = attendance_data["status"]
    last_record_time = attendance_data['last_record_time']
    record_time = record_time.replace("T", " ")
    last_record_time = last_record_time.replace("T", " ")
    if not (record_time and user_num):
        logger.info(">>> Meeting Attendance Lost Info :{}".format(attendance_id))
        return
    conn, cur = get_mssql_connection()
    if meet_no:
        sql = "SELECT ID, REALSTART, REALEND FROM M_Meeting_Man_Out " \
              "WHERE MeetNo='{}' AND OutId='{}' ORDER BY ID".format(meet_no, user_num)
        cur.execute(sql)
        result = cur.fetchone()
        record_id, start, end = result[0], result[1], result[2]
        start_date = date2str(start.date())
        set_start = start_date == "1900-01-01"
        if set_start:
            record_status = status_map.get(status)
            update_sql = "UPDATE M_Meeting_Man_Out SET REALSTART='{}', STARTSTATUS={} " \
                         "WHERE ID={}".format(record_time, record_status, record_id)
        else:
            update_sql = "UPDATE M_Meeting_Man_Out SET REALEND='{}', ENDSTATUS={} " \
                         "WHERE ID={}".format(last_record_time, 1, record_id)
        cur.execute(update_sql)
        conn.commit()
    create_sql = "INSERT INTO M_ID_Record_Out(ECODE,OUTID,Poscode,OPERTIME,RECTYPE,IOFLAG,UpDateFlag,UpDateDT) " \
                 "VALUES('{}','{}','{}','{}','{}','{}','{}','{}')". \
        format("00000000", user_num, "1234", record_time, 17, 0, 0, record_time)
    cur.execute(create_sql)
    conn.commit()
    cur.close()
    conn.close()


def upload_student_attendance(content):
    status_map = {1: 0, 2: 3, 3: 1, 4: 2}
    logger.info(">>> Process upload_student_attendance")
    attendance_id, school_id = content['attendance_id'], content['school_id']
    nirvana_requester = NirvanaRequester(school_id=school_id, host=CLASS_CARD_HOST, port=CLASS_CARD_PORT)
    attendance_data = nirvana_requester.get_student_attendance_info(attendance_id)
    record_time = attendance_data['record_time']
    num, week = attendance_data['num'], attendance_data['week']
    record_status = status_map.get(attendance_data["status"])
    now = datetime.datetime.now()
    update_datetime = date2str(now)
    if not record_time:
        return
    student_number = attendance_data["student"]["number"]
    conn, cur = get_mssql_connection()
    create_sql = "INSERT INTO M_ID_Record_Out(ECODE,OUTID,Poscode,OPERTIME,RECTYPE,IOFLAG,UpDateFlag,UpDateDT) " \
                 "VALUES('{}','{}','{}','{}','{}','{}','{}','{}')". \
        format("00000000", student_number, "xxxxx", record_time, 17, 0, 0, update_datetime)
    cur.execute(create_sql)
    conn.commit()
    cur.close()
    conn.close()
