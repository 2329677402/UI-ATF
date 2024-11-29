#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@ Date        : 2024/11/16 下午3:40
@ Author      : Poco Ray
@ File        : setting.py
@ Description : 实现不同操作系统的路径分离, 以兼容 Windows 和 Linux 不同环境的操作系统路径.
@Explain:
    1. os.path.abspath(__file__): 返回当前文件的绝对路径
    2. os.path.dirname(): 返回当前文件的上级目录路径
    3. os.path.join(): 拼接路径
    4. os.path.expanduser(): 将path中包含的"~"和"~user"转换成用户目录
"""
import os
from typing import Text


def root_path():
    """
    :return: 项目根路径
    """
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return path


def ensure_path_sep(path: Text) -> Text:
    """
    功能: 实现不同操作系统的路径分离, 以兼容 Windows 和 Linux 不同环境的操作系统路径.
    :param path: path路径(任意一种操作系统路径的格式都可以).
    :return: 视操作系统返回不同的路径, 路径分隔符自动转换为当前操作系统的路径分隔符.
    """
    if "/" in path:
        path = os.sep.join(path.split("/"))

    if "\\" in path:
        path = os.sep.join(path.split("\\"))

    return root_path() + path


# 测试
if __name__ == '__main__':
    print(root_path())
    print(ensure_path_sep("\\report\\html"))
    print(ensure_path_sep("/report/html"))