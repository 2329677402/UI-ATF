import os
import time
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.api_tool.locator import Locator
from config.setting import ensure_path_sep, root_path
from utils.log_tool.log_control import INFO, ERROR


class BaseUtil:
    def __init__(self, driver):
        """
        初始化 BaseUtil
        :param driver: WebDriver实例
        """
        if driver is None:
            raise ValueError("Driver cannot be None")
        self.driver = driver
        self._create_directories()

    @staticmethod
    def _create_directories():
        """创建必要的目录"""
        try:
            # 在根目录下创建 logs 目录
            log_dir = os.path.join(root_path(), 'logs')
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)

            # 在根目录下的 datas 目录中创建必要的子目录
            data_dir = os.path.join(root_path(), 'datas')
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
            
            for dir_name in ['screenshots', 'recordings']:
                dir_path = os.path.join(data_dir, dir_name)
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
        except Exception as e:
            ERROR.logger.error(f"创建目录失败: {str(e)}")
            raise

    def take_screenshot(self, name=None):
        """
        截取当前页面截图
        :param name: 截图名称，默认使用时间戳
        :return: 截图文件路径
        """
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{name}_{timestamp}.png" if name else f"screenshot_{timestamp}.png"
            # 使用 datas/screenshots 目录
            filepath = os.path.join(root_path(), 'datas', 'screenshots', filename)

            self.driver.save_screenshot(filepath)
            INFO.logger.info(f"截图保存成功: {filepath}")
            return filepath
        except Exception as e:
            ERROR.logger.error(f"截图失败: {str(e)}")
            return None

    def start_screen_recording(self):
        """
        开始录制屏幕（仅支持移动端）
        """
        try:
            if hasattr(self.driver, 'start_recording_screen'):
                self.driver.start_recording_screen()
                INFO.logger.info("开始录制屏幕")
            else:
                ERROR.logger.error("当前driver不支持录制屏幕")
        except Exception as e:
            ERROR.logger.error(f"开始录制屏幕失败: {str(e)}")

    def stop_screen_recording(self, name=None):
        """
        停止录制屏幕并保存（仅支持移动端）
        :param name: 视频名称，默认使用时间戳
        :return: 视频文件路径
        """
        try:
            if hasattr(self.driver, 'stop_recording_screen'):
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{name}_{timestamp}.mp4" if name else f"recording_{timestamp}.mp4"
                # 使用 datas/recordings 目录
                filepath = os.path.join(root_path(), 'datas', 'recordings', filename)

                video_data = self.driver.stop_recording_screen()
                with open(filepath, "wb") as f:
                    f.write(video_data)

                INFO.logger.info(f"录屏保存成功: {filepath}")
                return filepath
            else:
                ERROR.logger.error("当前driver不支持录制屏幕")
                return None
        except Exception as e:
            ERROR.logger.error(f"停止录制屏幕失败: {str(e)}")
            return None

    def wait_for_element(self, locator: Locator, timeout=10, condition=EC.presence_of_element_located):
        """
        等待元素满足指定条件
        :param locator: 元素定位器
        :param timeout: 超时时间（秒）
        :param condition: 等待条件，默认为元素存在
        :return: 目标元素
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                condition(locator.to_selenium())
            )
            return element
        except Exception as e:
            ERROR.logger.error(f"等待元素失败: {str(e)}")
            self.take_screenshot("wait_failed")
            raise

    def type(self, locator: Locator, text='', timeout=10, retry=False):
        """
        输入文本
        :param locator: 元素定位器
        :param text: 要输入的文本
        :param timeout: 超时时间（秒）
        :param retry: 失败是否重试
        """
        try:
            element = self.wait_for_element(locator, timeout)
            element.clear()
            element.send_keys(text)
        except Exception as e:
            if retry:
                self.type(locator, text, timeout, retry=False)
            else:
                ERROR.logger.error(f"输入文本失败: {str(e)}")
                self.take_screenshot("type_failed")
                raise

    def click(self, locator: Locator, timeout=10):
        """
        点击元素
        :param locator: 元素定位器
        :param timeout: 超时时间（秒）
        """
        try:
            element = self.wait_for_element(
                locator,
                timeout,
                condition=EC.element_to_be_clickable
            )
            element.click()
        except Exception as e:
            ERROR.logger.error(f"点击元素失败: {str(e)}")
            self.take_screenshot("click_failed")
            raise

    def get_element_text(self, locator: Locator, timeout=10):
        """
        获取元素文本
        :param locator: 元素定位器
        :param timeout: 超时时间（秒）
        :return: 元素文本内容
        """
        try:
            element = self.wait_for_element(locator, timeout)
            return element.text
        except Exception as e:
            ERROR.logger.error(f"获取元素文本失败: {str(e)}")
            self.take_screenshot("get_text_failed")
            raise

    def is_element_present(self, locator: Locator, timeout=3):
        """
        判断元素是否存在
        :param locator: 元素定位器
        :param timeout: 超时时间（秒）
        :return: 元素是否存在
        """
        try:
            self.wait_for_element(locator, timeout)
            return True
        except:
            return False

    def open(self, url):
        """
        打开网页
        :param url: 目标URL
        """
        try:
            self.driver.get(url)
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.execute_script('return document.readyState') == 'complete'
            )
        except Exception as e:
            ERROR.logger.error(f"打开页面失败: {str(e)}")
            self.take_screenshot("open_failed")
            raise

    def swipe(self, start_x, start_y, end_x, end_y, duration=None):
        """
        滑动屏幕（仅支持移动端）
        :param start_x: 起始x坐标
        :param start_y: 起始y坐标
        :param end_x: 结束x坐标
        :param end_y: 结束y坐标
        :param duration: 持续时间（毫秒）
        """
        try:
            if hasattr(self.driver, 'swipe'):
                self.driver.swipe(start_x, start_y, end_x, end_y, duration)
            else:
                ERROR.logger.error("当前driver不支持滑动操作")
        except Exception as e:
            ERROR.logger.error(f"滑动失败: {str(e)}")
            self.take_screenshot("swipe_failed")
            raise

    def sleep(self, seconds):
        """
        等待指定时间
        :param seconds: 等待秒数
        """
        time.sleep(seconds)

    def close(self):
        """关闭当前窗口"""
        try:
            self.driver.close()
        except Exception as e:
            ERROR.logger.error(f"关闭窗口失败: {str(e)}")

    def quit(self):
        """退出浏览器"""
        try:
            self.driver.quit()
        except Exception as e:
            ERROR.logger.error(f"退出浏览器失败: {str(e)}")
