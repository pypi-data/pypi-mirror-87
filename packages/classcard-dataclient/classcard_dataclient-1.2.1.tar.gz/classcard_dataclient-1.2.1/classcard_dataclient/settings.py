# -*- coding: utf-8 -*-
"""
Created By Murray(m18527) on 2019/9/9 17:14
"""
import os

# edtech
EDTECH_SERVER_URL = os.getenv("EDTECH_SERVER_URL", "http://127.0.0.1:8000")
EDTECH_SERVER_TOKEN = os.getenv("EDTECH_SERVER_TOKEN", 'Token xx')

# classcard
CLASS_CARD_SERVER_URL = os.getenv("CLASS_CARD_SERVER_URL", "http://127.0.0.1:8000")
CLASS_CARD_SERVER_TOKEN = os.getenv("CLASS_CARD_SERVER_TOKEN", 'xx')

CLASS_CARD_SCHOOL = os.getenv("CLASS_CARD_SCHOOL", 'xxx')
DATA_ROOT = os.getenv("DATA_ROOT", '/data/classcard_dataclient')

LIMIT_NUM = os.getenv("LIMIT_NUM", '300')
