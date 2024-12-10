#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@ Date        : 12/10/2024 10:55 AM
@ Author      : Administrator
@ File        : __init__.py
@ Description : Read the 'config.yaml' configuration file.
"""
from common.setting import Settings
from utils.other_tool.models import Config
from utils.read_tool.read_file import YamlReader

settings = Settings()
try:
    _data = YamlReader(settings.get_global_config('config_dir')).read_yaml()
except FileNotFoundError:
    _data = {}  # If the file does not exist, set it to an empty dictionary.

config = Config(**_data)

if __name__ == '__main__':
    print(config)
