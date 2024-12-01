import pytest
from tests.test_base_case import BaseCaseApp


class TestAppLogin(BaseCaseApp):
    """App登录测试类"""
    
    def setup_method(self, method):
        """每个测试方法执行前的设置"""
        super().__init__()

    @pytest.fixture(autouse=True)
    def init_driver(self, app_driver):
        """初始化driver"""
        self.setup_test(app_driver)
        yield
        if hasattr(self, 'driver'):
            self.quit()

    @pytest.mark.app
    def test_app_login(self):
        """测试App端登录功能"""
        try:
            self.take_screenshot("before_login")
            self.login()
            self.take_screenshot("after_login")
            
            assert self.is_element_present(
                self.create_locator(".login-success")
            ), "登录失败"
            
        except Exception as e:
            self.take_screenshot("login_failed")
            raise
