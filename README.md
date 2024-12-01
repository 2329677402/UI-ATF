# UI-ATF (UI Automation Test Framework)

一个基于 Python 的 UI 自动化测试框架，支持 Web 端和 App 端测试。

## 特性

- 支持 Web 端自动化测试
- 支持 App 端自动化测试
- 支持多种测试数据格式 (CSV, Excel, YAML)
- 支持多种通知方式 (钉钉, 企业微信, 邮件, 飞书)
- 自动管理浏览器驱动
- 生成 Allure 测试报告

## 安装

## 项目文档

### 最近更新
- 新增 ModelParams 数据类，用于规范化模型参数传递
- 改进了模型初始化方式，提高代码可读性

### 使用说明

#### 模型参数传递
使用 ModelParams 数据类来传递模型参数：

#### 定位元素
使用 Locator 数据类来封装定位元素：