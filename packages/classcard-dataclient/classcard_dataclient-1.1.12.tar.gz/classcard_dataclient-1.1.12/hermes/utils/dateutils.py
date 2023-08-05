import time
import datetime
import random


# 传入datetime,如果punchtime在(starttime, endtime)范围内返回TRUE
# 格式要求：punchtime:datetime.datetime, starttime,endtime:datetime.time
def is_in(punchtime, starttime, endtime):
    punchtime_int = int(datetime.datetime.strftime(punchtime, "%H%M%S"))
    starttime_int = int(datetime.time.strftime(starttime, "%H%M%S"))
    endtime_int = int(datetime.time.strftime(endtime, "%H%M%S"))
    if (punchtime_int >= starttime_int) and (punchtime_int <= endtime_int):
        return True
    else:
        return False


# 传入string,如果punchtime在(starttime, endtime)范围内返回TRUE
# 格式要求：punchtime:'2018-05-07 11:00:00', starttime,endtime:'11:00:00'
def is_in_str(punchtime, starttime, endtime):
    punchtime_int = int(
        datetime.datetime.strftime(datetime.datetime.strptime(punchtime, "%Y-%m-%d %H:%M:%S"), "%H%M%S"))
    starttime_int = int(datetime.datetime.strftime(datetime.datetime.strptime(starttime, "%H:%M:%S"), "%H%M%S"))
    endtime_int = int(datetime.datetime.strftime(datetime.datetime.strptime(endtime, "%H:%M:%S"), "%H%M%S"))
    if (punchtime_int >= starttime_int) and (punchtime_int <= endtime_int):
        return True
    else:
        return False


def rand_time(begin, end):
    return datetime.datetime.fromtimestamp(random.uniform(begin.timestamp(), end.timestamp()))


def str2_time(time_str):
    format_list = ["%H:%M:%S.%f", "%H:%M:%S"]
    for format in format_list:
        try:
            date_time = datetime.datetime.strptime(time_str, format)
            return date_time.time()
        except (Exception,):
            pass
    raise AttributeError('wrong time format')


def str2_date(date_str):
    if not date_str:
        return None
    if isinstance(date_str, datetime.date):
        return date_str
    elif isinstance(date_str, datetime.datetime):
        return date_str.date()
    try:
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return date.date()
    except (Exception,):
        pass
    raise AttributeError('wrong time format')


def date2str(dt):
    return dt.strftime("%Y-%m-%d") if dt else None


def str2datetime(time_str):
    if not time_str:
        return None
    format_list = ["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ",
                   "%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S"]

    for _ in format_list:
        try:
            date_time = datetime.datetime.strptime(time_str, _)
            return date_time
        except (Exception,):
            pass
    raise AttributeError('wrong time format')


def datetime2str_z(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ") if dt else None


def get_latest_days(days=7):
    today = datetime.date.today()
    weeks = []
    for _ in range(days):
        weeks.append(today.strftime('%Y%m%d'))
        today -= datetime.timedelta(days=1)
    return weeks


def format_datetime(date, time):
    return datetime.datetime.combine(date, time)
    # return datetime.datetime.strptime("{} {}".format(date.strftime("%Y-%m-%d"), time.strftime("%H:%M:%S")),
    #                                   "%Y-%m-%d %H:%M:%S")


def double2datetime_str(double_time):
    l_time = time.localtime(double_time)
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", l_time)
    return time_str


def get_week_days(index):
    days = []
    week = index.weekday()
    days.append(index)
    for si in range(1, week + 1):
        s_day = index - datetime.timedelta(days=si)
        days.append(s_day)
    for bi in range(1, 7 - week):
        b_day = index + datetime.timedelta(days=bi)
        days.append(b_day)
    return days
