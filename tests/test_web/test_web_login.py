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
            
        except Exception as e:
            ERROR.logger.error(f"测试执行失败: {str(e)}")
            self.take_screenshot("login_failed")
            raise
