#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@ Date        : 2024/11/16 下午5:36
@ Author      : Poco Ray
@ File        : get_file.py
@ Description : 功能描述
"""
import os
from common.setting import ensure_path_sep


def get_all_files(file_path, yaml_data_switch=False) -> list:
    """
    功能: 获取文件路径
    :param file_path: 目录路径
    :param yaml_data_switch: 是否过滤文件为 yaml格式， True则过滤
    :return: 文件路径列表
    """
    filename = []
    # 获取所有文件下的子文件名称
    for root, dirs, files in os.walk(file_path):
        for _file_path in files:
            path = os.path.join(root, _file_path)
            if yaml_data_switch:
                if 'yaml' in path or '.yml' in path:
                    filename.append(path)
            else:
                filename.append(path)
    return filename


# 测试
if __name__ == '__main__':
    print(get_all_files(file_path=ensure_path_sep('/data/locator'), yaml_data_switch=True))
