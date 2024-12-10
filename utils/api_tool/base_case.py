#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@ Date        : 12/9/2024 3:23 PM
@ Author      : Poco Ray
@ File        : base_case.py
@ Description : Test case base class.
"""
import base64
import os
import time
import shutil
import requests
from datetime import datetime
from common.setting import root_path, Settings
from utils.api_tool.custom_webelement import CustomWebElement
from utils.log_tool.log_control import INFO, ERROR
from utils.api_tool.selector_util import SelectorUtil
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, ElementClickInterceptedException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from appium.webdriver.webdriver import WebDriver as AppDriver
from typing import Any, List, Optional, Self, Tuple, ClassVar, Union


class BaseCase:
    """ Class variable declaration. """
    driver: WebDriver or AppDriver = None  # Test driver object.
    _settings: ClassVar[Settings] = Settings()
    _wait: Optional[WebDriverWait] = None
    _timeout: int = _settings.global_config['webdriver_timeout']
    _poll_frequency: float = _settings.global_config['webdriver_poll_frequency']
    screenshots_path = _settings.global_config['screenshots_dir']
    downloads_path = _settings.global_config['downloads_dir']
    logs_path = _settings.global_config['logs_dir']

    def setup_actions(self):
        """ Initialize the test environment. """
        if not hasattr(self, 'driver') or self.driver is None:
            raise ValueError("The driver object is not initialized!")

        # Initialize the wait object.
        self._wait = WebDriverWait(
            self.driver,
            self._timeout,
            poll_frequency=self._poll_frequency
        )

        # Clean up historical data.
        if self._settings.global_config.get('clean_screenshots', True):
            self._clean_screenshots()
        if self._settings.global_config.get('clean_downloads', True):
            self._clean_downloads()
        if self._settings.global_config.get('clean_logs', True):
            self._clean_logs()

    def _clean_screenshots(self):
        """ Clean up the screenshot file. """
        if not os.path.exists(self.screenshots_path):
            os.makedirs(self.screenshots_path, exist_ok=True)
            INFO.logger.info(f"Screenshot directory created: {self.screenshots_path}")
        else:
            shutil.rmtree(self.screenshots_path)
            os.makedirs(self.screenshots_path, exist_ok=True)
            INFO.logger.info("Screenshot files cleanup completed.")

    def _clean_downloads(self):
        """ Clean up the download file. """
        if not os.path.exists(self.downloads_path):
            os.makedirs(self.downloads_path, exist_ok=True)
            INFO.logger.info(f"Download directory created: {self.downloads_path}")
        else:
            shutil.rmtree(self.downloads_path)
            os.makedirs(self.downloads_path, exist_ok=True)
            INFO.logger.info("Download files cleanup completed.")

    def _clean_logs(self):
        """ Clean up the log file. """
        if not os.path.exists(self.logs_path):
            os.makedirs(self.logs_path, exist_ok=True)
            INFO.logger.info(f"Log directory created: {self.logs_path}")
        else:
            try:
                today = datetime.now().date()
                for filename in os.listdir(self.logs_path):
                    if not filename.endswith('.log'):
                        continue

                    file_path = os.path.join(self.logs_path, filename)
                    try:
                        # Extract the date from the file name. (e.g.: xxx-2024-01-01.log)
                        date_str = filename.split('-', 1)[1].split('.')[0]
                        file_date = datetime.strptime(date_str, '%Y-%m-%d').date()

                        # If file_date's not today's log, delete it.
                        if file_date < today:
                            os.remove(file_path)
                            INFO.logger.info(f"Deleted history log file: {filename}.")
                    except (ValueError, IndexError):
                        continue
                    except Exception as e:
                        ERROR.logger.error(f"Error occurred while cleaning log file: {str(e)}")

                INFO.logger.info("Log files cleanup completed.")
            except Exception as e:
                ERROR.logger.error(f"Error occurred while cleaning log directory: {str(e)}")

    def take_screenshot(self, name: str) -> Union[str, None]:
        """
        Take a screenshot of the current screen.

        :param name: Screenshot file name. The current date will be automatically added after the file name is saved.
        :return: Screenshot file path.
        :Usage:
            self.take_screenshot("screenshot_name")
        """
        try:
            # Wait for the page to load.
            # document.readyState: A property indicating the loading state of the document. It has the following possible values:
            # "loading": Document still loading.
            # "interactive": The document has finished loading, the document has been parsed, but Sub-resources such as images, stylesheets, and frames are still loading.
            # "complete": The document and all Sub-resources are fully loaded.
            self._wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")

            # Ensure the directory exists.
            screenshots_dir = os.path.join(root_path(), 'datas', 'screenshots')
            os.makedirs(screenshots_dir, exist_ok=True)

            # Generate file name.
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{name}_{timestamp}.png"

            # Use absolute paths.
            filepath = os.path.join(screenshots_dir, filename)

            # Save screenshot file.
            self.driver.save_screenshot(filepath)
            INFO.logger.info(f"Save screenshots to: {filepath}.")
            return filepath
        except Exception as e:
            ERROR.logger.error(f"Failed to take screenshot: {str(e)}")
            return None

    def open(self, url: str) -> None:
        """
        Open the specified web page URL.

        :param url: Web page URL.
        :Usage:
            self.open("https://www.google.com")
        """
        try:
            self.driver.get(url)
            INFO.logger.info(f"Successfully opened URL: {url}.")
        except TimeoutException:
            ERROR.logger.error(f"Timeout when opening URL: {url}.")
            self.take_screenshot("open_url_timeout")
            raise
        except WebDriverException as e:
            ERROR.logger.error(f"A WebDriverException occurred when opening the URL: {url}, error message: {str(e)}")
            self.take_screenshot("open_url_exception")
            raise
        except Exception as e:
            ERROR.logger.error(f"An unknown exception occurred when opening the URL: {url}, error message: {str(e)}")
            self.take_screenshot("open_url_unknown_exception")
            raise

    def click(self, selector: str = None, by: str = 'css_selector', delay: int = 0,
              pos: Tuple[int, int] = None) -> None:
        """
        Click the specified element or position.

        :param selector: Element selector.
        :param by: Locator method.
        :param delay: Delay time before clicking.
        :param pos: Click position.
        :Usage:
            self.click("#submit_button")
            self.click(pos=(100, 200))
        """
        if pos:
            try:
                if delay > 0:
                    time.sleep(delay)  # Wait only if explicitly requested.

                # Use JavaScript to click to specify the position.
                self.driver.execute_script(f"window.scrollTo({pos[0]}, {pos[1]});")
                self.driver.execute_script(f"document.elementFromPoint({pos[0]}, {pos[1]}).click();")
                INFO.logger.info(f"Successfully clicked position: {pos}.")
            except Exception as e:
                ERROR.logger.error(f"Failed to click position: {pos}, error message: {str(e)}")
                self.take_screenshot("click_pos_error")
                raise
        else:
            max_attempts = 3  # Maximum number of retries.
            attempt = 0
            last_exception = None

            while attempt < max_attempts:
                try:
                    # Wait for the page to load.
                    script = (
                        "return (typeof jQuery !== 'undefined') ? "
                        "jQuery.active == 0 : true"
                    )
                    self.driver.execute_script(script)

                    locator = SelectorUtil.get_selenium_locator(selector, by)

                    # Wait for the element to appear.
                    self._wait.until(EC.presence_of_element_located(locator))
                    self._wait.until(EC.visibility_of_element_located(locator))
                    element = self._wait.until(EC.element_to_be_clickable(locator))

                    # Scroll to the element.
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView(true);",
                        element
                    )

                    if delay > 0:
                        time.sleep(delay)  # Wait only if explicitly requested.

                    # Click the element.
                    try:
                        element.click()
                    except ElementClickInterceptedException:
                        # If the element attribute is blocked, use JavaScript to click.
                        self.driver.execute_script("arguments[0].click();", element)

                    INFO.logger.info(f"Successfully clicked element: {selector} (by={by}).")
                    return

                except TimeoutException as e:
                    last_exception = e
                    attempt += 1
                    continue
                except Exception as e:
                    last_exception = e
                    attempt += 1
                    continue

            # If the maximum number of retries is reached, an exception is thrown.
            ERROR.logger.error(f"Failed to click element: {selector} (by={by}), error message: {str(last_exception)}")
            self.take_screenshot("click_error")

            # Output the page source code.
            try:
                page_source = self.driver.page_source
                ERROR.logger.error(f"Page source code: {page_source}")
            except Exception as e:
                ERROR.logger.error(f"Failed to get page source code: {str(e)}")

            raise last_exception

    def type(self, selector: str, text: str, by: str = 'css_selector', timeout: int = None,
             retry: bool = False) -> None:
        """
        Enter text into the specified element.

        :param selector: Element selector.
        :param text: Text to enter.
        :param by: Locator method.
        :param timeout: Timeout.
        :param retry: Retry flag.
        :Usage:
            self.type("#input_field", "example text"，timeout=10，retry=True)
        """
        try:
            element = self.find_element(selector, by, timeout)
            element.clear()
            element.send_keys(text)
            INFO.logger.info(f"Successfully entered text: {text} into the element: {selector} (by={by}).")
        except TimeoutException:
            ERROR.logger.error(f"Timeout when entering text: {text} into the element: {selector} (by={by}).")
            self.take_screenshot("type_timeout")
            if retry:
                self.type(selector, text, by, timeout, retry=False)
            else:
                raise
        except Exception as e:
            ERROR.logger.error(
                f"Failed to enter text: {text} into the element: {selector} (by={by}), error message: {str(e)}")
            self.take_screenshot("type_error")
            raise

    def is_element_present(self, selector: str, by: str = 'css_selector') -> bool:
        """
        Check if the element exists.

        :param selector: Element selector.
        :param by: Locator method.
        :return: 1. True: Element exists. 2. False: Element does not exist.
        :Usage:
            is_present = self.is_element_present("#element_id")
        """
        try:
            self.find_element(selector, by)
            INFO.logger.info(f"Element found: {selector} (by={by}).")
            return True
        except TimeoutException:
            INFO.logger.info(f"Element not found (timeout): {selector} (by={by}).")
            return False
        except Exception as e:
            ERROR.logger.error(f"Failed to find element: {selector} (by={by}), error message: {str(e)}")
            return False

    @staticmethod
    def sleep(seconds: float = 0.1) -> None:
        """
        Pause for a specified number of seconds.

        :param seconds: Pause time (seconds).
        :Usage:
            self.sleep(5)
        """
        time.sleep(seconds)

    def start_app(self, app_package: str) -> None:
        """
        Start the App.

        :param app_package: App package name.
        :Usage:
            self.start_app("com.example.app")
        """
        try:
            if isinstance(self.driver, AppDriver):
                self.driver.activate_app(app_package)
                INFO.logger.info(f"Successfully started the App: {app_package}.")
            else:
                raise NotImplementedError("The Web end does not support the 'start_app' method!")
        except WebDriverException as e:
            ERROR.logger.error(f"Failed to start the App: {app_package}, error message: {str(e)}")
            raise

    def close_app(self, app_package: str) -> None:
        """
        Close the App.

        :param app_package: App package name.
        :Usage:
            self.close_app("com.example.app")
        """
        try:
            if isinstance(self.driver, AppDriver):
                self.driver.terminate_app(app_package)
                INFO.logger.info(f"Successfully closed the App: {app_package}.")
            else:
                raise NotImplementedError("The Web end does not support the 'close_app' method!")
        except WebDriverException as e:
            ERROR.logger.error(f"Failed to close the App: {app_package}, error message: {str(e)}")
            raise

    @property
    def current_package(self) -> str:
        """
        Get the current App package name.

        :return: Current App package name. e.g.: com.example.app.
        :Usage:
            print(self.current_package)
        """
        if isinstance(self.driver, AppDriver):
            return self.driver.current_package
        raise NotImplementedError("The Web end does not support the 'current_package' method!")

    @property
    def current_activity(self) -> str:
        """
        Get the current App activity name.

        :return: Current App activity name. e.g.: .MainActivity.
        :Usage:
            print(self.current_activity)
        """
        if isinstance(self.driver, AppDriver):
            return self.driver.current_activity
        raise NotImplementedError("The Web end does not support the 'current_activity' method!")

    def install_app(self, app_path: str) -> None:
        """
        Install the App.

        :param app_path: Apk file path.
        :Usage:
            self.install_app("/path/to/app.apk")
        """
        try:
            if isinstance(self.driver, AppDriver):
                self.driver.install_app(app_path)
                INFO.logger.info(f"Successfully installed the App: {app_path}.")
            else:
                raise NotImplementedError("The Web end does not support the 'install_app' method!")
        except WebDriverException as e:
            ERROR.logger.error(f"Failed to install the App: {app_path}, error message: {str(e)}")
            raise

    def uninstall_app(self, app_package: str) -> None:
        """
        Uninstall the App.

        :param app_package: App package name.
        :Usage:
            self.uninstall_app("com.example.app")
        """
        try:
            if isinstance(self.driver, AppDriver):
                self.driver.remove_app(app_package)
                INFO.logger.info(f"Successfully uninstalled the App: {app_package}.")
            else:
                raise NotImplementedError("The Web end does not support the 'uninstall_app' method!")
        except WebDriverException as e:
            ERROR.logger.error(f"Failed to uninstall the App: {app_package}, error message: {str(e)}")
            raise

    def is_app_installed(self, app_package: str) -> bool:
        """
        Check if the App is installed.

        :param app_package: App package name.
        :return: 1. True: Installed. 2. False: Not installed.
        :Usage:
            is_installed = self.is_app_installed("com.example.app")
        """
        try:
            if isinstance(self.driver, AppDriver):
                return self.driver.is_app_installed(app_package)
            raise NotImplementedError("The Web end does not support the 'is_app_installed' method!")
        except WebDriverException as e:
            ERROR.logger.error(f"Failed to check if the App is installed: {app_package}, error message: {str(e)}")
            raise

    def background_app(self, seconds: int) -> None:
        """
        Put the App in the background.

        :param seconds: Background time (seconds).
        :Usage:
            self.background_app(5)
        """
        try:
            if isinstance(self.driver, AppDriver):
                self.driver.background_app(seconds)
                INFO.logger.info(f"Successfully put the App in the background for {seconds} seconds.")
            else:
                raise NotImplementedError("The Web end does not support the 'background_app' method!")
        except WebDriverException as e:
            ERROR.logger.error(
                f"Failed to put the App in the background for {seconds} seconds, error message: {str(e)}")
            raise

    @property
    def get_network_connect(self) -> int:
        """
        Get the mobile network connection type.

        :return: 0 (None), 1 (Airplane Mode), 2 (Wi-fi only), 4 (Data only), 6 (All network on).
        :Usage:
            network_type = self.get_network_connect

        +--------------------+------+------+---------------+
        | Value (Alias)      | Data | Wi-fi| Airplane Mode |
        +====================+======+======+===============+
        | 0 (None)           | 0    | 0    | 0             |
        +--------------------+------+------+---------------+
        | 1 (Airplane Mode)  | 0    | 0    | 1             |
        +--------------------+------+------+---------------+
        | 2 (Wi-fi only)     | 0    | 1    | 0             |
        +--------------------+------+------+---------------+
        | 4 (Data only)      | 1    | 0    | 0             |
        +--------------------+------+------+---------------+
        | 6 (All network on) | 1    | 1    | 0             |
        +--------------------+------+------+---------------+
        """
        if isinstance(self.driver, AppDriver):
            return self.driver.network_connection
        raise NotImplementedError("The Web end does not support the 'get_network_connect' method!")

    def set_network_connect(self, connect_type: int) -> None:
        """
        Set the mobile network connection type.

        :param connect_type: 0 (None), 1 (Airplane Mode), 2 (Wi-fi only), 4 (Data only), 6 (All network on).
        :Usage:
            self.set_network_connect(2)
        """
        try:
            if isinstance(self.driver, AppDriver):
                self.driver.set_network_connection(connect_type)
                INFO.logger.info(f"Successfully set the network connection type: {connect_type}.")
            else:
                raise NotImplementedError("The Web end does not support the 'set_network_connect' method!")
        except WebDriverException as e:
            ERROR.logger.error(f"Failed to set the network connection type: {connect_type}, error message: {str(e)}")
            raise

    def press_keycode(self, keycode: int, metastate: Optional[int] = None, flags: Optional[int] = None) -> Self:
        """
        Sends a keycode to the device. Android only.
        Possible keycodes can be found in https://blog.csdn.net/feizhixuan46789/article/details/16801429.

        :param keycode: The keycode to be sent to the device.
        :param metastate: Meta information about the keycode being sent. e.g.: 1 (Shift), 2 (Ctrl), 4 (Alt).
        :param flags: The set of key event flags. e.g.: 0 (None), 1 (Long press).
        :return: Self instance.
        :Usage:
            self.press_keycode(66)

        List of commonly used keycodes:
        +--------------------+------------------+----------------------+
        | Keycode            | Keyname          | Description          |
        +====================+==================+======================+
        | 3                  | HOME             | 返回主屏幕            |
        +--------------------+------------------+----------------------+
        | 4                  | BACK             | 返回                 |
        +--------------------+------------------+----------------------+
        | 24                 | VOLUME_UP        | 增加音量             |
        +--------------------+------------------+----------------------+
        | 25                 | VOLUME_DOWN      | 减少音量             |
        +--------------------+------------------+----------------------+
        | 26                 | POWER            | 电源                 |
        +--------------------+------------------+----------------------+
        | 27                 | CAMERA           | 拍照                 |
        +--------------------+------------------+----------------------+
        | 66                 | ENTER            | 回车                 |
        +--------------------+------------------+----------------------+
        | 67                 | DELETE           | 删除                 |
        +--------------------+------------------+----------------------+
        | 82                 | MENU             | 菜单                 |
        +--------------------+------------------+----------------------+
        | 122                | MOVE_HOME        | 光标移动到行首        |
        +--------------------+------------------+----------------------+
        | 123                | MOVE_END         | 光标移动到行尾        |
        +--------------------+------------------+----------------------+
        | 187                | APP_SWITCH       | 切换应用             |
        +--------------------+------------------+----------------------+
        """
        try:
            if isinstance(self.driver, AppDriver):
                if metastate is not None and flags is not None:
                    self.driver.press_keycode(keycode, metastate, flags)
                elif metastate is not None:
                    self.driver.press_keycode(keycode, metastate)
                else:
                    self.driver.press_keycode(keycode)
                INFO.logger.info(f"Successfully sent the keycode: {keycode}.")
            else:
                raise NotImplementedError("The Web end does not support the 'press_keycode' method!")
        except WebDriverException as e:
            ERROR.logger.error(f"Failed to send the keycode: {keycode}, error message: {str(e)}")
            raise
        return self

    def open_notify(self) -> Self:
        """
        Open notification shade in Android.

        :Usage:
            self.open_notify()
        """
        try:
            if isinstance(self.driver, AppDriver):
                self.driver.open_notifications()
                INFO.logger.info("Successfully opened the notification shade.")
            else:
                raise NotImplementedError("The Web end does not support the 'open_notify' method!")
        except WebDriverException as e:
            ERROR.logger.error(f"Failed to open the notification shade, error message: {str(e)}")
            raise
        return self

    @property
    def contexts(self) -> List[str]:
        """
        Get all the contexts within the current session.

        :return: List of contexts. e.g.: ["NATIVE_APP", "WEBVIEW_com.example.app"]
        :Usage:
            contexts = self.contexts
            print(contexts)
        """
        if isinstance(self.driver, AppDriver):
            return self.driver.contexts
        raise NotImplementedError("The Web end does not support the 'contexts' method!")

    def switch_to_context(self, context_name: str) -> Self:
        """
        Sets the context for the current session.

        :param context_name: The name of the context to switch to.
        :Usage:
            self.switch_to_context("WEBVIEW_com.example.app")
        """
        try:
            if isinstance(self.driver, AppDriver):
                self.driver.switch_to.context(context_name)
                INFO.logger.info(f"Successfully switched to the context: {context_name}.")
            else:
                raise NotImplementedError("The Web end does not support the 'switch_to_context' method!")
        except WebDriverException as e:
            ERROR.logger.error(f"Failed to switch to the context: {context_name}, error message: {str(e)}")
            raise
        return self

    def find_element(self, selector: str, by: str = 'css_selector', timeout: Optional[int] = None) -> CustomWebElement:
        """
        Find a single element.

        :param selector: Element selector.
        :param by: Locator method.
        :param timeout: Timeout.
        :return: WebElement object.
        :Usage:
            element = self.find_element("#element_id")
        """
        temp_wait = self._wait if timeout is None else WebDriverWait(
            self.driver,
            timeout,
            poll_frequency=self._poll_frequency
        )

        try:
            locator = SelectorUtil.get_selenium_locator(selector, by)
            element = temp_wait.until(
                EC.presence_of_element_located(locator)
            )
            INFO.logger.info(f"Successfully found the element: {selector} (by={by}).")
            return CustomWebElement(self.driver, element.id)
        except TimeoutException:
            ERROR.logger.error(f"Timeout when finding the element: {selector} (by={by}).")
            self.take_screenshot("find_element_timeout")
            raise
        except Exception as e:
            ERROR.logger.error(f"Failed to find the element: {selector} (by={by}), error message: {str(e)}")
            self.take_screenshot("find_element_error")
            raise

    def find_elements(self, selector: str, by: str = 'css_selector', timeout: Optional[int] = None) -> List[WebElement]:
        """
        Find multiple elements.

        :param selector: Element selector.
        :param by: Locator method.
        :param timeout: Timeout.
        :return: List of WebElement objects.
        :Usage:
            elements = self.find_elements(".element_class")
        """
        temp_wait = self._wait if timeout is None else WebDriverWait(
            self.driver,
            timeout,
            poll_frequency=self._poll_frequency
        )

        try:
            locator = SelectorUtil.get_selenium_locator(selector, by)
            elements = temp_wait.until(
                EC.presence_of_all_elements_located(locator)
            )
            INFO.logger.info(f"Successfully found the elements: {selector} (by={by}).")
            return elements
        except TimeoutException:
            ERROR.logger.error(f"Timeout when finding the elements: {selector} (by={by}).")
            self.take_screenshot("find_elements_timeout")
            raise
        except Exception as e:
            ERROR.logger.error(f"Failed to find the elements: {selector} (by={by}), error message: {str(e)}")
            self.take_screenshot("find_elements_error")
            raise

    def send_keys(self, selector: str, text: str, by: str = 'css_selector') -> None:
        """
        Enter text into the specified element.

        :param selector: Element selector.
        :param text: Text to enter.
        :param by: Locator method.
        :Usage:
            self.send_keys("#input_field", "example text")
        """
        pass

    def download_image(self, element: WebElement, save_name: str, save_path: Optional[str] = None) -> Union[str, None]:
        """
        Download the image of the web page.

        :param element: WebElement object.
        :param save_name: Image file save name.
        :param save_path: Image file save path. Defaults to 'downloads_path'.
        :return: Image file full path.
        :Usage:
            img_el = self.find_element("img")
            image_path = self.download_image(img_el, "captcha.png")
            print(image_path)
        """
        try:
            if save_path is None:
                save_path = self.downloads_path

            os.makedirs(save_path, exist_ok=True)

            # Wait for the image element to load completely.
            self._wait.until(EC.visibility_of(element))

            # Get the src attribute of the image.
            image_src = element.get_attribute("src")

            if image_src.startswith("data:image"):
                # Handling base64 encoded images.
                header, encoded = image_src.split(",", 1)
                image_data = base64.b64decode(encoded)
                file_path = os.path.join(save_path, f"{save_name}")
                with open(file_path, "wb") as file:
                    file.write(image_data)
                INFO.logger.info(f"Succeeded in downloading the base64 image: {file_path}.")
            else:
                # Handling normal images.
                response = requests.get(image_src, stream=True)
                if response.status_code == 200:
                    file_path = os.path.join(save_path, f"{save_name}")
                    with open(file_path, 'wb') as file:
                        for chunk in response.iter_content(1024):
                            file.write(chunk)
                    INFO.logger.info(f"Succeeded in downloading the normal image: {file_path}.")
                else:
                    ERROR.logger.error(
                        f"Failed to download the image: {image_src}, status code: {response.status_code}.")
                    file_path = None

            return file_path

        except Exception as e:
            ERROR.logger.error(f"An unknown exception occurred when downloading the image: {str(e)}")
            return None

    def get_window_size(self, windowHandle: str = "current") -> dict:
        """
        Gets the width and height of the current window.

        :param windowHandle: Defaults to "current".
        :return: A dict containing the width and height of the window.
        :Usage:
            size = self.get_window_size()
            width, height = self.get_window_size().values()
        """
        try:
            size = self.driver.get_window_size(windowHandle)
            INFO.logger.info(f"Current window width: {size['width']}, height: {size['height']}.")
            return size
        except WebDriverException as e:
            ERROR.logger.error(f"Failed to get the window size: {str(e)}")
            raise

    def get_element_attribute(self, element: WebElement, attribute: str) -> str | None:
        """
        Get the value of the specified attribute of the element.

        :param element: WebElement object.
        :param attribute: Attribute name.
        :return: Attribute value.
        :Usage:
            value = self.get_element_attribute(element, "src")
        """
        try:
            attribute_value = element.get_attribute(attribute)
            INFO.logger.info(f"Successfully obtained the element attribute: {attribute}={attribute_value}.")
            return attribute_value
        except Exception as e:
            ERROR.logger.error(f"Failed to get the element attribute: {attribute}, error message: {str(e)}")
            self.take_screenshot("get_element_attribute_error")
            raise

    def refresh(self) -> None:
        """
        Refreshes the current page.

        :Usage:
            self.refresh()
        """
        try:
            self.driver.refresh()
            INFO.logger.info("Successfully refreshed the page.")
        except Exception as e:
            ERROR.logger.error(f"Failed to refresh the page: {str(e)}")
            self.take_screenshot("refresh_error")
            raise

    def back(self) -> None:
        """
        Returns to the previous page in the browser history.

        :Usage:
            self.back()
        """
        try:
            self.driver.back()
            INFO.logger.info("Successfully returned to the previous page.")
        except Exception as e:
            ERROR.logger.error(f"Failed to return to the previous page: {str(e)}")
            self.take_screenshot("back_error")
            raise

    def forward(self) -> None:
        """
        Forward to the next page in the browser history.

        :Usage:
            self.forward()
        """
        try:
            self.driver.forward()
            INFO.logger.info("Successfully moved forward to the next page.")
        except Exception as e:
            ERROR.logger.error(f"Failed to move forward to the next page: {str(e)}")
            self.take_screenshot("forward_error")
            raise

    def close(self) -> None:
        """
        Closes the current window.

        :Usage:
            self.close()
        """
        try:
            self.driver.close()
            INFO.logger.info("Successfully closed the current window.")
        except Exception as e:
            ERROR.logger.error(f"Failed to close the current window: {str(e)}")
            self.take_screenshot("close_error")
            raise

    def quit(self) -> None:
        """
        Quits the driver and closes all windows.

        :Usage:
            self.quit()
        """
        try:
            self.driver.quit()
            INFO.logger.info("Successfully exited the browser.")
        except Exception as e:
            ERROR.logger.error(f"Failed to exit the browser: {str(e)}")
            self.take_screenshot("quit_error")
            raise

    def maximize_window(self) -> None:
        """
        Maximizes the current window.

        :Usage:
            self.maximize_window()
        """
        try:
            self.driver.maximize_window()
            INFO.logger.info("Successfully maximized the window.")
        except Exception as e:
            ERROR.logger.error(f"Failed to maximize the window: {str(e)}")
            self.take_screenshot("maximize_window_error")
            raise

    def minimize_window(self) -> None:
        """
        Minimizes the current window.

        :Usage:
            self.minimize_window()
        """
        try:
            self.driver.minimize_window()
            INFO.logger.info("Successfully minimized the window.")
        except Exception as e:
            ERROR.logger.error(f"Failed to minimize the window: {str(e)}")
            self.take_screenshot("minimize_window_error")
            raise

    def switch_to_frame(self, frame: Union[str, int, WebElement]) -> None:
        """
        Switches focus to the specified frame, by index, name, or WebElement.

        :param frame: The name of the frame, index, or WebElement.
        :Usage:
            self.switch_to_frame("iframe_name")
            self.switch_to_frame(0)
            self.switch_to_frame(self.find_element("iframe"))
        """
        try:
            self.driver.switch_to.frame(frame)
            INFO.logger.info(f"Successfully switched to the frame: {frame}.")
        except Exception as e:
            ERROR.logger.error(f"Failed to switch to the frame: {frame}, error message: {str(e)}")
            self.take_screenshot("switch_to_frame_error")
            raise

    def switch_to_default_frame(self) -> None:
        """
        Switches focus to the default frame.

        :Usage:
            self.switch_to_default_frame()
        """
        try:
            self.driver.switch_to.default_content()
            INFO.logger.info("Successfully switched to the default frame.")
        except Exception as e:
            ERROR.logger.error(f"Failed to switch to the default frame: {str(e)}")
            self.take_screenshot("switch_to_default_frame_error")
            raise

    def execute_script(self, script: str, *args) -> Any:
        """
        Synchronously Executes JavaScript in the current window/frame.

        :param script: JavaScript code to execute.
        :param args: Arguments to pass to the script.
        :return: The result of the script.
        :Usage:
            result = self.execute_script("return document.title;")
        """
        try:
            result = self.driver.execute_script(script, *args)
            INFO.logger.info(f"Successfully executed JavaScript code: {script}.")
            return result
        except Exception as e:
            ERROR.logger.error(f"Failed to execute JavaScript code: {script}, error message: {str(e)}")
            self.take_screenshot("execute_script_error")
            raise

    def scroll_to(self, x_offset: Optional[int] = None, y_offset: Optional[int] = None,
                  element: Optional[WebElement] = None) -> None:
        """
        Scroll the page by the specified offsets or to the specified element.

        :param x_offset: Horizontal offset. Positive values scroll right, negative values scroll left.
        :param y_offset: Vertical offset. Positive values scroll down, negative values scroll up.
        :param element: WebElement to scroll to. The element will be centered vertically.
        :Usage:
            self.scroll_to(x_offset=100, y_offset=200)
            self.scroll_to(element=some_element)
        """
        try:
            self.switch_to_default_frame()  # Switch to the default content
            if element:
                # Scroll to the element and center it vertically
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                INFO.logger.info(f"Successfully scrolled to the element: {element}.")
            elif x_offset is not None or y_offset is not None:
                # Scroll by the specified offsets
                x_offset = x_offset or 0
                y_offset = y_offset or 0
                self.driver.execute_script(f"window.scrollBy({x_offset}, {y_offset});")
                INFO.logger.info(f"Successfully scrolled by offsets: x={x_offset}, y={y_offset}.")
            else:
                raise ValueError("Either x_offset/y_offset or element must be provided.")
        except Exception as e:
            ERROR.logger.error(f"Failed to scroll, error message: {str(e)}")
            self.take_screenshot("scroll_error")
            raise

    def scroll_to_top(self) -> None:
        """
        Scroll to the top of the page.

        :Usage:
            self.scroll_to_top()
        """
        try:
            self.switch_to_default_frame()  # Switch to the default content
            self.driver.execute_script("window.scrollTo(0, 0);")
            INFO.logger.info("Successfully scrolled to the top of the page.")
        except Exception as e:
            ERROR.logger.error(f"Failed to scroll to the top of the page, error message: {str(e)}")
            self.take_screenshot("scroll_to_top_error")
            raise

    def scroll_to_bottom(self) -> None:
        """
        Scroll to the bottom of the page.

        :Usage:
            self.scroll_to_bottom()
        """
        try:
            self.switch_to_default_frame()  # Switch to the default content
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            INFO.logger.info("Successfully scrolled to the bottom of the page.")
        except Exception as e:
            ERROR.logger.error(f"Failed to scroll to the bottom of the page, error message: {str(e)}")
            self.take_screenshot("scroll_to_bottom_error")
            raise

    @property
    def current_url(self) -> str:
        """
        Gets the URL of the current page.

        :return: The URL of the current page.
        :Usage:
            url = self.current_url
        """
        try:
            url = self.driver.current_url
            return url
        except Exception as e:
            ERROR.logger.error(f"Failed to get the current URL: {str(e)}")
            self.take_screenshot("current_url_error")
            raise

    @property
    def current_window_handle(self) -> str:
        """
        Gets the current window handle.

        :return: The current window handle.
        :Usage:
            handle = self.current_window_handle
        """
        try:
            handle = self.driver.current_window_handle
            return handle
        except Exception as e:
            ERROR.logger.error(f"Failed to get the current window handle: {str(e)}")
            self.take_screenshot("current_window_handle_error")
            raise

    @property
    def current_page_title(self) -> str:
        """
        Gets the title of the current page.

        :return: The title of the current page.
        :Usage:
            title = self.current_page_title
        """
        try:
            title = self.driver.title
            INFO.logger.info(f"Successfully obtained the page title: {title}")
            return title
        except Exception as e:
            ERROR.logger.error(f"Failed to get the page title: {str(e)}")
            self.take_screenshot("current_page_title_error")
            raise

    @property
    def current_page_code(self) -> str:
        """
        Gets the source code of the current page.

        :return: The source code of the current page.
        :Usage:
            source = self.page_source
        """
        try:
            source = self.driver.page_source
            INFO.logger.info("Successfully obtained the page source code.")
            return source
        except Exception as e:
            ERROR.logger.error(f"Failed to get the page source code: {str(e)}")
            self.take_screenshot("current_page_code_error")
            raise

    def tap(self, pos: List[Tuple[int, int]], duration: Optional[int] = None) -> Self:
        """
        Function: Simulates a click operation at the specified coordinates. (App only)
        Scenario: Applicable to scenarios where multiple click operations need to be simulated at different screen locations.
        e.g. 'Red envelope rain'.

        :param pos: A tuple array containing x/y positions, up to 5 in length.
        :param duration: Single click duration (ms)
        :return: Self instance.
        :Usage:
            self.tap([(100, 20), (100, 60), (100, 100)], 500)
        """
        if len(pos) > 5:
            raise ValueError("The maximum number of taps is 5.")
        try:
            if isinstance(self.driver, AppDriver):
                self.driver.tap(pos, duration)
                INFO.logger.info(f"Successfully tapped the positions: {pos}.")
            else:
                raise NotImplementedError("The Web end does not support the 'tap' method!")
        except WebDriverException as e:
            ERROR.logger.error(f"Failed to tap the positions: {pos}, error message: {e}")
            raise
        return self

    def drag_and_drop(self, start_element: WebElement, end_element: WebElement, pause: Optional[float] = None) -> Self:
        """
        Function: Drag the origin element to the destination element. (App only)
        Scenario: Applicable to scenarios where elements need to be dragged and dropped.
        e.g. 'Slider captcha'.

        :param start_element: The element to drag.
        :param end_element: The element to drag to.
        :param pause: Pause time (seconds), in float seconds.
        :return: Self instance.
        :Usage:
            self.drag_and_drop(el1, el2, 0.2)
        """
        try:
            if isinstance(self.driver, AppDriver):
                self.driver.drag_and_drop(start_element, end_element, pause)
                INFO.logger.info(f"Successfully dragged the element from {start_element} to {end_element}.")
            else:
                raise NotImplementedError("The Web end does not support the 'drag_and_drop' method!")
        except WebDriverException as e:
            ERROR.logger.error(f"Failed to drag the element from {start_element} to {end_element}, error message: {e}")
            raise
        return self

    def scroll(self, start_element: WebElement, end_element: WebElement, duration: Optional[int] = None) -> Self:
        """
        Function: Scrolls from one element to another. (App only)
        Scenario: Applicable to scenarios where you need to scroll from one element to another.
        e.g. 'Scroll to the bottom of the page'.

        :param start_element: The element from which to begin scrolling (center of element).
        :param end_element: The element to scroll to (center of element).
        :param duration: Duration of the scroll (ms), defaults to 600ms.
        :return: Self instance.
        :Usage:
            self.scroll(el1, el2, 1000)
        """
        try:
            if isinstance(self.driver, AppDriver):
                self.driver.scroll(start_element, end_element, duration)
                INFO.logger.info(f"Successfully scrolled from {start_element} to {end_element}.")
            else:
                raise NotImplementedError("The Web end does not support the 'scroll' method!")
        except WebDriverException as e:
            ERROR.logger.error(f"Failed to scroll from {start_element} to {end_element}, error message: {e}")
            raise
        return self

    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: int = None) -> Self:
        """
        Function: Slowly slide the screen from one point to another. (App only)
        Scenario: Applicable to scenarios where you need to slide slowly or control the sliding speed precisely.
        e.g. browsing content or scrolling pages.

        :param start_x: Starting X coordinate.
        :param start_y: Starting Y coordinate.
        :param end_x: Ending X coordinate.
        :param end_y: Ending Y coordinate.
        :param duration: Duration of the swipe (ms).
        :Usage:
            self.swipe(100, 200, 300, 400, 1000)
        """
        try:
            if isinstance(self.driver, AppDriver):
                self.driver.swipe(start_x, start_y, end_x, end_y, duration)
                INFO.logger.info(
                    f"Successfully swiped from ({start_x}, {start_y}) to ({end_x}, {end_y}) with duration {duration}ms.")
            else:
                raise NotImplementedError("The Web end does not support the 'swipe' method!")
        except WebDriverException as e:
            ERROR.logger.error(
                f"Failed to swipe from ({start_x}, {start_y}) to ({end_x}, {end_y}), error message: {str(e)}")
            raise
        return self

    def flick(self, start_x: int, start_y: int, end_x: int, end_y: int) -> Self:
        """
        Function: Quickly flick the screen from one point to another. (App only)
        Scenario: Applicable to scenarios where you need to quickly scroll the screen.
        e.g. quickly browse a long list or quickly switch images.

        :param start_x: Starting X coordinate.
        :param start_y: Starting Y coordinate.
        :param end_x: Ending X coordinate.
        :param end_y: Ending Y coordinate.
        :Usage:
            self.flick(100, 200, 300, 400)
        """
        try:
            if isinstance(self.driver, AppDriver):
                self.driver.flick(start_x, start_y, end_x, end_y)
                INFO.logger.info(f"Successfully flicked from ({start_x}, {start_y}) to ({end_x}, {end_y}).")
            else:
                raise NotImplementedError("The Web end does not support the 'flick' method!")
        except WebDriverException as e:
            ERROR.logger.error(f"Failed to flick from ({start_x}, {start_y}) to ({end_x}, {end_y}), error message: {e}")
            raise
        return self