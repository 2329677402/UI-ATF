from typing import Any
from selenium.webdriver.remote.webdriver import WebDriver
from utils.api_tool.base_util import BaseUtil


class BaseCase:
    """测试基类"""
    driver: WebDriver = None
    _util: BaseUtil = None

    def setup_actions(self):
        """初始化测试环境"""
        if not hasattr(self, 'driver') or self.driver is None:
            raise ValueError("执行测试前必须初始化driver对象")
        self._util = BaseUtil(self.driver)

    def __getattr__(self, name: str) -> Any:
        """代理到BaseUtil的方法"""
        if self._util is None:
            raise ValueError("工具类未初始化")
        return getattr(self._util, name)

    def __dir__(self) -> list[str]:
        """自定义类的属性列表，用于IDE提示"""
        attrs = set(super().__dir__())
        if self._util is not None:
            attrs.update(dir(self._util))
        return sorted(attrs)

    # 显式声明一些常用方法的类型提示
    def click(self, *args, **kwargs): 
        """点击元素"""
        return self._util.click(*args, **kwargs) if self._util else None

    def type(self, *args, **kwargs): 
        """输入文本"""
        return self._util.type(*args, **kwargs) if self._util else None

    def open(self, *args, **kwargs): 
        """打开URL"""
        return self._util.open(*args, **kwargs) if self._util else None

    def get(self, *args, **kwargs):
        """打开URL"""
        return self._util.get(*args, **kwargs) if self._util else None

    def take_screenshot(self, *args, **kwargs): 
        """截取屏幕截图"""
        return self._util.take_screenshot(*args, **kwargs) if self._util else None

    def is_element_present(self, *args, **kwargs): 
        """检查元素是否存在"""
        return self._util.is_element_present(*args, **kwargs) if self._util else None