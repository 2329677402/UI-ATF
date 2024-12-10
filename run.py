#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@ Date        : 12/10/2024 10:44 PM
@ Author      : Administrator
@ File        : run.py
@ Description : Test execution entry file.
"""
import os
import shutil
import traceback
import pyfiglet
import pytest
from common.setting import Settings
from utils import config
from utils.other_tool.models import NotificationType
from utils.other_tool.allure_data.allure_report_data import AllureFileClean
from utils.log_tool.log_control import INFO, ERROR
from utils.notify_tool.send_wechat import WeChatSend
from utils.notify_tool.send_ding import DingTalkSendMsg
from utils.notify_tool.send_mail import SendEmail
from utils.notify_tool.send_lark import FeiShuTalkChatBot


def run():
    try:
        # Print the project name in ASCII art.
        ascii_banner = pyfiglet.figlet_format(config.project_name)
        print(ascii_banner)
        INFO.logger.info(f"Start running test cases for project: {config.project_name}...")

        settings = Settings()
        report_tmp = settings.get_global_config('report_tmp')
        report_html = settings.get_global_config('report_html')
        # Clean up the report directory.
        for dir_path in [report_tmp, report_html]:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
                INFO.logger.info(f"Report child directory created: {dir_path}.")
            else:
                shutil.rmtree(dir_path)
                os.makedirs(dir_path, exist_ok=True)
                INFO.logger.info("Report files cleanup completed.")

        # Run test cases.
        pytest_args = ['-s', '-W', 'ignore:Module already imported:pytest.PytestWarning',
                       '--alluredir', './report/tmp', "--clean-alluredir"]

        try:
            pytest_args.extend(['-n', 'auto'])
        except ImportError:
            INFO.logger.warning("The pytest-xdist plugin is not installed, so the test cases will be executed serially.")

        exit_code = pytest.main(pytest_args)

        if exit_code != 0:
            ERROR.logger.error(f"Test execution failed with exit code: {exit_code}.")
            # 不要在这里直接返回，继续尝试生成报告

        # Generate Allure report.
        INFO.logger.info("Generating Allure report...")
        os.system(f"allure generate ./report/tmp -o ./report/html --clean")

        # Send notification.
        if config.notification_type != NotificationType.DEFAULT.value:
            try:
                allure_data = AllureFileClean().get_case_count()
                notification_mapping = {
                    NotificationType.DING_TALK.value: DingTalkSendMsg(allure_data).send_ding_notification,
                    NotificationType.WECHAT.value: WeChatSend(allure_data).send_wechat_notification,
                    NotificationType.EMAIL.value: SendEmail(allure_data).send_main,
                    NotificationType.FEI_SHU.value: FeiShuTalkChatBot(allure_data).post
                }
                notification_func = notification_mapping.get(config.notification_type)
                if notification_func:
                    notification_func()
            except Exception as e:
                ERROR.logger.error(f"Failed to send notification: {str(e)}")

        # Start Allure report service.
        INFO.logger.info("Starting Allure report service...")
        os.system(f"allure serve ./report/tmp -p 53230")

    except Exception as e:
        ERROR.logger.error(f"An unknown exception occurred, error message: {str(e)}")
        ERROR.logger.error(traceback.format_exc())
        # Send error email.
        try:
            send_email = SendEmail(AllureFileClean.get_case_count())
            send_email.error_mail(traceback.format_exc())
        except Exception as mail_error:
            ERROR.logger.error(f"Failed to send error email: {str(mail_error)}")
        raise


if __name__ == '__main__':
    run()
