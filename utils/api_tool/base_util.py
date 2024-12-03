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
from common.setting import root_path, Settings
from utils.log_tool.log_control import INFO, ERROR
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.remote.webelement import WebElement
from utils.api_tool.selector_util import SelectorUtil


class BaseUtil:
    """基础操作封装"""

    def __init__(self, driver: WebDriver):
        """
        初始化工具类
        :param driver: WebDriver实例
        """
        self._driver = driver
        self.settings = Settings()
        config = self.settings.global_config
        self.wait = WebDriverWait(
            driver,
            config['webdriver_timeout'],
            poll_frequency=config['webdriver_poll_frequency']
        )

        # 清理历史数据
        if config.get('clean_screenshots', True):
            self._clean_screenshots()
        if config.get('clean_logs', True):
            self._clean_logs()

    def __getattr__(self, name):
        """代理原生WebDriver的方法"""
        return getattr(self._driver, name)

    def find_element(self, selector: str, by: str = 'css_selector', timeout: int = None) -> WebElement:
        """
        查找元素
        :param selector: 选择器
        :param by: 定位方式
        :param timeout: 超时时间
        :return: WebElement对象
        """
        locator = SelectorUtil.get_selenium_locator(selector, by)
        try:
            return self.wait.until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            ERROR.logger.error(f"查找元素超时: {selector} (by={by})")
            self.take_screenshot("find_element_timeout")
            raise
        except Exception as e:
            ERROR.logger.error(f"查找元素失败: {selector} (by={by}), 错误: {str(e)}")
            self.take_screenshot("find_element_error")
            raise

    def click(self, selector: str, by: str = 'css_selector', delay: int = 0):
        """
        点击元素
        :param selector: 选择器
        :param by: 定位方式
        :param delay: 点击前的延迟时间(秒)
        """
        try:
            locator = SelectorUtil.get_selenium_locator(selector, by)
            element = self.wait.until(
                EC.element_to_be_clickable(locator)
            )
            if delay > 0:
                time.sleep(delay)
            element.click()
            INFO.logger.info(f"成功点击元素: {selector} (by={by})")
        except TimeoutException:
            ERROR.logger.error(f"点击元素超时: {selector} (by={by})")
            self.take_screenshot("click_timeout")
            raise
        except Exception as e:
            ERROR.logger.error(f"点击元素失败: {selector} (by={by}), 错误: {str(e)}")
            self.take_screenshot("click_error")
            raise

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

    def take_screenshot(self, name: str):
        """
        截取当前页面截图
        :param name: 截图名称
        """
        try:
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
            print(f"截图已保存: {filepath}")
            return filepath
        except Exception as e:
            print(f"截图失败: {str(e)}")
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
