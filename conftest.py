import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from appium import webdriver as appium_webdriver
from appium.options.common.base import AppiumOptions
from config.setting import ensure_path_sep, root_path


class DriverManager:
    """驱动管理器类"""

    def __init__(self):
        self.driver_path = os.path.join(root_path(), 'drivers')
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
            raise ValueError("driver_type必须是“web”或“app”")

        # 确定目标driver路径
        target_filename = f'chromedriver_{driver_type}.exe'
        target_path = os.path.join(self.driver_path, target_filename)

        # 如果目标driver已存在，直接返回路径
        if os.path.exists(target_path):
            print(f"使用现有的 {driver_type} driver: {target_path}")
            return target_path

        # 如果不存在，则下载新的driver
        print(f"正在下载 {driver_type} driver, 请稍候...")
        try:
            # 根据类型选择ChromeDriver版本
            chrome_driver = (ChromeDriverManager() if driver_type == 'web'
                             else ChromeDriverManager(driver_version=version or "95.0.4638.10"))

            # 下载ChromeDriver
            source_path = chrome_driver.install()

            # 复制到目标位置
            import shutil
            shutil.copy2(source_path, target_path)
            print(f"已成功下载驱动程序并将其复制到: {target_path}")

            return target_path

        except Exception as e:
            print(f"{driver_type} driver 下载失败: {str(e)}")
            raise


# 创建驱动管理器实例
driver_manager = DriverManager()


@pytest.fixture(scope='session')
def web_driver():
    """Web端测试driver配置"""
    driver = None
    try:
        driver_path = driver_manager.get_driver_path('web')
        print(f"Web ChromeDriver 路径: {driver_path}")

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
        driver_path = driver_manager.get_driver_path('app', "95.0.4638.10")
        print(f"App ChromeDriver 路径: {driver_path}")

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
