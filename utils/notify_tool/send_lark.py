#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@ Date        : 2024/11/16 下午6:15
@ Author      : Poco Ray
@ File        : send_lark.py
@ Description : 飞书机器人通知
@ Docs: https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot
"""
import base64
import hashlib
import hmac
import json
import logging
import time
import datetime
import requests
import urllib3
from utils.other_tool.allure_data.allure_report_data import TestMetrics, AllureFileClean
from utils import config
from utils.other_tool.get_local_ip import get_host_ip

urllib3.disable_warnings()

try:
    JSONDecodeError = json.decoder.JSONDecodeError
except AttributeError:
    JSONDecodeError = ValueError


def is_not_null_and_blank_str(content):
    """
    非空字符串
    :param content: 字符串
    :return: 非空 - True，空 - False
    """
    return bool(content and content.strip())


class FeiShuTalkChatBot:
    """飞书机器人通知"""

    def __init__(self, metrics: TestMetrics):
        self.metrics = metrics
        self.timestamp = str(round(time.time()))

    def send_text(self, msg: str):
        """
        消息类型为text类型
        :param msg: 消息内容
        :return: 返回消息发送结果
        """
        data = {"msg_type": "text", "at": {}}
        if is_not_null_and_blank_str(msg):  # 传入msg非空
            data["content"] = {"text": msg}
        else:
            logging.error("text类型，消息内容不能为空！")
            raise ValueError("text类型，消息内容不能为空！")

        logging.debug('text类型：%s', data)
        return self.post()

    def get_sign(self) -> str:
        """ 生成签名 """
        string_to_sign = f"{self.timestamp}\n{config.lark.secret}".encode('utf-8')
        hmac_code = hmac.new(string_to_sign, digestmod=hashlib.sha256).digest()
        sign = base64.b64encode(hmac_code).decode('utf-8')
        return sign

    def post(self):
        """
        发送消息（内容 UTF-8 编码）
        :return: 返回消息发送结果
        """
        sign = self.get_sign()
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        rich_text = {
            # 如果机器人开启签名校验, 需要传入timestamp和sign参数, 否则注释掉即可, 其他的无需变更.
            "timestamp": f"{self.timestamp}",
            "sign": f"{sign}",
            "email": "3157043973@qq.com",
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": f"【{config.project_name}自动化测试结果通知】",
                        "content": [
                            [
                                {"tag": "a", "text": "测试报告请点击这里",
                                 "href": f"http://{get_host_ip()}:53230/index.html#"},
                                {"tag": "at", "user_id": "ou_18eac85d35a26f989317ad4f02e8bbbb", "text": "Tester"}
                            ],
                            [
                                {"tag": "text", "text": "测试人员 : "},
                                {"tag": "text", "text": f"{config.tester_name}"}
                            ],
                            [
                                {"tag": "text", "text": "运行环境 : "},
                                {"tag": "text", "text": f"{config.env} {config.host}"}
                            ],
                            [
                                {"tag": "text", "text": "通过概率 : "},
                                {"tag": "text", "text": f"{self.metrics.pass_rate} %"}
                            ],
                            [
                                {"tag": "text", "text": "总用例数 : "},
                                {"tag": "text", "text": f"{self.metrics.total} %"}
                            ],
                            [
                                {"tag": "text", "text": "成功用例 : "},
                                {"tag": "text", "text": f"{self.metrics.passed}"}
                            ],
                            [
                                {"tag": "text", "text": "失败用例 : "},
                                {"tag": "text", "text": f"{self.metrics.failed}"}
                            ],
                            [
                                {"tag": "text", "text": "异常用例 : "},
                                {"tag": "text", "text": f"{self.metrics.broken}"}
                            ],
                            [
                                {"tag": "text", "text": "跳过用例 : "},
                                {"tag": "text", "text": f"{self.metrics.skipped}"}
                            ],
                            [
                                {"tag": "text", "text": "执行时间 : "},
                                {"tag": "text", "text": f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}
                            ],
                            [
                                {"tag": "img", "image_key": "img_v3_02gn_64679109-13d7-492c-ac1b-2ce763ad093g",
                                 "width": 300,
                                 "height": 300}
                            ]
                        ]
                    }
                }
            }
        }

        post_data = json.dumps(rich_text)
        response = requests.post(config.lark.webhook, headers=headers, data=post_data, verify=False)
        result = response.json()

        if result.get('StatusCode') != 0:
            time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            result_msg = result['errmsg'] if result.get('errmsg', False) else '未知异常'
            error_data = {
                "msgtype": "text",
                "text": {
                    "content": f"[注意-自动通知]飞书机器人消息发送失败，时间：{time_now}，"
                               f"原因：{result_msg}，请及时跟进，谢谢!"
                },
                "at": {
                    "isAtAll": False
                }
            }
            logging.error("消息发送失败，自动通知：%s", error_data)
            requests.post(config.lark.webhook, headers=headers, data=json.dumps(error_data))
        return result


# 测试
if __name__ == '__main__':
    FeiShuTalkChatBot(AllureFileClean().get_case_count()).post()