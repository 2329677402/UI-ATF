#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@ Date        : 2024/11/16 下午6:08
@ Author      : Poco Ray
@ File        : send_ding.py
@ Description : 钉钉机器人通知
@ Docs: https://open.dingtalk.com/document/robots/custom-robot-access
"""
import base64
import hashlib
import hmac
import time
import urllib.parse
from typing import Any, Text
from dingtalkchatbot.chatbot import DingtalkChatbot, FeedLink
from utils.other_tool.get_local_ip import get_host_ip
from utils.other_tool.allure_data.allure_report_data import AllureFileClean, TestMetrics
from utils import config


class DingTalkSendMsg:
    """ 发送钉钉通知 """

    def __init__(self, metrics: TestMetrics):
        """
        :param metrics: 测试用例统计数据
        """
        self.metrics = metrics
        self.timeStamp = str(round(time.time() * 1000))

    def get_sign(self) -> Text:
        """
        根据时间戳 + "sign" 生成密钥
        :return:
        """
        string_to_sign = f'{self.timeStamp}\n{config.ding_talk.secret}'.encode('utf-8')
        hmac_code = hmac.new(config.ding_talk.secret.encode('utf-8'), string_to_sign, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return sign

    def xiao_ding(self):
        sign = self.get_sign()
        # 从yaml文件中获取钉钉配置信息
        webhook = config.ding_talk.webhook + "&timestamp=" + self.timeStamp + "&sign=" + sign
        return DingtalkChatbot(webhook)

    def send_text(self, msg: Text, mobiles=None) -> None:
        """
        发送文本信息
        :param msg: 文本内容
        :param mobiles: @用户电话
        :return:
        """
        if not mobiles:
            self.xiao_ding().send_text(msg=msg, is_at_all=True)
        else:
            if isinstance(mobiles, list):
                self.xiao_ding().send_text(msg=msg, at_mobiles=mobiles)
            else:
                raise TypeError("mobiles类型错误 不是list类型.")

    def send_link(self, title: Text, text: Text, message_url: Text, pic_url: Text) -> None:
        """
        功能: 发送Link通知
        :param title: 链接通知标题
        :param text: 链接通知文本内容
        :param message_url: 链接通知目标URL
        :param pic_url: 链接通知图片URL
        :return: None
        """
        self.xiao_ding().send_link(title=title, text=text, message_url=message_url, pic_url=pic_url)

    def send_markdown(self, title: Text, msg: Text, mobiles=None, is_at_all=False) -> None:
        """
        功能: 发送markdown格式的通知
        :param title: markdown消息的标题
        :param msg: markdown格式的消息内容
        :param mobiles: 艾特用户电话列表, 可选
        :param is_at_all: 是否 @所有人, 可选
        :return: None
        """
        if mobiles is None:
            self.xiao_ding().send_markdown(title=title, text=msg, is_at_all=is_at_all)
        else:
            if isinstance(mobiles, list):
                self.xiao_ding().send_markdown(title=title, text=msg, at_mobiles=mobiles)
            else:
                raise TypeError("mobiles类型错误, 不是list类型.")

    @staticmethod
    def feed_link(title: Text, message_url: Text, pic_url: Text) -> Any:
        """ FeedLink 二次封装 """
        return FeedLink(title=title, message_url=message_url, pic_url=pic_url)

    def send_feed_link(self, *arg) -> None:
        """发送 feed_link """
        self.xiao_ding().send_feed_card(list(arg))

    def send_ding_notification(self):
        """ 发送钉钉报告通知 """
        # 判断如果有失败的用例，@所有人
        is_at_all = False
        if self.metrics.failed + self.metrics.broken > 0:
            is_at_all = True
        text = f"#### {config.project_name}自动化结果通知  " \
               f"\n\n>Python脚本任务: {config.project_name}" \
               f"\n\n>运行环境: {config.env} {config.host}" \
               f"\n\n>测试人员: {config.tester_name}" \
               f"\n\n>通过概率: {self.metrics.pass_rate}% " \
               f"\n\n>总用例数: {self.metrics.total} " \
               f"\n\n>成功用例: {self.metrics.passed}" \
               f"\n\n>失败用例: {self.metrics.failed} " \
               f"\n\n>异常用例: {self.metrics.broken} " \
               f"\n\n>跳过用例: {self.metrics.skipped}" \
               f" ![screenshot](" \
               f"https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png" \
               f")\n" \
               f" > ###### 测试报告 [详情](http://172.25.48.1:53230/) \n"
        # f" > ###### 测试报告 [详情](http://{get_host_ip()}:53230/index.html#) \n"
        DingTalkSendMsg(AllureFileClean().get_case_count()).send_markdown(
            title="【UI自动化通知】", msg=text, is_at_all=is_at_all)


# 测试
if __name__ == '__main__':
    DingTalkSendMsg(AllureFileClean().get_case_count()).send_ding_notification()