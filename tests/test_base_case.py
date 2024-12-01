import pytest

from utils.api_tool.base_util import BaseUtil
from utils.api_tool.locator import Locator


class BaseCase:
    """测试基类"""
    driver = None
    base_util = None

    def setup_base_util(self):
        """初始化 base_util"""
        if self.driver is None:
            raise ValueError("Driver must be initialized before running tests")
        return BaseUtil(self.driver)

    @staticmethod
    def create_locator(value: str, method: str = 'css_selector') -> Locator:
        """创建元素定位器"""
        return Locator(method=method, value=value)


class BaseCaseWeb(BaseCase):
    """Web测试基类"""

    def login(self):
        """Web端登录实现"""
        self.base_util.open("http://113.194.201.66:8092/login")

        # 使用create_locator创建Locator对象
        username_locator = self.create_locator("input[placeholder='账号']")
        password_locator = self.create_locator("input[placeholder='密码']")
        login_button_locator = self.create_locator("button[type='button']")

        # 使用Locator对象进行操作
        self.base_util.type(username_locator, "admin")
        self.base_util.type(password_locator, "yl123456")
        self.base_util.click(login_button_locator)


class BaseCaseApp(BaseCase):
    """App测试基类"""

    def login(self):
        """App端登录实现"""
        pass
