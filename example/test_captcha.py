#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@ Date        : 2024/12/5 上午11:49
@ Author      : Administrator
@ File        : test_captcha.py
@ Description : 验证码处理示例
"""
from tests.test_base_case import BaseCaseWeb


class TestExample(BaseCaseWeb):
    """示例测试类"""

    def test_click_captcha(self):
        """测试文本验证码"""
        self.open("https://captcha.ruijie.com.cn/")
        img_el = self.find_element("img")
        image_path = self.download_image(img_el, "captcha.png")
        print(image_path)
