#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@ Date        : 2024/12/5 上午10:23
@ Author      : Administrator
@ File        : text_captcha.py
@ Description : 文本验证码, 处理包含扭曲、模糊、叠加背景或噪点的文字.
@ Solution    : 1. 图像处理与OCR（光学字符识别）: 使用高级的OCR技术，可以识别一些扭曲的文字. 不过，现代的验证码往往会使用更复杂的变形，使OCR变得困难.
                    技术栈：Python + OpenCV + paddleocr + PaddlePaddle.

                2. 机器学习与深度学习: 训练模型来识别特定类型验证码的模式.
                    技术栈：Python + TensorFlow/Keras/PyTorch + Convolutional Neural Networks (CNNs).

                3. 人工智能服务: 深度学习算法可以学习识别这些图形，即使是高度变形的文本.
                    技术栈：云端 AI 服务（如 Google Cloud Vision API, Amazon Rekognition, Microsoft Azure Computer Vision）

                4. 手动输入或人机交互: 使用自动化工具截取验证码图片并显示给用户, 用户手动输入识别结果，程序继续执行.
                    技术栈：Python + pyautogui.
"""
import cv2
import numpy as np
from paddleocr import PaddleOCR
import pyautogui
import time
import re
import os
from typing import List, Tuple
from common.setting import ensure_path_sep


class TextCaptcha:
    """文本验证码处理工具"""

    def __init__(self):
        """初始化OCR引擎"""
        self.ocr = PaddleOCR(
            use_angle_cls=True,
            lang='ch',
            show_log=True,  # 日志信息
            det_db_thresh=0.3,  # 降低检测阈值
            det_db_box_thresh=0.3,  # 降低框检测阈值
            det_db_unclip_ratio=1.6  # 调整文本框扩张比例
        )

    def recognize_text(self, image_path: str) -> List[Tuple[str, Tuple[int, int]]]:
        """
        优化的文字识别函数

        :param image_path: 图像路径
        :return: 文字和位置信息列表，如：[('送', (100, 200)), ('公', (200, 300)), ('赶', (300, 400))]
        """
        try:
            # 读取图像
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"无法读取图片: {image_path}")

            # 图像预处理
            processed_image = self._preprocess_image(image)

            # 保存预处理后的图像用于调试
            debug_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'datas', 'debug')
            os.makedirs(debug_dir, exist_ok=True)
            processed_path = os.path.join(debug_dir, 'processed.png')
            cv2.imwrite(processed_path, processed_image)

            # OCR识别，使用简化的参数
            result = self.ocr.ocr(
                processed_path,
                cls=True,
                det=True,
                rec=True
            )

            if not result or not result[0]:
                # 如果识别失败，尝试使用原始图像
                result = self.ocr.ocr(
                    image_path,
                    cls=True,
                    det=True,
                    rec=True
                )

            if not result or not result[0]:
                return []

            # 提取文字和位置信息
            text_positions = []
            for line in result[0]:
                if not line:
                    continue

                box = line[0]
                text = line[1][0]
                confidence = float(line[1][1])

                if confidence < 0.3:  # 降低置信度阈值
                    continue

                # 计算中心点
                center_x = int((box[0][0] + box[2][0]) / 2)
                center_y = int((box[0][1] + box[2][1]) / 2)

                # 对单个汉字进行处理
                if len(text) == 1 and '\u4e00' <= text <= '\u9fff':
                    text_positions.append((text, (center_x, center_y)))

                # 处理多字符文本
                elif len(text) > 1:
                    char_width = (box[2][0] - box[0][0]) / len(text)
                    for i, char in enumerate(text):
                        if '\u4e00' <= char <= '\u9fff':
                            char_x = int(box[0][0] + char_width * (i + 0.5))
                            char_y = center_y
                            text_positions.append((char, (char_x, char_y)))

            return text_positions

        except Exception as e:
            print(f"识别文字失败: {str(e)}")
            return []


    def _preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        优化的图像预处理，专门处理彩色文字验证码
        """
        try:
            # 调整图像大小以提高清晰度
            height, width = image.shape[:2]
            scale = 3.0  # 进一步增加放大比例
            image = cv2.resize(image, (int(width * scale), int(height * scale)))
            
            # 转换到HSV空间以更好地处理彩色
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # 创建多个颜色掩码，针对性调整每种颜色的范围
            masks = []
            
            # 褐色范围（针对"叫"字）
            lower_brown = np.array([10, 40, 40])
            upper_brown = np.array([20, 255, 200])
            masks.append(cv2.inRange(hsv, lower_brown, upper_brown))
            
            # 青色范围（针对"眼"字）
            lower_cyan = np.array([80, 40, 40])
            upper_cyan = np.array([100, 255, 255])
            masks.append(cv2.inRange(hsv, lower_cyan, upper_cyan))
            
            # 绿色范围（针对"知"字）
            lower_green = np.array([35, 40, 40])
            upper_green = np.array([75, 255, 255])
            masks.append(cv2.inRange(hsv, lower_green, upper_green))
            
            # 紫色范围（针对"神"字）
            lower_purple = np.array([130, 40, 40])
            upper_purple = np.array([170, 255, 255])
            masks.append(cv2.inRange(hsv, lower_purple, upper_purple))
            
            # 白色范围（可选，用于识别白色文字）
            lower_white = np.array([0, 0, 200])
            upper_white = np.array([180, 30, 255])
            masks.append(cv2.inRange(hsv, lower_white, upper_white))

            # 合并所有颜色掩码
            final_mask = np.zeros_like(masks[0])
            for mask in masks:
                final_mask = cv2.bitwise_or(final_mask, mask)
            
            # 应用掩码到原始图像
            result = cv2.bitwise_and(image, image, mask=final_mask)
            
            # 转换为灰度图并增强对比度
            gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
            clahe = cv2.createCLAHE(clipLimit=3.5, tileGridSize=(4,4))  # 调整对比度参数
            enhanced = clahe.apply(gray)
            
            # 使用Otsu's二值化方法
            _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # 降噪处理
            binary = cv2.medianBlur(binary, 3)
            
            # 形态学操作改进
            kernel = np.ones((2,2), np.uint8)
            binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=1)
            binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)
            
            # 保存调试图像
            debug_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'datas', 'debug')
            os.makedirs(debug_dir, exist_ok=True)
            
            cv2.imwrite(os.path.join(debug_dir, 'debug_original.png'), image)
            cv2.imwrite(os.path.join(debug_dir, 'debug_mask.png'), final_mask)
            cv2.imwrite(os.path.join(debug_dir, 'debug_result.png'), result)
            cv2.imwrite(os.path.join(debug_dir, 'debug_binary.png'), binary)
            
            return binary
            
        except Exception as e:
            print(f"图像预处理失败: {str(e)}")
            return image

    @staticmethod
    def parse_captcha_text(text: str) -> List[str]:
        """
        解析验证码文本要求，提取需要点击的文字序列
        
        :param text: 验证码文本要求，如："请依次点击【送,公,赶】"
        :return: 需要点击的文字列表，如：['送', '公', '赶']
        """
        pattern = r'【(.*?)】'
        match = re.search(pattern, text)
        if not match:
            raise ValueError("未找到需要点击的文字序列")
        return match.group(1).split(',')

    @staticmethod
    def click_text_positions(text_positions: List[Tuple[str, Tuple[int, int]]],
                             text_sequence: List[str], delay: float = 0.5) -> None:
        """
        按顺序点击指定文字位置
        
        :param text_positions: 文字位置列表
        :param text_sequence: 需要点击的文字序列
        :param delay: 点击间隔时间(秒)
        """
        # 创建文字到位置的映射
        text_map = {text: pos for text, pos in text_positions}

        # 按序列依次点击
        for text in text_sequence:
            if text in text_map:
                x, y = text_map[text]
                pyautogui.moveTo(x, y, duration=0.5)
                pyautogui.click()
                time.sleep(delay)
            else:
                print(f"警告: 未找到文字 {text}")


if __name__ == '__main__':
    captcha_tool = TextCaptcha()
    img_path = ensure_path_sep("\\datas\\downloads\\img.png")
    print(f"处理图片: {img_path}")
    text_positions = captcha_tool.recognize_text(image_path=img_path)
    print(f"识别结果: {text_positions}")
