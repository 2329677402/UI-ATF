#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@ Date        : 2024/11/6 上午12:09
@ Author      : Poco Ray
@ File        : __init__.py
@ Description : 读取config.yaml配置文件
"""
from utils.read_tool.read_file import YamlReader
from common.setting import ensure_path_sep
from utils.other_tool.models import Config

try:
    _data = YamlReader(ensure_path_sep("/common/config.yaml")).read_yaml()
except FileNotFoundError:
    _data = {}  # 如果文件不存在，使用空字典作为默认值

config = Config(**_data)
