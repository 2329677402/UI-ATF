#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@ Date        : 2024/12/1 下午8:06
@ Author      : Poco Ray
@ File        : test_app_login.py
@ Description : 功能描述
"""
import pytest
from tests.test_base_case import BaseCaseApp
from utils.log_tool.log_control import INFO, ERROR


class TestAppLogin(BaseCaseApp):
    """App登录测试类"""

    @pytest.mark.app
    @pytest.mark.login
    def test_app_login(self):
        """测试App端登录功能"""
        try:
            INFO.logger.info("开始执行 test_app_login 测试")
            self.login()
            self.take_screenshot("after_login")
            self.close_app("com.android.browser")
            self.start_app("com.tongjiwisdom")

        except Exception as e:
            ERROR.logger.error(f"测试执行失败: {str(e)}")
            self.take_screenshot("login_failed")
            raise
