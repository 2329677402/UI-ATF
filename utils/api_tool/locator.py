from dataclasses import dataclass
from selenium.webdriver.common.by import By

@dataclass
class Locator:
    """封装Selenium定位方式的数据类"""
    method: str
    value: str

    def to_selenium(self):
        """将自定义Locator转换为Selenium可用的格式"""
        return getattr(By, self.method.upper()), self.value
