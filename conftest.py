import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from appium import webdriver as appium_webdriver
from appium.options.common.base import AppiumOptions

# 定义driver存放路径
DRIVER_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'drivers')
if not os.path.exists(DRIVER_PATH):
    os.makedirs(DRIVER_PATH)

def get_web_driver_path():
    """获取web端ChromeDriver路径"""
    driver_path = ChromeDriverManager().install()
    web_driver_path = os.path.join(DRIVER_PATH, 'chromedriver_web.exe')
    if os.path.exists(driver_path) and not os.path.exists(web_driver_path):
        import shutil
        shutil.copy2(driver_path, web_driver_path)
    return web_driver_path

def get_app_driver_path():
    """获取app端ChromeDriver路径"""
    driver_path = ChromeDriverManager(driver_version="95.0.4638.74").install()
    app_driver_path = os.path.join(DRIVER_PATH, 'chromedriver_app.exe')
    if os.path.exists(driver_path) and not os.path.exists(app_driver_path):
        import shutil
        shutil.copy2(driver_path, app_driver_path)
    return app_driver_path

@pytest.fixture(scope='session')
def web_driver():
    """
    Web端测试driver配置
    使用webdriver_manager自动管理chrome driver版本
    """
    try:
        # 显式下载并复制 ChromeDriver
        driver_path = get_web_driver_path()
        print(f"Web ChromeDriver path: {driver_path}")
        
        service = Service(executable_path=driver_path)
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        # 添加调试选项
        options.add_argument('--verbose')
        options.add_argument('--log-level=3')
        
        driver = webdriver.Chrome(service=service, options=options)
        print("WebDriver 初始化成功")
        yield driver
    except Exception as e:
        print(f"WebDriver 初始化失败: {str(e)}")
        raise
    finally:
        if 'driver' in locals():
            driver.quit()

@pytest.fixture(scope='session')
def app_driver():
    """
    App端测试driver配置
    使用Android System WebView 95.0.4638.74版本对应的chromedriver
    """
    try:
        # 显式下载并复制 ChromeDriver
        driver_path = get_app_driver_path()
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
        if 'driver' in locals():
            driver.quit()
