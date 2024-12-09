#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@ Date        : 2024/12/5 上午11:49
@ Author      : Administrator
@ File        : test_captcha.py
@ Description : 验证码处理示例
"""
from tests.test_base_case import BaseCaseWeb
from utils.captcha_tool.text_captcha import TextCaptcha
from common.setting import ensure_path_sep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyautogui


class TestExample(BaseCaseWeb):
    """示例测试类"""

    def test_click_captcha(self):
        """测试文本验证码"""
        # 打开验证码页面
        self.open("https://captcha.ruijie.com.cn/")
        img_el = self.find_element("img")
        self.sleep(0.5)

        # 下载验证码图片
        captcha_path = self.download_image(img_el, "captcha1.png")
        print(f"验证码图片保存路径: {captcha_path}")

        # 获取验证码文本要求
        text_captcha = self.find_element("span.verify-msg").text
        print(f"验证码文本要求: {text_captcha}")

        # 初始化验证码处理工具
        captcha_tool = TextCaptcha()

        try:
            # 识别图片中的文字和位置
            text_positions = captcha_tool.recognize_text(captcha_path)
            print(f"识别到的文字和位置: {text_positions}")

            # 解析需要点击的文字序列
            text_sequence = captcha_tool.parse_captcha_text(text_captcha)
            print(f"需要点击的文字序列: {text_sequence}")
            width, height = self.get_window_size().values()

            # 点击文字
            # captcha_tool.click_text_positions(text_positions, text_sequence)
            self.click(pos=(50, 380))
            # 截图记录结果
            self.sleep(0.5)
            img_path = self.take_screenshot("在线体验")
            print(f"结果截图保存路径: {img_path}")

        except Exception as e:
            print(f"验证码处理失败: {str(e)}")
            self.take_screenshot("验证码处理失败")
            raise
