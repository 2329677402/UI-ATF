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
            'tests/test_web/test_web_login.py',
            '-v',
            '--alluredir=./report/tmp',
            '--clean-alluredir',
            '--capture=no',
        ]

        try:
            pytest_args.extend(['-n', '4'])
        except ImportError:
            INFO.logger.warning("pytest-xdist未安装. 按顺序运行测试.")

        exit_code = pytest.main(pytest_args)

        if exit_code != 0:
            ERROR.logger.error(f"测试执行失败，退出码: {exit_code}")
            # 不要在这里直接返回，继续尝试生成报告

        # 生成报告
        INFO.logger.info("生成 Allure 报告...")
        os.system(f"allure generate ./report/tmp -o ./report/html --clean")

        # 发送通知
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
                ERROR.logger.error(f"发送通知失败: {str(e)}")

        # 启动报告服务
        INFO.logger.info("启动 Allure 报告服务...")
        os.system(f"allure serve ./report/tmp -p 53230")

    except Exception as e:
        ERROR.logger.error(f"测试执行失败: {str(e)}")
        ERROR.logger.error(traceback.format_exc())
        # 尝试发送错误邮件，但不抛出新的异常
        try:
            send_email = SendEmail(AllureFileClean.get_case_count())
            send_email.error_mail(traceback.format_exc())
        except Exception as mail_error:
            ERROR.logger.error(f"发送错误邮件失败: {str(mail_error)}")
        raise

if __name__ == '__main__':
    run()