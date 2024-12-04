#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@ Date        : 2024/12/2 下午9:42
@ Author      : Poco Ray
@ File        : base_util.py
@ Description : 基础操作封装
"""
import os
import time
import shutil
from datetime import datetime
from typing import List, Any, Optional, Self, Tuple
from common.setting import root_path, Settings
from utils.log_tool.log_control import INFO, ERROR
from appium.webdriver.webdriver import WebDriver as AppDriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, ElementClickInterceptedException
from selenium.webdriver.remote.webelement import WebElement
from utils.api_tool.selector_util import SelectorUtil


class BaseUtil:
    """基础操作封装"""

    def __init__(self, driver: AppDriver or WebDriver):
        """
        初始化工具类
        :param driver: WebDriver实例
        """
        self._driver = driver
        self.settings = Settings()
        config = self.settings.global_config

        # 保存常用配置参数
        self._timeout = config['webdriver_timeout']
        self._poll_frequency = config['webdriver_poll_frequency']

        self.wait = WebDriverWait(
            driver,
            self._timeout,
            poll_frequency=self._poll_frequency
        )

        # 清理历史数据
        if config.get('clean_screenshots', True):
            self._clean_screenshots()
        if config.get('clean_logs', True):
            self._clean_logs()

    def find_element(self, selector: str, by: str = 'css_selector', timeout=None) -> WebElement:
        """
        查找元素
        :param selector: 选择器
        :param by: 定位方式
        :param timeout: 超时时间
        :return: WebElement对象
        """
        temp_wait = self.wait if timeout is None else WebDriverWait(
            self._driver,
            timeout,
            poll_frequency=self._poll_frequency
        )

        try:
            locator = SelectorUtil.get_selenium_locator(selector, by)
            element = temp_wait.until(
                EC.presence_of_element_located(locator)
            )
            INFO.logger.info(f"成功查找到元素: {selector} (by={by})")
            return element
        except TimeoutException:
            ERROR.logger.error(f"查找元素超时: {selector} (by={by})")
            self.take_screenshot("find_element_timeout")
            raise
        except Exception as e:
            ERROR.logger.error(f"查找元素失败: {selector} (by={by}), 错误: {str(e)}")
            self.take_screenshot("find_element_error")
            raise

    def find_elements(self, selector: str, by: str = 'css_selector', timeout=None) -> List[WebElement]:
        """
        查找多个元素
        :param selector: 选择器
        :param by: 定位方式
        :param timeout: 超时时间
        :return: WebElement对象列表
        """
        temp_wait = self.wait if timeout is None else WebDriverWait(
            self._driver,
            timeout,
            poll_frequency=self._poll_frequency
        )

        try:
            locator = SelectorUtil.get_selenium_locator(selector, by)
            elements = temp_wait.until(
                EC.presence_of_all_elements_located(locator)
            )
            INFO.logger.info(f"成功查找到元素: {selector} (by={by})")
            return elements
        except TimeoutException:
            ERROR.logger.error(f"查找元素超时: {selector} (by={by})")
            self.take_screenshot("find_elements_timeout")
            raise
        except Exception as e:
            ERROR.logger.error(f"查找元素失败: {selector} (by={by}), 错误: {str(e)}")
            self.take_screenshot("find_elements_error")
            raise

    def click(self, selector: str, by: str = 'css_selector', delay: int = 0) -> None:
        """
        点击元素
        :param selector: 选择器
        :param by: 定位方式
        :param delay: 点击前的延迟时间(秒)
        """
        max_attempts = 3  # 最大重试次数
        attempt = 0
        last_exception = None

        while attempt < max_attempts:
            try:
                # 等待任何可能的Ajax请求完成
                script = (
                    "return (typeof jQuery !== 'undefined') ? "
                    "jQuery.active == 0 : true"
                )
                self._driver.execute_script(script)

                locator = SelectorUtil.get_selenium_locator(selector, by)

                # 等待元素存在、可见并可点击
                self.wait.until(EC.presence_of_element_located(locator))
                self.wait.until(EC.visibility_of_element_located(locator))
                element = self.wait.until(EC.element_to_be_clickable(locator))

                # 使用JavaScript滚动到元素位置，不使用smooth效果
                self._driver.execute_script(
                    "arguments[0].scrollIntoView(true);",
                    element
                )

                if delay > 0:
                    time.sleep(delay)  # 仅在明确要求时等待

                # 尝试点击
                try:
                    element.click()
                except ElementClickInterceptedException:
                    # 如果普通点击失败，尝试JavaScript点击
                    self._driver.execute_script("arguments[0].click();", element)

                INFO.logger.info(f"成功点击元素: {selector} (by={by})")
                return

            except TimeoutException as e:
                last_exception = e
                attempt += 1
                continue
            except Exception as e:
                last_exception = e
                attempt += 1
                continue

        # 如果所有重试都失败了
        ERROR.logger.error(f"点击元素失败(重试{max_attempts}次后): {selector} (by={by})")
        self.take_screenshot("click_error")

        # 记录页面源码以便调试
        try:
            page_source = self._driver.page_source
            ERROR.logger.error(f"页面源码: {page_source}")
        except Exception as e:
            ERROR.logger.error(f"获取页面源码失败: {str(e)}")

        raise last_exception

    def type(self, selector: str, text: str, by: str = 'css_selector', timeout: int = None, retry: bool = False):
        """
        清空并输入文本
        :param selector: 选择器
        :param text: 要输入的文本
        :param by: 定位方式
        :param timeout: 超时时间
        :param retry: 是否重试
        """
        try:
            element = self.find_element(selector, by, timeout)
            element.clear()
            element.send_keys(text)
            INFO.logger.info(f"成功输入文本: {text} 到元素: {selector} (by={by})")
        except TimeoutException:
            ERROR.logger.error(f"输入文本超时: {text} 到元素: {selector} (by={by})")
            self.take_screenshot("type_timeout")
            if retry:
                self.type(selector, text, by, timeout, retry=False)
            else:
                raise
        except Exception as e:
            ERROR.logger.error(f"输入文本失败: {text} 到元素: {selector} (by={by}), 错误: {str(e)}")
            self.take_screenshot("type_error")
            raise

    def is_element_present(self, selector: str, by: str = 'css_selector') -> bool:
        """
        检查元素是否存在
        :param selector: 选择器
        :param by: 定位方式
        :return: 元素是否存在
        """
        try:
            self.find_element(selector, by)
            return True
        except TimeoutException:
            return False
        except Exception as e:
            ERROR.logger.error(f"检查元素存在时失败: {selector} (by={by}), 错误: {str(e)}")
            return False

    def take_screenshot(self, name: str, wait: Optional[float] = None):
        """
        截取当前页面截图
        :param name: 截图名称
        :param wait: 截图前的等待时间（秒）
        """
        try:
            if wait:
                time.sleep(wait)  # 等待指定的秒数

            # 确保目录存在
            screenshots_dir = os.path.join(root_path(), 'datas', 'screenshots')
            os.makedirs(screenshots_dir, exist_ok=True)

            # 生成文件名
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{name}_{timestamp}.png"

            # 使用绝对路径
            filepath = os.path.join(screenshots_dir, filename)

            # 保存截图
            self._driver.save_screenshot(filepath)
            INFO.logger.info(f"截图保存至: {filepath}")
            return filepath
        except Exception as e:
            ERROR.logger.error(f"截图失败: {str(e)}")
            return None

    @staticmethod
    def _clean_screenshots():
        """清理历史截图"""
        screenshots_path = os.path.join(root_path(), 'datas', 'screenshots')
        if os.path.exists(screenshots_path):
            shutil.rmtree(screenshots_path)
        os.makedirs(screenshots_path, exist_ok=True)
        INFO.logger.info("历史截图清理完成")

    @staticmethod
    def _clean_logs():
        """清理历史日志"""
        try:
            logs_path = os.path.join(root_path(), 'logs')
            if not os.path.exists(logs_path):
                os.makedirs(logs_path)
                return

            # 获取当前日期
            today = datetime.now().date()

            # 遍历日志目录
            for filename in os.listdir(logs_path):
                if not filename.endswith('.log'):
                    continue

                file_path = os.path.join(logs_path, filename)
                try:
                    # 从文件名中提取日期（格式：xxx-2024-01-01.log）
                    date_str = filename.split('-', 1)[1].split('.')[0]
                    file_date = datetime.strptime(date_str, '%Y-%m-%d').date()

                    # 如果不是今天的日志，则删除
                    if file_date < today:
                        os.remove(file_path)
                        INFO.logger.info(f"已删除历史日志文件: {filename}")
                except (ValueError, IndexError):
                    continue
                except Exception as e:
                    ERROR.logger.error(f"清理日志文件时发生错误: {str(e)}")

            INFO.logger.info("历史日志清理完成")
        except Exception as e:
            ERROR.logger.error(f"清理日志目录时发生错误: {str(e)}")

    def open(self, url: str):
        """
        打开URL
        :param url: 要打开的URL
        """
        try:
            self._driver.get(url)
            INFO.logger.info(f"成功打开URL: {url}")
        except TimeoutException:
            ERROR.logger.error(f"打开URL超时: {url}")
            self.take_screenshot("open_url_timeout")
            raise
        except WebDriverException as e:
            ERROR.logger.error(f"打开URL时发生WebDriver异常: {url}, 异常信息: {str(e)}")
            self.take_screenshot("open_url_exception")
            raise
        except Exception as e:
            ERROR.logger.error(f"打开URL时发生未知异常: {url}, 异常信息: {str(e)}")
            self.take_screenshot("open_url_unknown_exception")
            raise

    @staticmethod
    def sleep(seconds: int) -> None:
        """暂停执行"""
        time.sleep(seconds)

    def start_app(self, app_package: str) -> None:
        """启动App"""
        try:
            if isinstance(self._driver, AppDriver):
                self._driver.activate_app(app_package)
                INFO.logger.info(f"成功启动应用: {app_package}")
            else:
                raise NotImplementedError("Web端不支持start_app方法")
        except WebDriverException as e:
            ERROR.logger.error(f"启动应用失败: {app_package}, 错误信息: {e}")
            raise

    def close_app(self, app_package: str) -> None:
        """关闭App"""
        try:
            if isinstance(self._driver, AppDriver):
                self._driver.terminate_app(app_package)
                INFO.logger.info(f"成功关闭应用: {app_package}")
            else:
                raise NotImplementedError("Web端不支持close_app方法")
        except WebDriverException as e:
            ERROR.logger.error(f"关闭应用失败: {app_package}, 错误信息: {e}")
            raise

    def current_package(self) -> str:
        """获取当前应用包名"""
        if isinstance(self._driver, AppDriver):
            return self._driver.current_package
        raise NotImplementedError("Web端不支持current_package方法")

    def current_activity(self) -> str:
        """获取当前活动"""
        if isinstance(self._driver, AppDriver):
            return self._driver.current_activity
        raise NotImplementedError("Web端不支持current_activity方法")

    def install_app(self, app_path: str) -> None:
        """安装App"""
        try:
            if isinstance(self._driver, AppDriver):
                self._driver.install_app(app_path)
                INFO.logger.info(f"成功安装应用: {app_path}")
            else:
                raise NotImplementedError("Web端不支持install_app方法")
        except WebDriverException as e:
            ERROR.logger.error(f"安装应用失败: {app_path}, 错误信息: {e}")
            raise

    def uninstall_app(self, app_package: str) -> None:
        """卸载App"""
        try:
            if isinstance(self._driver, AppDriver):
                self._driver.remove_app(app_package)
                INFO.logger.info(f"成功卸载应用: {app_package}")
            else:
                raise NotImplementedError("Web端不支持uninstall_app方法")
        except WebDriverException as e:
            ERROR.logger.error(f"卸载应用失败: {app_package}, 错误信息: {e}")
            raise

    def is_app_installed(self, app_package: str) -> bool:
        """检查App是否已安装"""
        try:
            if isinstance(self._driver, AppDriver):
                return self._driver.is_app_installed(app_package)
            raise NotImplementedError("Web端不支持is_app_installed方法")
        except WebDriverException as e:
            ERROR.logger.error(f"检查应用是否安装失败: {app_package}, 错误信息: {e}")
            raise

    def background_app(self, seconds: int) -> None:
        """将App置于后台"""
        try:
            if isinstance(self._driver, AppDriver):
                self._driver.background_app(seconds)
                INFO.logger.info(f"成功将应用置于后台: {seconds}秒")
            else:
                raise NotImplementedError("Web端不支持background_app方法")
        except WebDriverException as e:
            ERROR.logger.error(f"将应用置于后台失败, 错误信息: {e}")
            raise

    def get_network_connect(self) -> int:
        """获取手机网络连接类型"""
        if isinstance(self._driver, AppDriver):
            return self._driver.network_connection
        raise NotImplementedError("Web端不支持get_network_connect方法")

    def set_network_connect(self, connection_type: int) -> None:
        """设置网络连接类型"""
        try:
            if isinstance(self._driver, AppDriver):
                self._driver.set_network_connection(connection_type)
                INFO.logger.info(f"成功设置网络连接类型: {connection_type}")
            else:
                raise NotImplementedError("Web端不支持set_network_connect方法")
        except WebDriverException as e:
            ERROR.logger.error(f"设置网络连接类型失败, 错误信息: {e}")
            raise

    def press_keycode(self, keycode: int, metastate: Optional[int] = None, flags: Optional[int] = None) -> None:
        """
        发送按键码

        :param keycode: 按键码
        :param metastate: 按键的元状态（可选）
        :param flags: 按键事件的标志（可选）
        """
        try:
            if isinstance(self._driver, AppDriver):
                if metastate is not None and flags is not None:
                    self._driver.press_keycode(keycode, metastate, flags)
                elif metastate is not None:
                    self._driver.press_keycode(keycode, metastate)
                else:
                    self._driver.press_keycode(keycode)
                INFO.logger.info(f"成功发送按键码: {keycode}")
            else:
                raise NotImplementedError("Web端不支持press_keycode方法")
        except WebDriverException as e:
            ERROR.logger.error(f"发送按键码失败: {keycode}, 错误信息: {e}")
            raise

    def open_notify(self) -> None:
        """打开通知栏"""
        try:
            if isinstance(self._driver, AppDriver):
                self._driver.open_notifications()
                INFO.logger.info("成功打开通知栏")
            else:
                raise NotImplementedError("Web端不支持open_notify方法")
        except WebDriverException as e:
            ERROR.logger.error(f"打开通知栏失败, 错误信息: {e}")
            raise

    def contexts(self):
        """获取上下文"""
        if isinstance(self._driver, AppDriver):
            return self._driver.contexts
        raise NotImplementedError("Web端不支持contexts方法")

    def switch_to_context(self, context: str) -> None:
        """切换上下文"""
        try:
            if isinstance(self._driver, AppDriver):
                self._driver.switch_to.context(context)
                INFO.logger.info(f"成功切换到上下文: {context}")
            else:
                raise NotImplementedError("Web端不支持switch_to_context方法")
        except WebDriverException as e:
            ERROR.logger.error(f"切换上下文失败, 错误信息: {e}")
            raise

    def refresh(self) -> None:
        """刷新页面"""
        try:
            self._driver.refresh()
            INFO.logger.info("页面刷新成功")
        except Exception as e:
            ERROR.logger.error(f"刷新页面失败: {str(e)}")
            self.take_screenshot("refresh_error")
            raise

    def back(self) -> None:
        """返回上一页"""
        try:
            self._driver.back()
            INFO.logger.info("成功返回上一页")
        except Exception as e:
            ERROR.logger.error(f"返回上一页失败: {str(e)}")
            self.take_screenshot("back_error")
            raise

    def forward(self) -> None:
        """前进到下一页"""
        try:
            self._driver.forward()
            INFO.logger.info("成功前进到下一页")
        except Exception as e:
            ERROR.logger.error(f"前进到下一页失败: {str(e)}")
            self.take_screenshot("forward_error")
            raise

    def close(self) -> None:
        """关闭当前窗口"""
        try:
            self._driver.close()
            INFO.logger.info("成功关闭当前窗口")
        except Exception as e:
            ERROR.logger.error(f"关闭当前窗口失败: {str(e)}")
            self.take_screenshot("close_error")
            raise

    def quit(self) -> None:
        """退出浏览器"""
        try:
            self._driver.quit()
            INFO.logger.info("成功退出浏览器")
        except Exception as e:
            ERROR.logger.error(f"退出浏览器失败: {str(e)}")
            self.take_screenshot("quit_error")
            raise

    def maximize_window(self) -> None:
        """最大化窗口"""
        try:
            self._driver.maximize_window()
            INFO.logger.info("成功最大化窗口")
        except Exception as e:
            ERROR.logger.error(f"最大化窗口失败: {str(e)}")
            self.take_screenshot("maximize_window_error")
            raise

    def minimize_window(self) -> None:
        """最小化窗口"""
        try:
            self._driver.minimize_window()
            INFO.logger.info("成功最小化窗口")
        except Exception as e:
            ERROR.logger.error(f"最小化窗口失败: {str(e)}")
            self.take_screenshot("minimize_window_error")
            raise

    def switch_to_frame(self, iframe) -> None:
        """切换到iframe"""
        try:
            self._driver.switch_to.frame(iframe)
            INFO.logger.info(f"成功切换到iframe: {iframe}")
        except Exception as e:
            ERROR.logger.error(f"切换到iframe失败: {str(e)}")
            self.take_screenshot("switch_to_frame_error")
            raise

    def switch_to_default_frame(self) -> None:
        """切换到默认内容"""
        try:
            self._driver.switch_to.default_content()
            INFO.logger.info("成功切换到默认内容")
        except Exception as e:
            ERROR.logger.error(f"切换到默认内容失败: {str(e)}")
            self.take_screenshot("switch_to_default_frame_error")
            raise

    def execute_script(self, script: str, *args) -> Any:
        """执行JavaScript代码"""
        try:
            result = self._driver.execute_script(script, *args)
            INFO.logger.info(f"成功执行JavaScript代码: {script}")
            return result
        except Exception as e:
            ERROR.logger.error(f"执行JavaScript代码失败: {str(e)}")
            self.take_screenshot("execute_script_error")
            raise

    def current_url(self) -> str:
        """获取当前URL"""
        try:
            url = self._driver.current_url
            return url
        except Exception as e:
            ERROR.logger.error(f"获取当前URL失败: {str(e)}")
            self.take_screenshot("current_url_error")
            raise

    def current_window_handle(self) -> str:
        """获取当前窗口句柄"""
        try:
            handle = self._driver.current_window_handle
            return handle
        except Exception as e:
            ERROR.logger.error(f"获取当前窗口句柄失败: {str(e)}")
            self.take_screenshot("current_window_handle_error")
            raise

    def title(self) -> str:
        """获取页面标题"""
        try:
            title = self._driver.title
            INFO.logger.info(f"当前页面标题: {title}")
            return title
        except Exception as e:
            ERROR.logger.error(f"获取页面标题失败: {str(e)}")
            self.take_screenshot("title_error")
            raise

    def page_source(self) -> str:
        """获取页面源码"""
        try:
            source = self._driver.page_source
            INFO.logger.info("成功获取页面源码")
            return source
        except Exception as e:
            ERROR.logger.error(f"获取页面源码失败: {str(e)}")
            self.take_screenshot("page_source_error")
            raise

    def tap(self, positions: List[Tuple[int, int]], duration: Optional[int] = None) -> Self:
        """
        点击屏幕上的指定坐标

        :param positions: 一个包含 x/y 坐标的元组数组，长度最多为 5
        :param duration: 单次点击持续时间（毫秒）
        :return: Self instance
        """
        if len(positions) > 5:
            raise ValueError("positions 数组的长度不能超过 5")

        try:
            self._driver.tap(positions, duration)
            INFO.logger.info(f"成功点击坐标: {positions} 持续时间: {duration}ms")
        except WebDriverException as e:
            ERROR.logger.error(f"点击坐标失败: {positions}, 错误信息: {e}")
            raise
        return self

    def drag_and_drop(self, start_element: WebElement, end_element: WebElement, pause: Optional[float] = None) -> Self:
        """
        拖拽元素

        :param start_element: 起始元素
        :param end_element: 结束元素
        :param pause: 暂停时间（秒）
        :return: Self instance
        """
        try:
            self._driver.drag_and_drop(start_element, end_element, pause)
            INFO.logger.info(f"成功拖拽元素从 {start_element} 到 {end_element}")
        except WebDriverException as e:
            ERROR.logger.error(f"拖拽元素失败: 从 {start_element} 到 {end_element}, 错误信息: {e}")
            raise
        return self

    def scroll(self, start_element: WebElement, end_element: WebElement, duration: Optional[int] = None) -> Self:
        """
        滚动屏幕

        :param start_element: 起始元素
        :param end_element: 结束元素
        :param duration: 持续时间（毫秒）
        """
        try:
            self._driver.scroll(start_element, end_element, duration)
            INFO.logger.info(f"成功滚动屏幕从 {start_element} 到 {end_element}")
        except WebDriverException as e:
            ERROR.logger.error(f"滚动屏幕失败: 从 {start_element} 到 {end_element}, 错误信息: {e}")
            raise
        return self

    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: int = None) -> Self:
        """
        滑动屏幕

        :param start_x: 起始X坐标
        :param start_y: 起始Y坐标
        :param end_x: 结束X坐标
        :param end_y: 结束Y坐标
        :param duration: 持续时间（毫秒）
        """
        try:
            self._driver.swipe(start_x, start_y, end_x, end_y, duration)
            INFO.logger.info(f"成功滑动屏幕从 ({start_x}, {start_y}) 到 ({end_x}, {end_y}) 持续时间: {duration}ms")
        except WebDriverException as e:
            ERROR.logger.error(f"滑动屏幕失败: 从 ({start_x}, {start_y}) 到 ({end_x}, {end_y}), 错误信息: {e}")
            raise
        return self
