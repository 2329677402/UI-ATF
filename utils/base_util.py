#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@ Date        : 2024/11/26 下午5:29
@ Author      : Administrator
@ File        : base_util.py
@ Description : 功能描述
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BaseUtil:
    def __init__(self, driver):
        self.driver = driver

    def type(self, by=By.CSS_SELECTOR, locator='', text='', timeout=10, retry=False):
        """
        Types text into an element, clearing it first.
        """
        max_attempts = 2 if retry else 1
        for _ in range(max_attempts):
            try:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((by, locator))
                )
                element.clear()
                element.send_keys(text)
                return
            except TimeoutException:
                if retry:
                    continue
                else:
                    raise

    def open(self, url):
        """
        Opens a URL and waits for the page to load.
        """
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")
