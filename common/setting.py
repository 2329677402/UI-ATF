#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@ Date        : 2024/11/16 下午3:40
@ Author      : Poco Ray
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
    def project_paths(self) -> Dict[str, str]:
        """ Project paths """
        return {
            'root': root_path(),
            'datas': ensure_path_sep('/datas'),
            'screenshots': ensure_path_sep('/datas/screenshots'),
            'logs': ensure_path_sep('/logs'),
            'report': ensure_path_sep('/report'),
        }

    @property
    def global_config(self) -> Dict[str, Any]:
        """ Project parameters """
        return {
            # WebDriver related configuration
            'webdriver_timeout': 10,  # WebDriver timeout (seconds)
            'webdriver_poll_frequency': 0.5,  # Polling frequency (seconds)
            'implicit_timeout': 10,  # Implicit wait time (seconds)
            'page_load_timeout': 30,  # Page load timeout (seconds)

            # Download related configuration
            'downloads_dir': ensure_path_sep('\\datas\\downloads'),  # 下载文件目录
            'clean_downloads': True,  # 是否清理历史下载文件

            # Screenshot related configuration
            'screenshots_dir': ensure_path_sep('\\datas\\screenshots'),  # 截图目录
            'clean_screenshots': True,  # 是否清理历史截图
            'screenshot_format': 'png',  # 截图格式

            # Log related configuration
            'logs_dir': ensure_path_sep('\\logs'),  # 日志目录
            'clean_logs': True,  # 是否清理历史日志
            'log_level': 'INFO',  # 日志级别
            'log_format': '%(asctime)s [%(levelname)s] %(message)s',  # 日志格式
            'log_date_format': '%Y-%m-%d %H:%M:%S',  # 日志日期格式

            # Report related configuration
            'report_dir_name': 'reports',  # 报告目录名称
            'report_format': 'html',  # 报告格式
            'report_title': 'UI自动化测试报告',  # 报告标题
            'report_description': 'UI自动化测试执行结果',  # 报告描述
        }

    def get_path(self, key: str) -> str:
        """获取指定路径"""
        return self.project_paths.get(key, '')

    @staticmethod
    def ensure_path_exists(path_str: str) -> None:
        """确保路径存在"""
        if not os.path.exists(path_str):
            os.makedirs(path_str)


# 创建全局配置实例
settings = Settings()

# 测试
if __name__ == '__main__':
    print(root_path())
    print(ensure_path_sep("\\report\\html"))
    print(ensure_path_sep("/report/html"))
