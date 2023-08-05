# -*- coding: utf-8 -*-
"""
Created By Murray(m18527) on 2019/9/18 11:01
"""
import time
from datetime import datetime

from basedata1.convertor import (section_convert, bk_student_convert, yj_student_convert, teacher_convert)
from classcard_dataclient import DataClient
from config import SCHOOL_NAME, SDTU_PAGE_SIZE
from requester.sdtu import SDTURequester
from utils.loggerutils import logging

logger = logging.getLogger(__name__)

client = DataClient()
client.set_config_module("config")


def get_school_id():
    code, school = client.get_school_by_name(SCHOOL_NAME)
    if code or not isinstance(school, dict):
        logger.error("Error: get school info, Detail: {}".format(school))
        school = {}
    return code, school.get("uuid")


def transact_section_data():
    logger.info("start section data sync at {}".format(datetime.now()))
    # 学校数据
    code, school_id = get_school_id()
    if code or not school_id:
        logger.error("Error: get school id fail, now break transact next data.")
        return
    sdtu_requester = SDTURequester()
    today_year = datetime.now().year
    front_years = 6
    # 获取班级数据
    for cut_year in range(front_years):
        current_year = today_year - cut_year
        page_index, row_index = 1, 1
        while True:
            section_res = sdtu_requester.get_section_list(page=page_index, pagesize=SDTU_PAGE_SIZE,
                                                          params={"NJ": str(current_year)})
            total_count = section_res["total"]
            current_rows = section_res["data"]["Rows"]
            for d in current_rows:
                section = section_convert(data=d, school=school_id)
                code, data = client.create_section(sections=section)
                if code:
                    logger.error("Code: {}, Msg: {}".format(code, data))
                logger.info("Already create {}/{} section".format(row_index, total_count))
                row_index += 1
            if page_index * SDTU_PAGE_SIZE >= total_count:
                break
            page_index += 1
        # 创建研究生班级
        current_yjs_section_data = {"BJMC": "研究生班级{}".format(current_year),
                                    "BH": "yjsection{}".format(current_year),
                                    "NJ": str(current_year)}
        current_yjs_section = section_convert(data=current_yjs_section_data, school=school_id)
        code, data = client.create_section(sections=current_yjs_section)
        if code:
            logger.error("Code: {}, Msg: {}".format(code, data))
    logger.info("end section data sync at {}".format(datetime.now()))


def transact_student_data():
    logger.info("start student data sync at {}".format(datetime.now()))
    # 1. 学校数据
    code, school_id = get_school_id()
    if code or not school_id:
        logger.error("Error: get school id fail, now break transact next data.")
        return
    sdtu_requester = SDTURequester()
    # 2. 一卡通数据
    card_dict = {}
    page_index, row_index = 1, 1
    while True:
        ecard_res = sdtu_requester.get_ecard_list(page=page_index, pagesize=SDTU_PAGE_SIZE)
        total_count = ecard_res["total"]
        current_rows = ecard_res["data"]["Rows"]
        sub_card_dict = {c['XGH']: c for c in current_rows if c.get("XGH")}
        card_dict.update(sub_card_dict)
        if page_index * SDTU_PAGE_SIZE >= total_count:
            break
        page_index += 1
    # 3. 班级数据
    code, sections = client.get_section_list(school_id=school_id)
    if code or not isinstance(sections, list):
        logger.error("Error: get section info, Detail: {}".format(sections))
        sections = []
    section_dict = {d["name"]: d['uuid'] for d in sections if d.get("name")}
    # 4. 学生数据
    number_map = client.get_student_number_map(school_id)
    today_year = datetime.now().year
    front_years = 6
    # 4.1 本科生数据
    for cut_year in range(front_years):
        current_year = today_year - cut_year
        page_index, row_index = 1, 1
        while True:
            bk_student_res = sdtu_requester.get_bk_student_list(page=page_index, pagesize=SDTU_PAGE_SIZE,
                                                                params={"XZNJ": str(current_year)})
            total_count = bk_student_res["total"]
            current_rows = bk_student_res["data"]["Rows"]
            for d in current_rows:
                section_id = section_dict.get(d["BH"])
                ecard = card_dict.get(d["XH"])
                student = bk_student_convert(data=d, ecard=ecard, school=school_id, section=section_id)
                if student.number in number_map:
                    student.uid = number_map[student.number]
                code, data = client.create_student(students=student)
                if code:
                    logger.error("Code: {}, Msg: {}".format(code, data))
                logger.info("Already create {}/{} bks".format(row_index, total_count))
                row_index += 1
            if page_index * SDTU_PAGE_SIZE >= total_count:
                break
            page_index += 1
    # 4.1 研究生数据
    for cut_year in range(front_years):
        current_year = today_year - cut_year
        page_index, row_index = 1, 1
        while True:
            yj_student_res = sdtu_requester.get_yj_student_list(page=page_index, pagesize=SDTU_PAGE_SIZE,
                                                                params={"NJ": str(current_year)})
            total_count = yj_student_res["total"]
            current_rows = yj_student_res["data"]["Rows"]
            for d in current_rows:
                section_bh = "yjsection{}".format(current_year)
                section_id = section_dict.get(section_bh)
                ecard = card_dict.get(d["XH"])
                student = yj_student_convert(data=d, ecard=ecard, school=school_id, section=section_id)
                if student.number in number_map:
                    student.uid = number_map[student.number]
                code, data = client.create_student(students=student)
                if code:
                    logger.error("Code: {}, Msg: {}".format(code, data))
                logger.info("Already create {}/{} yjs".format(row_index, total_count))
                row_index += 1
            if page_index * SDTU_PAGE_SIZE >= total_count:
                break
            page_index += 1
    logger.info("end student data sync at {}".format(datetime.now()))


def transact_teacher_data():
    logger.info("start teacher data sync at {}".format(datetime.now()))
    # 1. 学校数据
    code, school_id = get_school_id()
    if code or not school_id:
        logger.error("Error: get school id fail, now break transact next data.")
        return
    sdtu_requester = SDTURequester()
    # 2. 一卡通数据
    card_dict = {}
    page_index, row_index = 1, 1
    while True:
        ecard_res = sdtu_requester.get_ecard_list(page=page_index, pagesize=SDTU_PAGE_SIZE)
        total_count = ecard_res["total"]
        current_rows = ecard_res["data"]["Rows"]
        sub_card_dict = {c['XGH']: c for c in current_rows if c.get("XGH")}
        card_dict.update(sub_card_dict)
        if page_index * SDTU_PAGE_SIZE >= total_count:
            break
        page_index += 1
    # 3. 教职工数据
    number_map = client.get_teacher_number_map(school_id)
    page_index, row_index = 1, 1
    while True:
        teacher_res = sdtu_requester.get_teacher_list(page=page_index, pagesize=SDTU_PAGE_SIZE)
        total_count = teacher_res["total"]
        current_rows = teacher_res["data"]["Rows"]
        for d in current_rows:
            ecard = card_dict.get(d["ZGH"])
            teacher = teacher_convert(data=d, ecard=ecard, school=school_id)
            if teacher.number in number_map:
                teacher.uid = number_map[teacher.number]
                logger.info("find number {}: {}".format(teacher.number, teacher.uid))
            code, data = client.create_teacher(teacher)
            if code:
                logger.error("Code: {}, Msg: {}".format(code, data))
            logger.info("Already create {}/{} teacher".format(row_index, total_count))
            row_index += 1
        if page_index * SDTU_PAGE_SIZE >= total_count:
            break
        page_index += 1
    logger.info("end teacher data sync at {}".format(datetime.now()))


def start_data_sync():
    start_time = time.time()
    logger.info("start data sync at {}".format(datetime.now()))
    transact_section_data()
    transact_student_data()
    transact_teacher_data()
    logger.info("end data sync at {}".format(datetime.now()))
    logger.info("data sync used: {}s".format(round(time.time() - start_time, 4)))


def start_teacher_sync():
    start_time = time.time()
    logger.info("start teacher sync at {}".format(datetime.now()))
    transact_teacher_data()
    logger.info("end teacher sync at {}".format(datetime.now()))
    logger.info("teacher sync used: {}s".format(round(time.time() - start_time, 4)))


if __name__ == '__main__':
    pass
    # start_data_sync()
