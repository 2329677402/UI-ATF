#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@ Date        : 2024/11/26 下午5:38
@ Author      : Administrator
@ File        : test_web_login.py
@ Description : 功能描述
"""
# test_web_login.py
from tests.base_case_web import BaseCaseWeb


class TestWebLogin(BaseCaseWeb):
    def test_login(self):
        self.login('https://example.com/login', 'user', 'pass')
        # Assert something after login

