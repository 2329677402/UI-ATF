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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.pointer_input import PointerInput


class TestAppLogin(BaseCaseApp):
    """App登录测试类"""

    @pytest.mark.app
    @pytest.mark.login
    def test_app_login(self):
        """测试App端登录功能"""
        try:
            INFO.logger.info("开始执行 test_app_login 测试")
            self.login()
            self.close_app("com.android.browser")
            self.start_app("com.tongjiwisdom")
            self.sleep(3)
            print(self.current_package)
            print(self.current_activity)

            contexts = self.driver.contexts
            print(contexts)
            self.switch_to_context(contexts[-1])
            # ActionChains(self.driver).w3c_actions.pointer_action.click_and_hold().perform()
            username = self.find_element('//*[@text="请输入账号"]', by='xpath')
            password = self.find_element("//*[@text='请输入密码']", by='xpath')
            username.send_keys("admin")
            password.send_keys("yl123456")
            self.click("//*[@text='登录']", by='xpath')
            self.sleep(3)

        except Exception as e:
            ERROR.logger.error(f"测试执行失败: {str(e)}")
            self.take_screenshot("login_failed")
            raise
