#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@ Date        : 12/10/2024 5:45 PM
@ Author      : Administrator
@ File        : custom_webelement.py
@ Description :
"""
import warnings
from selenium.webdriver.remote.webelement import WebElement


class CustomWebElement(WebElement):
    def screenshot(self, filename):
        """
        截图元素
        :param filename: 文件名
        """
        print("Starting screenshot process...")

        if not filename.lower().endswith(".png"):
            warnings.warn(
                "name used for saved screenshot does not match file type. It should end with a `.png` extension",
                UserWarning,
            )
        png = self.screenshot_as_png
        try:
            with open(filename, "wb") as f:
                f.write(png)
        except OSError:
            return False
        finally:
            del png

        # Additional processing logic after taking the screenshot
        print("Screenshot process completed.")
        return True
