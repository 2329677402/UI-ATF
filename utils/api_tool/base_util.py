from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import os
from typing import Union, Tuple
from datetime import datetime
from config.setting import ensure_path_sep, root_path, Settings
from utils.api_tool.locator import Locator


class BaseUtil(WebDriver):
    """基础操作封装"""

    def __init__(self, driver: WebDriver):
        """
        初始化工具类
        :param driver: WebDriver实例
        """
        self._driver = driver
        # 创建设置实例
        settings = Settings()
        config = settings.global_config
        self.wait = WebDriverWait(
            driver,
            config['webdriver_timeout'],
            poll_frequency=config['webdriver_poll_frequency']
        )

    def __getattr__(self, name):
        """代理原生WebDriver的方法"""
        return getattr(self._driver, name)

    @staticmethod
    def clean_screenshots():
        """清理历史截图"""
        screenshots_path = os.path.join(root_path(), 'datas', 'screenshots')
        if os.path.exists(screenshots_path):
            import shutil
            shutil.rmtree(screenshots_path)
        os.makedirs(screenshots_path, exist_ok=True)

    def take_screenshot(self, name: str):
        """
        截取当前页面截图
        :param name: 截图名称
        """
        try:
            settings = Settings()
            if not settings.global_config['save_screenshot']:
                return

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
            print(f"截图已保存: {filepath}")  # 添加日志
            return filepath
        except Exception as e:
            print(f"截图失败: {str(e)}")  # 添加错误日志
            return None

    @staticmethod
    def _convert_to_locator(selector: Union[str, Tuple, Locator]) -> Locator:
        """
        转换为Locator对象
        :param selector: 选择器
        :return: Locator对象
        """
        if isinstance(selector, Locator):
            return selector
        elif isinstance(selector, str):
            return Locator('CSS_SELECTOR', selector)
        elif isinstance(selector, tuple):
            return Locator(selector[0], selector[1])
        raise ValueError(f"无效的选择器类型: {type(selector)}")

    def click(self, selector: Union[str, Tuple, Locator]):
        """
        点击元素
        :param selector: 元素选择器
        """
        locator = self._convert_to_locator(selector)
        element = self.wait.until(
            EC.element_to_be_clickable(locator.to_selenium())
        )
        element.click()

    def type(self, selector: Union[str, Tuple, Locator], text: str):
        """
        输入文本
        :param selector: 元素选择器
        :param text: 要输入的文本
        """
        locator = self._convert_to_locator(selector)
        element = self.wait.until(
            EC.presence_of_element_located(locator.to_selenium())
        )
        element.clear()
        element.send_keys(text)

    def is_element_present(self, selector: Union[str, Tuple, Locator]) -> bool:
        """
        检查元素是否存在
        :param selector: 元素选择器
        :return: 元素是否存在
        """
        try:
            locator = self._convert_to_locator(selector)
            self.wait.until(
                EC.presence_of_element_located(locator.to_selenium())
            )
            return True
        except TimeoutException:
            return False
        except WebDriverException as e:
            raise WebDriverException(f"检查元素存在时失败: {str(e)}")

    def open(self, url: str):
        """
        打开URL
        :param url: 要打开的URL
        """
        self._driver.get(url) 