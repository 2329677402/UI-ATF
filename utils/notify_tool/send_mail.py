#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@ Date        : 2024/11/29 下午5:11
@ Author      : Administrator
@ File        : send_mail.py
@ Description : 功能描述
"""
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@ Date        : 2024/11/16 下午2:51
@ Author      : Poco Ray
@ File        : send_mail.py
@ Description : 发送邮件通知
"""
import smtplib
from email.mime.text import MIMEText
from utils.other_tool.allure_data.allure_report_data import TestMetrics, AllureFileClean
from utils import config


class SendEmail:
    """ 发送邮箱 """

    def __init__(self, metrics: TestMetrics):
        self.metrics = metrics  # 测试指标
        self.allure_data = AllureFileClean()  # Allure数据清理
        self.CaseDetail = self.allure_data.get_failed_cases_detail()  # 失败用例详情

    @classmethod
    def send_mail(cls, user_list: list, sub, content: str) -> None:
        """
        功能：使用smtplib库发送邮件
        :param user_list: 发件人邮箱
        :param sub: 邮件主题
        :param content: 发送内容
        :return:
        """
        user = "Poco" + "<" + config.email.send_user + ">"
        message = MIMEText(content, _subtype='plain', _charset='utf-8')
        message['Subject'] = sub
        message['From'] = user
        message['To'] = ";".join(user_list)
        server = smtplib.SMTP()
        server.connect(config.email.email_host)
        server.login(config.email.send_user, config.email.stamp_key)
        server.sendmail(user, user_list, message.as_string())
        server.close()

    def error_mail(self, error_message: str) -> None:
        """
        功能：发送异常邮件通知
        :param error_message: 报错信息
        :return:
        """
        email = config.email.send_list
        user_list = email.split(',')  # 多个邮箱发送，config文件中直接添加  '806029174@qq.com'
        sub = config.project_name + "UI自动化执行异常通知"
        content = f"自动化测试执行完毕，程序中发现异常，请悉知. 报错信息如下: \n{error_message}"
        self.send_mail(user_list, sub, content)

    def send_main(self) -> None:
        """
        功能：发送正常邮件通知
        :return:
        """
        email = config.email.send_list
        user_list = email.split(',')  # 多个邮箱发送，yaml文件中直接添加  '806029174@qq.com'
        sub = config.project_name + "UI自动化报告"
        content = f"""
        各位同事, 大家好:
            UI自动化用例执行完毕，执行结果如下:
            运行总数: {self.metrics.total} 个
            通过数量: {self.metrics.passed} 个
            失败数量: {self.metrics.failed} 个
            异常数量: {self.metrics.broken} 个
            跳过数量: {self.metrics.skipped} 个
            成 功 率: {self.metrics.pass_rate} %

        {self.allure_data.get_failed_cases_detail()}

        **********************************
        jenkins地址：https://121.xx.xx.47:8989/login
        详细情况可登录jenkins平台查看，非相关负责人员可忽略此消息. 谢谢！
        """
        self.send_mail(user_list, sub, content)


if __name__ == '__main__':
    SendEmail(AllureFileClean().get_case_count()).send_main()