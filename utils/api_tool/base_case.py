from typing import Any, Union, List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from utils.api_tool.base_util import BaseUtil
from utils.api_tool.locator import Locator


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

    # ====== 封装的自定义方法 ======
    def open(self, url: str) -> None:
        """打开网页"""
        self._util.get(url)

    def click(self, selector: Union[str, tuple, Locator]) -> None:
        """点击元素"""
        self._util.click(selector)

    def type(self, selector: Union[str, tuple, Locator], text: str) -> None:
        """输入文本"""
        self._util.type(selector, text)

    def is_element_present(self, selector: Union[str, tuple, Locator]) -> bool:
        """检查元素是否存在"""
        return self._util.is_element_present(selector)

    def take_screenshot(self, name: str) -> str:
        """截取屏幕截图"""
        return self._util.take_screenshot(name)

    # ====== Selenium原生方法 ======
    def get(self, url: str) -> None:
        """访问URL"""
        self.driver.get(url)

    def find_element(self, by: str, value: str) -> WebElement:
        """查找单个元素"""
        return self.driver.find_element(by, value)

    def find_elements(self, by: str, value: str) -> List[WebElement]:
        """查找多个元素"""
        return self.driver.find_elements(by, value)

    def refresh(self) -> None:
        """刷新页面"""
        self.driver.refresh()

    def back(self) -> None:
        """返回上一页"""
        self.driver.back()

    def forward(self) -> None:
        """前进到下一页"""
        self.driver.forward()

    def close(self) -> None:
        """关闭当前窗口"""
        self.driver.close()

    def quit(self) -> None:
        """退出浏览器"""
        self.driver.quit()

    def maximize_window(self) -> None:
        """最大化窗口"""
        self.driver.maximize_window()

    def minimize_window(self) -> None:
        """最小化窗口"""
        self.driver.minimize_window()

    def switch_to_frame(self, frame_reference) -> None:
        """切换到iframe"""
        self.driver.switch_to.frame(frame_reference)

    def switch_to_default_content(self) -> None:
        """切换到默认内容"""
        self.driver.switch_to.default_content()

    def execute_script(self, script: str, *args) -> Any:
        """执行JavaScript代码"""
        return self.driver.execute_script(script, *args)

    @property
    def current_url(self) -> str:
        """获取当前URL"""
        return self.driver.current_url

    @property
    def title(self) -> str:
        """获取页面标题"""
        return self.driver.title

    @property
    def page_source(self) -> str:
        """获取页面源码"""
        return self.driver.page_source
