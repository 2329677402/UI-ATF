import pytest
from utils.api_tool.base_case import BaseCase
from pages.page_web.page_web_login import PageWebLogin


class BaseCaseWeb(BaseCase):
    """Web测试基类"""

    @pytest.fixture(autouse=True)
    def setup_web_test(self, web_driver):
        """设置Web测试环境"""
        self.driver = web_driver
        self.setup_actions()
        yield

    def login(self):
        """执行登录操作"""
        PageWebLogin.login(self, "http://113.194.201.66:8092/login", "admin", "yl123456")


class BaseCaseApp(BaseCase):
    """App测试基类"""

    @pytest.fixture(autouse=True)
    def setup_app_test(self, app_driver):
        """设置App测试环境"""
        self.driver = app_driver
        self.setup_actions()
        yield

    def login(self):
        """App端登录实现"""
        pass