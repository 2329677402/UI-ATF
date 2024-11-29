import pytest
from tests.test_base_case import BaseCaseWeb


class TestWebLogin(BaseCaseWeb):
    @pytest.fixture(autouse=True)
    def setup(self, web_driver):
        """
        设置测试环境
        """
        print("开始设置测试环境")
        self.driver = web_driver
        self.setUp()
        print("测试环境设置完成")

    @pytest.mark.web
    def test_web_login(self):
        """
        测试Web端登录功能
        """
        try:
            print("开始执行登录测试")
            self.login()
            print("登录测试执行完成")
        except Exception as e:
            print(f"登录测试失败: {str(e)}")
            pytest.fail(f"登录失败: {str(e)}")
