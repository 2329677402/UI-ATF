#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@ Date        : 2024/11/16 下午6:08
@ Author      : Poco Ray
@ File        : get_local_ip.py
@ Description : 获取本机ip地址
"""
import socket


def get_host_ip():
    """
    :return: 本机ip地址
    """
    _s = None
    try:
        _s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        _s.connect(('8.8.8.8', 80))
        l_host = _s.getsockname()[0]
    finally:
        _s.close()

    return l_host

# 测试
if __name__ == '__main__':
    print(get_host_ip())