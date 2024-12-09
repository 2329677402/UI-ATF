#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@ Date        : 12/09/2024 5:24 PM
@ Author      : Administrator
@ File        : test_base_case.py
@ Description : Web-side test base class and App-side test base class.
"""
import pytest
from utils.api_tool.base_case import BaseCase
from pages.page_web.page_web_login import PageWebLogin


class BaseCaseWeb(BaseCase):
    """ Web-side test base class """

    @pytest.fixture(autouse=True)
    def setup_web_test(self, web_driver) -> None:
        """
        Set up the Web test environment.

        :param web_driver: Web driver instance.
        """
        self.driver = web_driver
        self.setup_actions()
        yield

    def login(self):
        """ Web login implementation. """
        PageWebLogin.login(self, "http://113.194.201.66:8092/login", "admin", "yl123456")


class BaseCaseApp(BaseCase):
    """ App-side test base class """

    @pytest.fixture(autouse=True)
    def setup_app_test(self, app_driver):
        """
        Set up the App test environment.

        :param app_driver: App driver instance.
        """
        self.driver = app_driver
        self.setup_actions()
        yield

    def login(self):
        """ App login implementation. """
        pass
