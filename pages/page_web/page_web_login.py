#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@ Date        : 2024/12/1 下午7:42
@ Author      : Poco Ray
@ File        : page_web_login.py
@ Description : 功能描述
"""
input_username = "input[placeholder='账号']"
input_password = "input[placeholder='密码']"
button_login = "button[type='button']"


class PageWebLogin:
    """Web登录页面"""

    @classmethod
    def login(cls, driver, url, username, password):
        """Web端登录实现"""
        driver.open(url)
        driver.type(input_username, username)
        driver.type(input_password, password)
        driver.click(button_login)
