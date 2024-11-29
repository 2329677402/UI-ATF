#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@ Date        : 2024/11/6 上午12:09
@ Author      : Poco Ray
@ File        : __init__.py
@ Description : 读取config.yaml配置文件
"""
from utils.read_tool.read_file import YamlReader
from config.setting import ensure_path_sep
from utils.other_tool.models import Config

_data = YamlReader(ensure_path_sep("/config/config.yaml")).read_yaml()
config = Config(**_data)

print(config.lark.secret)