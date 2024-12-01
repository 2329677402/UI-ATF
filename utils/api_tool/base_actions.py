from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import os
from typing import Union, Tuple
from datetime import datetime
from config.setting import ensure_path_sep, root_path, Settings
from utils.api_tool.locator import Locator


class BaseActions:
    """基础操作封装"""
    
    def __init__(self, driver):
        self.driver = driver
        # 创建设置实例
        settings = Settings()
        config = settings.global_config
        self.wait = WebDriverWait(
            driver,
            config['webdriver_timeout'],
            poll_frequency=config['webdriver_poll_frequency']
        )

    @staticmethod
    def clean_screenshots():
        """清理历史截图"""
        screenshots_path = os.path.join(root_path(), 'datas', 'screenshots')
        if os.path.exists(screenshots_path):
            import shutil
            shutil.rmtree(screenshots_path)
        os.makedirs(screenshots_path, exist_ok=True)

    def take_screenshot(self, name: str):
        """截图"""
        settings = Settings()
        if not settings.global_config['save_screenshot']:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.{settings.global_config['screenshot_format']}"
        filepath = ensure_path_sep(os.path.join('/datas/screenshots', filename))
        self.driver.save_screenshot(filepath)

    @staticmethod
    def _convert_to_locator(selector: Union[str, Tuple, Locator]) -> Locator:
        """转换为Locator对象"""
        if isinstance(selector, Locator):
            return selector
        elif isinstance(selector, str):
            return Locator('css_selector', selector)
        elif isinstance(selector, tuple):
            return Locator(selector[0], selector[1])
        raise ValueError(f"Invalid selector type: {type(selector)}")

    def click(self, selector: Union[str, Tuple, Locator]):
        """点击元素"""
        locator = self._convert_to_locator(selector)
        element = self.wait.until(
            EC.element_to_be_clickable(locator.to_selenium())
        )
        element.click()

    def type(self, selector: Union[str, Tuple, Locator], text: str):
        """输入文本"""
        locator = self._convert_to_locator(selector)
        element = self.wait.until(
            EC.presence_of_element_located(locator.to_selenium())
        )
        element.clear()
        element.send_keys(text)

    def is_element_present(self, selector: Union[str, Tuple, Locator]) -> bool:
        """检查元素是否存在"""
        try:
            locator = self._convert_to_locator(selector)
            self.wait.until(
                EC.presence_of_element_located(locator.to_selenium())
            )
            return True
        except TimeoutException:
            return False
        except WebDriverException as e:
            raise WebDriverException(f"Failed to check element presence: {str(e)}")

    def open(self, url: str):
        """打开URL"""
        self.driver.get(url) 