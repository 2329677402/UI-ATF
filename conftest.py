import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from appium import webdriver as appium_webdriver
from appium.options.common.base import AppiumOptions


class DriverManager:
    """驱动管理器类"""

    def __init__(self):
        # 获取项目根目录下的drivers目录
        self.driver_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'drivers')
        if not os.path.exists(self.driver_path):
            os.makedirs(self.driver_path)

    def get_driver_path(self, driver_type: str, version: str = None) -> str:
        """
        获取driver路径，如果本地不存在则下载
        :param driver_type: 驱动类型 ('web' 或 'app')
        :param version: ChromeDriver版本号（可选）
        :return: driver路径
        """
        if driver_type not in ['web', 'app']:
            raise ValueError("driver_type must be 'web' or 'app'")

        # 确定目标driver路径
        target_filename = f'chromedriver_{driver_type}.exe'
        target_path = os.path.join(self.driver_path, target_filename)

        # 如果目标driver已存在，直接返回路径
        if os.path.exists(target_path):
            print(f"Using existing {driver_type} driver: {target_path}")
            return target_path

        # 如果不存在，则下载新的driver
        print(f"Downloading new {driver_type} driver...")
        try:
            # 根据类型选择ChromeDriver版本
            chrome_driver = (ChromeDriverManager() if driver_type == 'web'
                             else ChromeDriverManager(driver_version=version or "95.0.4638.74"))

            # 下载ChromeDriver
            source_path = chrome_driver.install()

            # 复制到目标位置
            import shutil
            shutil.copy2(source_path, target_path)
            print(f"Successfully downloaded and copied driver to: {target_path}")

            return target_path

        except Exception as e:
            print(f"Failed to download {driver_type} driver: {str(e)}")
            raise


# 创建驱动管理器实例
driver_manager = DriverManager()


@pytest.fixture(scope='session')
def web_driver():
    """Web端测试driver配置"""
    driver = None
    try:
        driver_path = driver_manager.get_driver_path('web')
        print(f"Web ChromeDriver path: {driver_path}")

        service = Service(executable_path=driver_path)
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--verbose')
        options.add_argument('--log-level=3')

        driver = webdriver.Chrome(service=service, options=options)
        print("WebDriver 初始化成功")
        yield driver
    except Exception as e:
        print(f"WebDriver 初始化失败: {str(e)}")
        raise
    finally:
        if driver is not None:
            driver.quit()


@pytest.fixture(scope='session')
def app_driver():
    """App端测试driver配置"""
    driver = None
    try:
        driver_path = driver_manager.get_driver_path('app', "95.0.4638.74")
        print(f"App ChromeDriver path: {driver_path}")

        options = AppiumOptions()
        options.load_capabilities({
            "appium:appPackage": "com.android.browser",
            "appium:appActivity": ".BrowserActivity",
            "platformName": "Android",
            "appium:automationName": "uiautomator2",
            "appium:deviceName": "127.0.0.1:16384",
            "appium:ensureWebviewsHavePages": True,
            "appium:nativeWebScreenshot": True,
            "appium:newCommandTimeout": 3600,
            "appium:connectHardwareKeyboard": True,
            "appium:chromedriverExecutable": driver_path,
            "appium:noReset": True
        })

        driver = appium_webdriver.Remote("http://127.0.0.1:4723", options=options)
        print("AppDriver 初始化成功")
        yield driver
    except Exception as e:
        print(f"AppDriver 初始化失败: {str(e)}")
        raise
    finally:
        if driver is not None:
            driver.quit()
