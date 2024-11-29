import pytest
from tests.test_base_case import BaseCaseApp


class TestAppLogin(BaseCaseApp):
    @pytest.fixture(autouse=True)
    def setup(self, app_driver):
        self.driver = app_driver
        self.setUp()

    def test_app_login(self):
        self.login('admin', 'yl123456')
