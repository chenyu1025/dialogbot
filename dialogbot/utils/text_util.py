# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""
import json
import logging
import os
import re

ch_pattern = re.compile(r"[\u4e00-\u9fa5]+")
remove_pattern = re.compile(r"好的")


def ch_count(text):
    """
    Count chinese number.
    :param text:
    :return:
    """
    text = remove_pattern.sub("", text)
    r = ch_pattern.findall(text)
    cnt = len("".join(r))
    return cnt


def parse_result_from_str(str):
    try:

        pattern = re.compile(r'\{(.*)\}', re.DOTALL)  # replace with your regex
        match = pattern.search(str)
        cleaned_str = ""
        if match:
            cleaned_str = "{" + match.group(1) + "}"
        return json.loads(cleaned_str)
    except Exception as e:
        logging.error("parse error ", e)
        parsed_result = {"positive": {}, "negative": {}}
        return parsed_result


def read_txt_file(file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return []
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = []
    for line in lines:
        # 使用strip()函数去除每行的换行符，然后使用split()函数以逗号分隔每行
        row = line.strip().split(',')
        data.append(row)

    return data
