import os

MHANG_CLIENT_ID = os.environ.get("MHANG_CLIENT_ID", "f849bbb3-09df-41cb-a6d4-7e76d8d1be4a")
MHANG_CLIENT_SECRET = os.environ.get("MHANG_CLIENT_SECRET", "07d7bd5646b200366863724f0c5c6cd3e9c40f83")
MHANG_EDU_ID = os.environ.get("MHANG_EDU_ID", "2d4aab3927127fba1b8ec2666ee86461")
MHANG_BASE_URL = os.environ.get("MHANG_BASE_URL", "https://dev.web.ckmooc.com")


NIRVANA_PROTOCOL = os.environ.get("NIRVANA_PROTOCOL", "http")
NIRVANA_HOST = os.environ.get("NIRVANA_HOST", "10.88.190.210")
NIRVANA_PORT = int(os.environ.get("NIRVANA_PORT", 14001))
NIRVANA_SCHOOL = os.environ.get("NIRVANA_SCHOOL", "35482fb5-6215-4187-a025-0562819eaef2")
NIRVANA_TOKEN = os.environ.get("NIRVANA_TOKEN", "skeleton gjtxsjtyjsxqsl Z2p0eHNqdHlqc3hxc2w=")

REDIS_HOST = os.environ.get('REDIS_HOST', "10.88.188.228")
REDIS_PORT = int(os.environ.get('REDIS_PORT', 16379))
REDIS_DB = int(os.environ.get('REDIS_DB', 4))
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', None)

