#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@ Date        : 2024/12/4 下午8:40
@ Author      : Poco Ray
@ File        : base_case.py
@ Description : 测试基类
"""

from typing import Any, List, Optional, Self, Tuple
from appium.webdriver.webdriver import WebDriver as AppDriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from utils.api_tool.base_util import BaseUtil


class BaseCase:
    """测试基类"""
    driver: WebDriver or AppDriver = None
    _util: BaseUtil = None

    def setup_actions(self):
        """初始化测试环境"""
        if not hasattr(self, 'driver') or self.driver is None:
            raise ValueError("执行测试前必须初始化driver对象!")
        self._util = BaseUtil(self.driver)

    def open(self, url: str) -> None:
        """
        打开网页

        :param url: 要打开的网页URL
        :Usage:
            self.open("https://www.google.com")
        """
        self._util.open(url)

    def click(self, selector: str, by: str = 'css_selector', delay: int = 0) -> None:
        """
        点击元素

        :param selector: 元素选择器
        :param by: 定位方式，默认为'css_selector'
        :param delay: 点击前的延迟时间，默认为0秒
        :Usage:
            self.click("#submit_button")
        """
        self._util.click(selector, by, delay)

    def type(self, selector: str, text: str, by: str = 'css_selector', timeout: Optional[int] = None,
             retry: bool = False) -> None:
        """
        输入文本

        :param selector: 元素选择器
        :param text: 要输入的文本
        :param by: 定位方式，默认为'css_selector'
        :param timeout: 超时时间，默认为None
        :param retry: 是否重试，默认为False
        :Usage:
            self.type("#input_field", "example text"，timeout=10，retry=True)
        """
        self._util.type(selector, text, by, timeout, retry)

    def is_element_present(self, selector: str, by: str = 'css_selector') -> bool:
        """
        检查元素是否存在

        :param selector: 元素选择器
        :param by: 定位方式，默认为'css_selector'
        :return: 元素是否存在
        :Usage:
            is_present = self.is_element_present("#element_id")
        """
        return self._util.is_element_present(selector, by)

    def take_screenshot(self, name: str) -> str:
        """
        截取屏幕截图

        :param name: 截图名称
        :return: 截图文件路径
        :Usage:
            screenshot_path = self.take_screenshot("screenshot_name")
        """
        return self._util.take_screenshot(name)

    def sleep(self, seconds: int = 2) -> None:
        """
        暂停执行

        :param seconds: 暂停时间，默认为2秒
        :Usage:
            self.sleep(5)
        """
        self._util.sleep(seconds)

    def send_keys(self, selector: str, text: str, by: str = 'css_selector') -> None:
        """
        输入文本

        :param selector: 元素选择器
        :param text: 要输入的文本
        :param by: 定位方式，默认为'css_selector'
        :Usage:
            self.send_keys("#input_field", "example text")
        """
        self._util.find_element(selector, by).send_keys(text)

    def start_app(self, app_package: str) -> None:
        """
        启动App

        :param app_package: App包名
        :Usage:
            self.start_app("com.example.app")
        """
        self._util.start_app(app_package)

    def close_app(self, app_package: str) -> None:
        """
        关闭App

        :param app_package: App包名
        :Usage:
            self.close_app("com.example.app")
        """
        self._util.close_app(app_package)

    @property
    def current_package(self) -> str:
        """
        获取当前App包名

        :return: 当前App包名, 如：com.android.browser
        :Usage:
            print(self.current_package)
        """
        return self._util.current_package()

    @property
    def current_activity(self) -> str:
        """
        获取当前App活动名

        :return: 当前App活动名，如：.BrowserActivity
        :Usage:
            print(self.current_activity)
        """
        return self._util.current_activity()

    def install_app(self, app_path: str) -> None:
        """
        安装App

        :param app_path: App路径
        :Usage:
            self.install_app("/path/to/app.apk")
        """
        self._util.install_app(app_path)

    def uninstall_app(self, app_package: str) -> None:
        """
        卸载App

        :param app_package: App包名
        :Usage:
            self.uninstall_app("com.example.app")
        """
        self._util.uninstall_app(app_package)

    def is_app_installed(self, app_package: str) -> bool:
        """
        检查App是否安装

        :param app_package: App包名
        :return: App是否安装
        :Usage:
            is_installed = self.is_app_installed("com.example.app")
        """
        return self._util.is_app_installed(app_package)

    def background_app(self, seconds: int) -> None:
        """
        App后台运行

        :param seconds: 后台运行时间，单位为秒
        :Usage:
            self.background_app(5)
        """
        self._util.background_app(seconds)

    @property
    def get_network_connect(self) -> int:
        """
        获取手机网络连接类型

        :return: 网络连接类型
        :Usage:
            network_type = self.get_network_connect

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

    def set_network_connect(self, connect_type: int) -> None:
        """
        设置手机网络连接类型

        :param connect_type: 网络连接类型
        :Usage:
            self.set_network_connect(2)
        """
        self._util.set_network_connect(connect_type)

    def press_keycode(self, keycode: int, metastate: Optional[int] = None, flags: Optional[int] = None) -> None:
        """
        按键事件

        :param keycode: 按键码
        :param metastate: 元状态，如：1 表示 META_SHIFT_ON
        :param flags: 标志，如：0 表示没有特殊标志
        :Usage:
            self.press_keycode(66)

        常用按键码列表：
        +--------------------+------------------+----------------------+
        | 键码                | 名称             | 描述                 |
        +====================+==================+======================+
        | 3                  | HOME             | 返回主屏幕            |
        +--------------------+------------------+----------------------+
        | 4                  | BACK             | 返回                 |
        +--------------------+------------------+----------------------+
        | 24                 | VOLUME_UP        | 增加音量             |
        +--------------------+------------------+----------------------+
        | 25                 | VOLUME_DOWN      | 减少音量             |
        +--------------------+------------------+----------------------+
        | 26                 | POWER            | 电源                 |
        +--------------------+------------------+----------------------+
        | 27                 | CAMERA           | 拍照                 |
        +--------------------+------------------+----------------------+
        | 66                 | ENTER            | 回车                 |
        +--------------------+------------------+----------------------+
        | 67                 | DELETE           | 删除                 |
        +--------------------+------------------+----------------------+
        | 82                 | MENU             | 菜单                 |
        +--------------------+------------------+----------------------+
        | 122                | MOVE_HOME        | 光标移动到行首        |
        +--------------------+------------------+----------------------+
        | 123                | MOVE_END         | 光标移动到行尾        |
        +--------------------+------------------+----------------------+
        | 187                | APP_SWITCH       | 切换应用             |
        +--------------------+------------------+----------------------+
        """
        self._util.press_keycode(keycode, metastate, flags)

    def open_notify(self) -> None:
        """
        打开通知栏

        :Usage:
            self.open_notify()
        """
        self._util.open_notify()

    @property
    def contexts(self) -> List[str]:
        """
        获取所有上下文名称

        :return: 上下文列表，如：['NATIVE_APP', 'WEBVIEW_com.example.app']
        :Usage:
            contexts = self.contexts
        """
        return self._util.contexts()

    def switch_to_context(self, context: str) -> None:
        """
        切换上下文

        :param context: 上下文名称
        :Usage:
            self.switch_to_context("WEBVIEW_com.example.app")
        """
        self._util.switch_to_context(context)

    def find_element(self, selector: str, by: str = 'css_selector', timeout: Optional[int] = None) -> WebElement:
        """
        查找单个元素

        :param selector: 元素选择器
        :param by: 定位方式，默认为'css_selector'
        :param timeout: 超时时间，默认为None
        :return: WebElement对象
        :Usage:
            element = self.find_element("#element_id")
        """
        return self._util.find_element(selector, by, timeout)

    def find_elements(self, selector: str, by: str = 'css_selector', timeout: Optional[int] = None) -> List[WebElement]:
        """
        查找多个元素

        :param selector: 元素选择器
        :param by: 定位方式，默认为'css_selector'
        :param timeout: 超时时间，默认为None
        :return: WebElement对象列表
        :Usage:
            elements = self.find_elements(".element_class")
        """
        return self._util.find_elements(selector, by, timeout)

    def refresh(self) -> None:
        """
        刷新页面

        :Usage:
            self.refresh()
        """
        self._util.refresh()

    def back(self) -> None:
        """
        返回上一页

        :Usage:
            self.back()
        """
        self._util.back()

    def forward(self) -> None:
        """
        前进到下一页

        :Usage:
            self.forward()
        """
        self._util.forward()

    def close(self) -> None:
        """
        关闭当前窗口

        :Usage:
            self.close()
        """
        self._util.close()

    def quit(self) -> None:
        """
        退出浏览器

        :Usage:
            self.quit()
        """
        self._util.quit()

    def maximize_window(self) -> None:
        """
        最大化窗口

        :Usage:
            self.maximize_window()
        """
        self._util.maximize_window()

    def minimize_window(self) -> None:
        """
        最小化窗口

        :Usage:
            self.minimize_window()
        """
        self._util.minimize_window()

    def switch_to_frame(self, iframe) -> None:
        """
        切换到iframe

        :param iframe: iframe元素或索引
        :Usage:
            self.switch_to_frame("iframe_name")
        """
        self._util.switch_to_frame(iframe)

    def switch_to_default_frame(self) -> None:
        """
        切换到默认框架

        :Usage:
            self.switch_to_default_frame()
        """
        self._util.switch_to_default_frame()

    def execute_script(self, script: str, *args) -> Any:
        """
        执行JavaScript代码

        :param script: JavaScript代码
        :param args: 传递给JavaScript代码的参数
        :return: JavaScript代码的执行结果
        :Usage:
            result = self.execute_script("return document.title;")
        """
        return self._util.execute_script(script, *args)

    @property
    def current_url(self) -> str:
        """
        获取当前URL

        :return: 当前URL
        :Usage:
            url = self.current_url
        """
        return self._util.current_url()

    @property
    def title(self) -> str:
        """
        获取页面标题

        :return: 页面标题
        :Usage:
            title = self.title
        """
        return self._util.title()

    @property
    def page_source(self) -> str:
        """
        获取页面源码

        :return: 页面源码
        :Usage:
            source = self.page_source
        """
        return self._util.page_source()

    @property
    def current_window_handle(self) -> str:
        """
        获取当前窗口句柄

        :return: 当前窗口句柄
        :Usage:
            handle = self.current_window_handle
        """
        return self._util.current_window_handle()

    def tap(self, positions: List[Tuple[int, int]], duration: Optional[int] = 100) -> Self:
        """
        点击屏幕上的指定坐标

        :param positions: 一个包含 x/y 坐标的元组数组，长度最多为 5
        :param duration: 单次点击持续时间（毫秒）
        :return: BaseCase对象, 允许链式调用
        :Usage:
            self.tap([(100, 20), (100, 60), (100, 100)], 500)
        """
        self._util.tap(positions, duration)
        return self

    def drag_and_drop(self, start_element: WebElement, end_element: WebElement, pause: Optional[float] = None) -> Self:
        """
        拖拽元素

        :param start_element: 起始元素
        :param end_element: 结束元素
        :param pause: 拖拽前的暂停时间(秒)
        :return: BaseCase对象, 允许链式调用
        :Usage:
            self.drag_and_drop(el1, el2, 0.2)
        """
        self._util.drag_and_drop(start_element, end_element, pause)
        return self

    def scroll(self, start_element: WebElement, end_element: WebElement, duration: Optional[int] = None) -> Self:
        """
        滚动元素

        :param start_element: 起始元素
        :param end_element: 结束元素
        :param duration: 滚动持续时间（毫秒）
        :return: BaseCase对象, 允许链式调用
        :Usage:
            self.scroll(el1, el2, 1000)
        """
        self._util.scroll(start_element, end_element, duration)
        return self

    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: int = None) -> Self:
        """
        滑动屏幕

        :param start_x: 起始X坐标
        :param start_y: 起始Y坐标
        :param end_x: 结束X坐标
        :param end_y: 结束Y坐标
        :param duration: 持续时间（毫秒）
        :Usage:
            self.swipe(100, 200, 300, 400, 1000)
        """
        self._util.swipe(start_x, start_y, end_x, end_y, duration)
        return self
