from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BaseUtil:
    def __init__(self, driver):
        self.driver = driver

    def type(self, by=By.CSS_SELECTOR, locator='', text='', timeout=10, retry=False):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, locator))
            )
            element.clear()
            element.send_keys(text)
        except Exception as e:
            if retry:
                self.type(by, locator, text, timeout, retry=False)
            else:
                raise e

    def open(self, url):
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete'
        )

    def click(self, by=By.CSS_SELECTOR, locator='', timeout=10):
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, locator))
        )
        element.click()

    def swipe(self, start_x, start_y, end_x, end_y, duration):
        self.driver.swipe(start_x, start_y, end_x, end_y, duration)

    def sleep(self, seconds):
        self.driver.implicitly_wait(seconds)

    def close_app(self):
        self.driver.quit()
