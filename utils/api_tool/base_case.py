from utils.api_tool.base_actions import BaseActions


class BaseCase:
    """测试基类"""
    driver = None
    _actions = None

    def __getattr__(self, name):
        """代理到BaseActions的方法"""
        if self._actions is None:
            raise ValueError("Actions not initialized")
        return getattr(self._actions, name)

    def setup_actions(self):
        """初始化操作类"""
        if self.driver is None:
            raise ValueError("Driver must be initialized before running tests")
        self._actions = BaseActions(self.driver)
        self._actions.clean_screenshots()  # 清理历史截图
