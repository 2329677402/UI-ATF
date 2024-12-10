#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@ Date        : 12/10/2024 10:18 PM
@ Author      : Administrator
@ File        : setting.py
@ Description : Global configuration parameters for the project.
"""
import os
from typing import Text, Dict, Any


def root_path() -> str:
    """
    :return: Project root path.
    """
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return path


def ensure_path_sep(path: Text) -> Text:
    """
    Ensure that the path separator is consistent with the current operating system.

    :param path: Path string.
    :return: Path string with consistent separator.
    """
    if "/" in path:
        path = os.sep.join(path.split("/"))

    if "\\" in path:
        path = os.sep.join(path.split("\\"))

    return root_path() + path


class Settings:
    """ Global Configuration Class """

    @property
    def global_config(self) -> Dict[str, Any]:
        """
        Project global config.

        :return: Defined project global_config.
        """
        return {
            # WebDriver related configuration
            'webdriver_timeout': 10,
            'webdriver_poll_frequency': 0.5,
            'implicit_timeout': 10,
            'page_load_timeout': 30,

            # Download related configuration
            'downloads_dir': ensure_path_sep('\\datas\\downloads'),
            'clean_downloads': True,

            # Screenshot related configuration
            'screenshots_dir': ensure_path_sep('\\datas\\screenshots'),
            'clean_screenshots': True,
            'screenshot_format': 'png',

            # Log related configuration
            'logs_dir': ensure_path_sep('\\logs'),
            'clean_logs': True,
            'log_level': 'INFO',
            'log_format': '%(asctime)s [%(levelname)s] %(message)s',
            'log_date_format': '%Y-%m-%d %H:%M:%S',

            # Report related configuration
            'report_dir': ensure_path_sep('\\report'),
            'report_tmp': ensure_path_sep('\\report\\tmp'),
            'report_html': ensure_path_sep('\\report\\html'),
            'report_format': 'html',
            'report_title': 'UI自动化测试报告',
            'report_description': 'UI自动化测试执行结果',

            # Other configuration
            'config_dir': ensure_path_sep('\\common\\config.yaml'),
        }

    def get_global_config(self, key: str) -> str:
        """
        Get the path based on the key.

        :param key: Path key.
        :return: Full path.
        :Usage:
            print(settings.get_path('logs'))
        """
        return self.global_config.get(key, '')


# 创建全局配置实例
settings = Settings()

# 测试
if __name__ == '__main__':
    print(root_path())
    print(ensure_path_sep("\\report\\html"))
    print(ensure_path_sep("/report/html"))
    print(settings.get_global_config('config_dir'))
