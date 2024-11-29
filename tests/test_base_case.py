from utils.base_util import BaseUtil


class BaseCase:
    driver = None
    base_util = None

    def setUp(self):
        self.base_util = BaseUtil(self.driver)

    def login(self):
        # 实现登录逻辑
        pass


class BaseCaseWeb(BaseCase):
    def login(self):
        # 实现Web端登录逻辑
        self.base_util.open("http://192.168.124.73:8008/login")  # 替换为实际的登录URL
        self.base_util.type("input[placeholder='账号']", "admin")
        self.base_util.type("input[placeholder='密码']", "yl123456")
        self.base_util.click("button[type='button']")


class BaseCaseApp(BaseCase):
    def login(self):
        # 实现App端登录逻辑
        pass
