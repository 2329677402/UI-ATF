#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@ Date        : 2024/11/26 下午5:38
@ Author      : Administrator
@ File        : test_app_login.py
@ Description : 功能描述
"""
# test_app_login.py
from tests.base_case_app import BaseCaseApp


class TestAppLogin(BaseCaseApp):
    def test_login(self):
        self.login('user', 'pass')
        # Assert something after login
