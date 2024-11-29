#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@ Date        : 2024/11/1 下午9:08
@ Author      : Poco Ray
@ File        : run.py
@ Description : 入口文件，用于执行整个自动化测试生成Allure报告并发送通知.
"""
import os
import traceback
import pyfiglet
import pytest
from utils.other_tool.models import NotificationType
from utils.other_tool.allure_data.allure_report_data import AllureFileClean
from utils.log_tool.log_control import INFO, ERROR
from utils.notify_tool.send_wechat import WeChatSend
from utils.notify_tool.send_ding import DingTalkSendMsg
from utils.notify_tool.send_mail import SendEmail
from utils.notify_tool.send_lark import FeiShuTalkChatBot
from utils import config


def run():
    try:
        # 打印项目信息
        ascii_banner = pyfiglet.figlet_format(config.project_name)
        print(ascii_banner)
        INFO.logger.info(f"开始执行{config.project_name}项目...")

        # 创建报告目录
        for dir_path in ['./report/tmp', './report/html']:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

        # 运行测试
        pytest_args = [
            'tests/test_web/test_web_login.py',  # 指定测试文件
            '-v',  # 详细输出
            '--alluredir=./report/tmp',  # Allure 报告目录
            '--clean-alluredir',  # 清理已有报告
            '--capture=no',  # 允许打印输出
        ]
        
        # 如果安装了 pytest-xdist，可以启用并行执行
        try:
            import pytest_xdist
            pytest_args.extend(['-n', 'auto'])
        except ImportError:
            INFO.logger.warning("pytest-xdist not installed. Running tests in sequence.")

        exit_code = pytest.main(pytest_args)
        
        if exit_code != 0:
            ERROR.logger.error(f"测试执行失败，退出码: {exit_code}")
            return

        # 生成报告
        INFO.logger.info("生成 Allure 报告...")
        os.system(f"allure generate ./report/tmp -o ./report/html --clean")

        # 发送通知
        if config.notification_type != NotificationType.DEFAULT.value:
            allure_data = AllureFileClean().get_case_count()
            notification_mapping = {
                NotificationType.DING_TALK.value: DingTalkSendMsg(allure_data).send_ding_notification,
                NotificationType.WECHAT.value: WeChatSend(allure_data).send_wechat_notification,
                NotificationType.EMAIL.value: SendEmail(allure_data).send_main,
                NotificationType.FEI_SHU.value: FeiShuTalkChatBot(allure_data).post
            }
            notification_mapping.get(config.notification_type)()

        # 启动报告服务
        INFO.logger.info("启动 Allure 报告服务...")
        os.system(f"allure serve ./report/tmp -p 53230")

    except Exception as e:
        ERROR.logger.error(f"测试执行失败: {str(e)}")
        ERROR.logger.error(traceback.format_exc())
        # 发送错误邮件
        send_email = SendEmail(AllureFileClean.get_case_count())
        send_email.error_mail(traceback.format_exc())
        raise


if __name__ == '__main__':
    run()
