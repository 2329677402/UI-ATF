import pytest

from config.setting import root_path
from utils.api_tool.base_case import BaseCase
from pages.page_web.page_web_login import PageWebLogin
import os


class BaseCaseWeb(BaseCase):
    """Web测试基类"""

    @pytest.fixture(autouse=True)
    def setup_web_test(self, web_driver):
        """设置Web测试环境"""
        # 清理历史截图
        screenshots_path = os.path.join(root_path(), 'datas', 'screenshots')
        if os.path.exists(screenshots_path):
            import shutil
            shutil.rmtree(screenshots_path)
        os.makedirs(screenshots_path, exist_ok=True)
        
        self.driver = web_driver
        self.setup_actions()
        yield

    def login(self):
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