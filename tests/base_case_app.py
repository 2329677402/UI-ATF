#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@ Date        : 2024/11/26 下午5:31
@ Author      : Administrator
@ File        : base_case_app.py
@ Description : 功能描述
"""
from selenium.webdriver.common.by import By

from utils.base_util import BaseUtil


# base_case_app.py
class BaseCaseApp(BaseUtil):
    def setUp(self):
        # App-specific setup
        pass

    def tearDown(self):
        # Close the app
        self.driver.terminate_app('com.your.package')

    def login(self, username, password):
        self.type(By.ID, 'username', username)
        self.type(By.ID, 'password', password)
        self.type(By.ID, 'login_button', 'Login')
