# -*- coding: utf-8 -*-
import json
import os
base_file_path = os.path.dirname(__file__)


def file_read(filename):
    ret = None
    try:
        with open(os.path.join(base_file_path, filename), 'r', encoding='utf-8') as f:
            ret = f.read()
            ret = json.loads(ret)
    except Exception as e:
        print(e)
    return ret


def get_province_name(code):
    province = file_read("province.json")
    if isinstance(province, list):
        for i in province:
            if i.get("code") == code:
                return i.get("name")
    return "NA"


def get_city_name(code):
    city = file_read("city.json")
    if isinstance(city, list):
        for i in city:
            if i.get("code") == code:
                return i.get("name")
    return "NA"


def get_area_name(code):
    area = file_read("area.json")
    if isinstance(area, list):
        for i in area:
            if i.get("code") == code:
                return i.get("name")
    return "NA"


