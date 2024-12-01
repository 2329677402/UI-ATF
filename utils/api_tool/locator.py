from selenium.webdriver.common.by import By

class Locator:
    def __init__(self, method: str, value: str):
        """
        初始化定位器
        :param method: 定位方法
        :param value: 定位值
        """
        self.method = method.replace(' ', '_')  # 确保空格被替换为下划线
        self.value = value

    def to_selenium(self):
        """将自定义Locator转换为Selenium可用的格式"""
        # 将方法名转换为 By 类的属性名格式
        method_name = self.method.upper().replace(' ', '_')
        return getattr(By, method_name), self.value
