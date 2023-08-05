import os

SCHOOL_NAME = os.environ.get("SCHOOL_NAME", "北京好专业考勤管理学校")
NICE_SECRET_KEY = os.environ.get("NICE_SECRET_KEY", "ff48dec875cc56f330b28f14388b05e9")
NICE_APP_KEY = os.environ.get("NICE_APP_KEY", "21b190d5785837695e8cade16410be3a")
NICE_PROTOCOL = os.environ.get("NICE_PROTOCOL", "https")
NICE_HOST = os.environ.get("NICE_HOST", "xgk.lanzhou.edu.cn/schoolscheduleserv/integration")
# NICE_HOST = os.environ.get("NICE_HOST", "connect.nicezhuanye.com/schoolscheduleserv/integration")

NIRVANA_PROTOCOL = os.environ.get("NIRVANA_PROTOCOL", "http")
NIRVANA_HOST = os.environ.get("NIRVANA_HOST", "10.88.190.210")
NIRVANA_PORT = int(os.environ.get("NIRVANA_PORT", 14001))
NIRVANA_SCHOOL = os.environ.get("NIRVANA_SCHOOL", "35482fb5-6215-4187-a025-0562819eaef2")
NIRVANA_TOKEN = os.environ.get("NIRVANA_TOKEN", "skeleton gjtxsjtyjsxqsl Z2p0eHNqdHlqc3hxc2w=")

