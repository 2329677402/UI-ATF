import pytest
from tests.test_base_case import BaseCaseWeb
from utils.log_tool.log_control import INFO, ERROR


class TestWebLogin(BaseCaseWeb):
    """Web登录测试类"""

    @pytest.fixture(autouse=True)
    def setup_web_test(self, web_driver):
        """
        设置测试环境
        :param web_driver: web driver fixture
        """
        self.driver = web_driver
        self.base_util = self.setup_base_util()
        yield
        # 测试结束后的清理工作可以放在这里

    @pytest.mark.web
    @pytest.mark.login
    def test_web_login(self):
        """测试Web端登录功能"""
        try:
            INFO.logger.info("开始执行 test_web_login 测试")
            self.login()
            self.base_util.take_screenshot("after_login")
            
            assert self.base_util.is_element_present(
                self.create_locator(".user-info")
            ), "登录失败，未找到用户信息元素"
            
        except Exception as e:
            ERROR.logger.error(f"测试执行失败: {str(e)}")
            self.base_util.take_screenshot("login_failed")
            raise
