#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@ Date        : 2024/11/26 下午5:29
@ Author      : Administrator
@ File        : conftest.py
@ Description : 功能描述
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from appium import webdriver as appium_driver
from appium.options.common.base import AppiumOptions
import os
import shutil


def setup_chromedriver(version, identifier):
    """
    Feat: Download and set the ChromeDriver path.
    :param version:
    :param identifier:
    :return: target path.
    """
    drivers_dir = os.path.join(os.path.dirname(__file__), 'drivers')
    if not os.path.exists(drivers_dir):
        os.makedirs(drivers_dir)

    # Download the specific version of ChromeDriver.
    driver_path = ChromeDriverManager(version).install()

    # Move the downloaded driver to the drivers directory and rename.
    target_path = os.path.join(drivers_dir, f'chromedriver_{identifier}.exe')
    shutil.move(driver_path, target_path)

    return target_path


@pytest.fixture(scope="session")
def web_driver(request):
    web_driver_path = setup_chromedriver(None, "web")
    options = webdriver.ChromeOptions()
    service = ChromeService(executable_path=web_driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def app_driver(request):
    app_driver_path = setup_chromedriver("95.0.4638.74", "appium")
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
        "appium:connectHardwareKeyboard": True
    })
    options.app = os.path.join(os.path.dirname(__file__), 'datas', 'apk', 'yangli.apk')  # Adjust the path as needed
    options.chromedriver_executable = app_driver_path
    driver = appium_driver.Remote("http://127.0.0.1:4723", options=options)
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def base_case_web(web_driver):
    from utils.base_util import BaseUtil
    return BaseUtil(web_driver)


@pytest.fixture(scope="function")
def base_case_app(app_driver):
    from utils.base_util import BaseUtil
    return BaseUtil(app_driver)
