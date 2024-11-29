#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@ Date        : 2024/11/26 下午5:31
@ Author      : Administrator
@ File        : base_case_web.py
@ Description : 功能描述
"""
import os
from selenium.webdriver.common.by import By

from utils.base_util import BaseUtil


class BaseCaseWeb(BaseUtil):
    def setUp(self):
        self.driver.maximize_window()
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.set_download_prefs(os.path.join(os.path.dirname(__file__), 'datas'))

    def tearDown(self):
        pass

    def login(self, url, username, password):
        self.open(url)
        self.type(By.ID, 'username', username)
        self.type(By.ID, 'password', password)
        self.type(By.ID, 'login_button', 'Login')
