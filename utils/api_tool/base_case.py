from typing import Any, List
from appium.webdriver.webdriver import WebDriver as AppDriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from utils.api_tool.base_util import BaseUtil


class BaseCase:
    """测试基类"""
    driver: WebDriver = None
    app_driver: AppDriver = None
    _util: BaseUtil = None

    def setup_actions(self):
        """初始化测试环境"""
        if not hasattr(self, 'driver') or self.driver is None:
            raise ValueError("执行测试前必须初始化driver对象!")
        self._util = BaseUtil(self.driver)

    # ====== 自定义方法 ======
    def open(self, url) -> None:
        """打开网页"""
        self._util.open(url)

    def click(self, selector, by='css_selector', delay=0) -> None:
        """点击元素"""
        self._util.click(selector, by, delay)

    def type(self, selector, text, by='css_selector', timeout=None, retry: bool = False):
        """输入文本"""
        self._util.type(selector, text, by, timeout, retry)

    def is_element_present(self, selector, by='css_selector') -> bool:
        """检查元素是否存在"""
        return self._util.is_element_present(selector, by)

    def take_screenshot(self, name) -> str:
        """截取屏幕截图"""
        return self._util.take_screenshot(name)

    def sleep(self, seconds=2) -> None:
        """暂停执行"""
        self._util.sleep(seconds)

    def send_keys(self, selector, text, by='css_selector') -> None:
        """输入文本"""
        self._util.find_element(selector, by).send_keys(text)

    def start_app(self, app_package) -> None:
        """启动App"""
        self._util.start_app(app_package)

    def close_app(self, app_package) -> None:
        """关闭App"""
        self._util.close_app(app_package)

    @property
    def current_package(self) -> str:
        """获取当前App包名"""
        return self._util.current_package()

    @property
    def current_activity(self) -> str:
        """获取当前App活动名"""
        return self._util.current_activity()

    def install_app(self, app_path) -> None:
        """安装App"""
        self._util.install_app(app_path)

    def uninstall_app(self, app_package) -> None:
        """卸载App"""
        self._util.uninstall_app(app_package)

    def is_app_installed(self, app_package) -> bool:
        """检查App是否安装"""
        return self._util.is_app_installed(app_package)

    def background_app(self, seconds) -> None:
        """App后台运行"""
        self._util.background_app(seconds)

    @property
    def get_network_connect(self) -> int:
        """
        获取手机网络连接类型
            +--------------------+------+------+---------------+
            | Value (Alias)      | Data | Wifi | Airplane Mode |
            +====================+======+======+===============+
            | 0 (None)           | 0    | 0    | 0             |
            +--------------------+------+------+---------------+
            | 1 (Airplane Mode)  | 0    | 0    | 1             |
            +--------------------+------+------+---------------+
            | 2 (Wifi only)      | 0    | 1    | 0             |
            +--------------------+------+------+---------------+
            | 4 (Data only)      | 1    | 0    | 0             |
            +--------------------+------+------+---------------+
            | 6 (All network on) | 1    | 1    | 0             |
            +--------------------+------+------+---------------+
        """
        return self._util.get_network_connect()

    def set_network_connect(self, connect_type) -> None:
        """设置手机网络连接类型"""
        self._util.set_network_connect(connect_type)

    def press_keycode(self, keycode) -> None:
        """按键事件"""
        self._util.press_keycode(keycode)

    def open_notify(self) -> None:
        """打开通知栏"""
        self._util.open_notify()

    @property
    def contexts(self) -> list:
        """获取所有上下文"""
        return self._util.contexts()

    def switch_to(self, context) -> None:
        """切换上下文"""
        self._util.switch_to(context)

    # ====== Selenium ======
    def get(self, url) -> None:
        """访问URL"""
        self.driver.get(url)

    def find_element(self, by, value) -> WebElement:
        """查找单个元素"""
        return self.driver.find_element(by, value)

    def find_elements(self, by, value) -> List[WebElement]:
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

    @property
    def current_window_handle(self) -> str:
        """获取当前窗口句柄"""
        return self.driver.current_window_handle
