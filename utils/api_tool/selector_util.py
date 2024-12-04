#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@ Date        : 2024/12/2 下午9:42
@ Author      : Poco Ray
@ File        : selector_util.py
@ Description : 选择器工具类，用于处理和转换各种类型的选择器
"""
import re
from typing import Tuple
from selenium.webdriver.common.by import By


class SelectorUtil:
    """选择器工具类"""

    # 支持的定位方式映射
    LOCATOR_MAP = {
        'id': By.ID,
        'name': By.NAME,
        'css_selector': By.CSS_SELECTOR,
        'xpath': By.XPATH,
        'link': By.LINK_TEXT,
        'partial_link': By.PARTIAL_LINK_TEXT,
        'tag': By.TAG_NAME,
        'class': By.CLASS_NAME
    }

    @staticmethod
    def is_valid_by(by: str) -> bool:
        """
        检查定位方式是否有效
        :param by: 定位方式
        :return: 是否有效
        """
        valid_by = [
            'css_selector', 'id', 'name', 'xpath',
            'link', 'partial_link', 'tag', 'class'
        ]
        return by.lower() in valid_by

    @staticmethod
    def is_xpath_selector(selector: str) -> bool:
        """
        判断是否为XPath选择器
        :param selector: 选择器字符串
        :return: 是否为XPath
        """
        return selector.strip().startswith(('/', './/', '('))

    @staticmethod
    def process_contains_selector(selector: str) -> Tuple[str, str]:
        """
        处理包含:contains()的选择器
        :param selector: CSS选择器
        :return: (选择器, 定位方式)的元组
        """
        # 匹配:contains('文本')或:contains("文本")模式
        contains_pattern = r':contains\([\'\"](.*?)[\'\"]\)'
        if ':contains(' in selector:
            text = re.search(contains_pattern, selector).group(1)
            base_selector = re.sub(contains_pattern, '', selector).strip()

            # 转换为XPath表达式，使用更灵活的文本匹配方式
            if base_selector:
                # 如果有基础选择器，使用normalize-space()处理文本
                xpath = (
                    f"//{base_selector}["
                    f"contains(normalize-space(.), '{text}') or "
                    f"contains(normalize-space(text()), '{text}') or "
                    f".//text()[contains(normalize-space(.), '{text}')] or "
                    f"@*[contains(normalize-space(.), '{text}')]"
                    f"]"
                )
            else:
                # 如果没有基础选择器，搜索所有元素
                xpath = (
                    f"//*["
                    f"contains(normalize-space(.), '{text}') or "
                    f"contains(normalize-space(text()), '{text}') or "
                    f".//text()[contains(normalize-space(.), '{text}')] or "
                    f"@*[contains(normalize-space(.), '{text}')]"
                    f"]"
                )
            return xpath, 'xpath'

        return selector, 'css_selector'

    @classmethod
    def get_selenium_locator(cls, selector: str, by: str = 'css_selector') -> Tuple[str, str]:
        """
        获取Selenium支持的定位器
        :param selector: 选择器字符串
        :param by: 定位方式
        :return: (定位方式, 选择器)元组
        """
        by = by.lower()

        # 检查定位方式是否有效
        if not cls.is_valid_by(by):
            raise ValueError(f"不支持的定位方式: {by}")

        # 处理XPath选择器
        if cls.is_xpath_selector(selector):
            return By.XPATH, selector

        # 处理:contains()选择器
        if by == 'css_selector' and ':contains(' in selector:
            selector, by = cls.process_contains_selector(selector)
            return By.XPATH, selector

        # 返回标准定位器
        return cls.LOCATOR_MAP[by], selector
