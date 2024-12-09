#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@ Date        : 12/09/2024 5:36 PM
@ Author      : Administrator
@ File        : conftest.py
@ Description : Test fixture configuration file.
"""
import os
import time
import pytest
from common.setting import root_path
from selenium import webdriver as WebDriver
from appium import webdriver as AppDriver
from selenium.webdriver.chrome.service import Service
from appium.options.common.base import AppiumOptions
from webdriver_manager.chrome import ChromeDriverManager


class DriverManager:
    def __init__(self):
        self.driver_path = os.path.join(root_path(), 'drivers')
        if not os.path.exists(self.driver_path):
            os.makedirs(self.driver_path)

    def get_driver_path(self, driver_type: str, version: str = None) -> str:
        """
        Get the driver path. If the driver does not exist, download it.

        :param driver_type: Driver type, 'web' or 'app'.
        :param version: Driver version.
        :return: Driver path.
        """
        if driver_type not in ['web', 'app']:
            raise ValueError("Invalid driver type, must be 'web' or 'app'.")

        # Define the target driver path.
        target_filename = f'chromedriver_{driver_type}.exe'
        target_path = os.path.join(self.driver_path, target_filename)

        # If the driver exists, return the path.
        if os.path.exists(target_path):
            return target_path
        else:
            print(f"Start downloading the {driver_type} driver, please wait...")

        try:
            # Initialize the driver manager.
            chrome_driver = (ChromeDriverManager() if driver_type == 'web'
                             else ChromeDriverManager(driver_version=version or "95.0.4638.10"))

            # Download the chromedriver.
            source_path = chrome_driver.install()
            print(f"Downloaded the {driver_type} driver to: {source_path}.")

            # Copy the driver to the target path.
            import shutil
            shutil.copy2(source_path, target_path)
            print(f"Copy the {driver_type} driver to: {target_path}.")

            return target_path

        except Exception as e:
            print(f"Failed to download the {driver_type} driver: {str(e)}")
            raise


# Initialize DriverManager class.
driver_manager = DriverManager()


@pytest.fixture(scope='session')
def web_driver():
    driver = None
    try:
        driver_path = driver_manager.get_driver_path('web')
        print(f"\nCurrently using the WebDriver driver path: {driver_path}.")

        service = Service(executable_path=driver_path)
        options = WebDriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--verbose')
        options.add_argument('--log-level=3')

        driver = WebDriver.Chrome(service=service, options=options)
        print("Start initializing the WebDriver object, please wait...")
        print("Initialization completed, start executing test cases...")
        time.sleep(0.5)
        yield driver
    except Exception as e:
        print(f"WebDriver initialization failed: {str(e)}")
        raise
    finally:
        if driver is not None:
            driver.quit()
            print("\nWeb-related tests have been completed, please check the Allure report for details!")


@pytest.fixture(scope='session')
def app_driver():
    driver = None
    try:
        driver_path = driver_manager.get_driver_path('app', "95.0.4638.10")
        print(f"\nCurrently using the AppDriver driver path: {driver_path}.")

        # Get the current appPackage and appActivity of the Android device:
        # adb shell dumpsys window | findstr mCurrentFocus
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

        driver = AppDriver.Remote("http://127.0.0.1:4723", options=options)
        print("Start initializing the AppDriver object, please wait...")
        print("Initialization completed, start executing test cases...")
        time.sleep(0.5)
        yield driver
    except Exception as e:
        print(f"AppDriver initialization failed: {str(e)}")
        raise
    finally:
        if driver is not None:
            driver.quit()
            print("\nApp-related tests have been completed, please check the Allure report for details!")
