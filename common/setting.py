#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@ Date        : 2024/11/16 下午3:40
@ Author      : Poco Ray
@ File        : setting.py
@ Description : 实现不同操作系统的路径分离, 以兼容 Windows 和 Linux 不同环境的操作系统路径.
"""
import os
from typing import Text, Dict, Any


def root_path() -> str:
    """
    :return: 项目根路径
    """
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return path


def ensure_path_sep(path: Text) -> Text:
    """
    功能: 实现不同操作系统的路径分离, 以兼容 Windows 和 Linux 不同环境的操作系统路径.
    :param path: path路径(任意一种操作系统路径的格式都可以).
    :return: 视操作系统返回不同的路径, 路径分隔符自动转换为当前操作系统的路径分隔符.
    """
    if "/" in path:
        path = os.sep.join(path.split("/"))

    if "\\" in path:
        path = os.sep.join(path.split("\\"))

    return root_path() + path


class Settings:
    """项目配置类"""

    @property
    def project_paths(self) -> Dict[str, str]:
        """项目相关路径"""
        return {
            'root': root_path(),
            'datas': ensure_path_sep('/datas'),
            'screenshots': ensure_path_sep('/datas/screenshots'),
            'logs': ensure_path_sep('/logs'),
            'report': ensure_path_sep('/report'),
        }

    @property
    def global_config(self) -> Dict[str, Any]:
        """全局配置参数"""
        return {
            # WebDriver相关配置
            'webdriver_timeout': 10,  # WebDriver超时时间（秒）
            'webdriver_poll_frequency': 0.5,  # 轮询频率（秒）
            'implicit_timeout': 10,  # 隐式等待时间（秒）
            'page_load_timeout': 30,  # 页面加载超时时间（秒）

            # 下载文件相关配置
            'downloads_dir': ensure_path_sep('\\datas\\downloads'),  # 下载文件目录
            'clean_downloads': True,  # 是否清理历史下载文件

            # 截图相关配置
            'screenshots_dir': ensure_path_sep('\\datas\\screenshots'),  # 截图目录
            'clean_screenshots': True,  # 是否清理历史截图
            'screenshot_format': 'png',  # 截图格式

            # 日志相关配置
            'logs_dir': ensure_path_sep('\\logs'),  # 日志目录
            'clean_logs': True,  # 是否清理历史日志
            'log_level': 'INFO',  # 日志级别
            'log_format': '%(asctime)s [%(levelname)s] %(message)s',  # 日志格式
            'log_date_format': '%Y-%m-%d %H:%M:%S',  # 日志日期格式

            # 报告相关配置
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
