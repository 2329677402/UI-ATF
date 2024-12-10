import pytest
from tests.test_base_case import BaseCaseWeb
from utils.log_tool.log_control import INFO, ERROR


class TestWebLogin(BaseCaseWeb):
    """Web登录测试类"""

    @pytest.mark.web
    @pytest.mark.login
    def test_web_login(self):
        """测试Web端登录功能"""
        try:
            INFO.logger.info("开始执行 test_web_login 测试")
            self.login()
            self.take_screenshot("after_login")
            current = self.current_url
            handle = self.current_window_handle
            print(f"当前URL: {current}")
            print(f"当前窗口句柄: {handle}")
            self.click("li:contains('特殊作业全过程')")
            self.sleep(1)

        except Exception as e:
            ERROR.logger.error(f"测试执行失败: {str(e)}")
            self.take_screenshot("login_failed")
            raise
