#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@ Date        : 2024/11/16 下午3:36
@ Author      : Poco Ray
@ File        : models.py
@ Description : 用于定义一些数据模型
"""
import types
from enum import Enum, unique
from typing import Text, Dict, Callable, Union, Optional, List, Any
from dataclasses import dataclass
from pydantic import BaseModel, Field


class NotificationType(Enum):
    """ 自动化通知方式 """
    DEFAULT = 0  # 不发送通知
    DING_TALK = 1  # 钉钉通知
    WECHAT = 2  # 企业微信通知
    EMAIL = 3  # 邮箱通知
    FEI_SHU = 4  # 飞书通知


@dataclass
class TestMetrics:
    """ 用例指标数据 """
    passed: int  # 成功用例数量
    failed: int  # 失败用例数量
    broken: int  # 异常用例数量
    skipped: int  # 跳过用例数量
    total: int  # 总用例数量
    pass_rate: float  # 通过率
    time: Text  # 执行时间


class RequestType(Enum):
    """ request请求发送，请求参数的数据类型 """
    JSON = "JSON"  # json格式
    PARAMS = "PARAMS"  # params参数
    DATA = "DATA"  # data参数
    FILE = 'FILE'  # file文件
    EXPORT = "EXPORT"  # export导出
    NONE = "NONE"  # 无


def load_module_functions(module) -> Dict[Text, Callable]:
    """
    功能: 获取 module中方法的名称和所在的内存地址
    :param module:
    :return:
    """
    module_functions = {}

    for name, item in vars(module).items():
        if isinstance(item, types.FunctionType):
            module_functions[name] = item
    return module_functions


@unique
class DependentType(Enum):
    """ 数据依赖相关枚举 """
    RESPONSE = 'response'  # response响应数据
    REQUEST = 'request'  # request请求数据
    SQL_DATA = 'sqlData'  # sql数据
    CACHE = "cache"  # 缓存数据(用于接口关联的依赖数据, 相当于Apifox中的提取变量)


class Assert(BaseModel):
    """ 断言数据 """
    jsonpath: Text  # jsonpath路径
    type: Text  # 断言类型
    value: Any  # 断言值
    AssertType: Union[None, Text] = None  # 断言类型


class DependentData(BaseModel):
    """ 依赖数据 """
    dependent_type: Text  # 依赖类型
    jsonpath: Text  # jsonpath路径
    set_cache: Optional[Text]  # 设置缓存
    replace_key: Optional[Text]  # 替换key


class DependentCaseData(BaseModel):
    """ 依赖用例数据 """
    case_id: Text  # 用例id
    # dependent_data: List[DependentData]
    dependent_data: Union[None, List[DependentData]] = None  # 依赖数据


class ParamPrepare(BaseModel):
    """ 参数准备 """
    dependent_type: Text  # 依赖类型
    jsonpath: Text  # jsonpath路径
    set_cache: Text  # 设置缓存


class SendRequest(BaseModel):
    """ 发送请求 """
    dependent_type: Text  # 依赖类型
    jsonpath: Optional[Text]  # jsonpath路径
    cache_data: Optional[Text]  # 缓存数据
    set_cache: Optional[Text]  # 设置缓存
    replace_key: Optional[Text]  # 替换key


class TearDown(BaseModel):
    """ 用例后置处理 """
    case_id: Text  # 用例id
    param_prepare: Optional[List["ParamPrepare"]]  # 参数准备
    send_request: Optional[List["SendRequest"]]  # 发送请求


class CurrentRequestSetCache(BaseModel):
    """ 当前请求设置缓存 """
    type: Text  # 类型
    jsonpath: Text  # jsonpath路径
    name: Text  # 变量名称


class TestCase(BaseModel):
    """ 测试用例数据 """
    url: Text  # 请求url
    method: Text  # 请求方法
    detail: Text  # 用例描述
    # assert_data: Union[Dict, Text] = Field(..., alias="assert")
    assert_data: Union[Dict, Text]  # 断言数据
    headers: Union[None, Dict, Text] = {}  # 请求头
    requestType: Text  # 请求类型
    is_run: Union[None, bool, Text] = None  # 是否运行
    data: Any = None  # 请求数据
    dependence_case: Union[None, bool] = False  # 是否依赖用例
    dependence_case_data: Optional[Union[None, List["DependentCaseData"], Text]] = None  # 依赖用例数据
    sql: List = None  # sql数据
    setup_sql: List = None  # 设置sql
    status_code: Optional[int] = None  # 状态码
    teardown_sql: Optional[List]  # 后置sql
    teardown: Union[List["TearDown"], None] = None  # 后置处理
    current_request_set_cache: Optional[List["CurrentRequestSetCache"]]  # 当前请求设置缓存(环境变量)
    sleep: Optional[Union[int, float]]  # 等待时间


class ResponseData(BaseModel):
    """ 响应数据 """
    url: Text  # 请求url
    is_run: Union[None, bool, Text] = None  # 是否运行
    detail: Text  # 用例描述
    response_data: Text  # 响应数据
    request_body: Any  # 请求数据
    method: Text  # 请求方法
    sql_data: Dict  # sql数据
    yaml_data: "TestCase"  # 测试用例数据
    headers: Dict  # 请求头
    cookie: Dict  # cookie数据
    assert_data: Dict  # 断言数据
    res_time: Union[int, float]  # 响应时间
    status_code: int  # 状态码
    teardown: List["TearDown"] = None  # 后置处理
    teardown_sql: Union[None, List]  # 后置sql
    body: Any  # 请求体


class DingTalk(BaseModel):
    """ 钉钉通知 """
    webhook: Union[Text, None]  # 钉钉webhook地址
    secret: Union[Text, None]  # 钉钉secret加签密钥

class Lark(BaseModel):
    """ 飞书通知 """
    webhook: Union[Text, None]  # 飞书webhook地址
    secret: Union[Text, None]  # 飞书secret加签密钥


class MySqlDB(BaseModel):
    """ mysql数据库 """
    switch: bool = False  # 是否开启
    host: Union[Text, None] = None  # IP地址
    user: Union[Text, None] = None  # 用户名
    password: Union[Text, None] = None  # 密码
    port: Union[int, None] = 3306  # 端口


class Webhook(BaseModel):
    """ webhook地址 """
    webhook: Union[Text, None]  # webhook地址


class Email(BaseModel):
    """ 邮箱通知 """
    send_user: Union[Text, None]  # 发送人邮箱
    email_host: Union[Text, None]  # 邮箱服务器地址
    stamp_key: Union[Text, None]  # 邮箱授权码
    send_list: Union[Text, None]  # 收件人邮箱


class Config(BaseModel):
    """ 配置信息 """
    project_name: Text
    env: Text
    tester_name: Text
    notification_type: int = 0
    ding_talk: "DingTalk"
    mysql_db: "MySqlDB"
    mirror_source: Text
    wechat: "Webhook"
    email: "Email"
    lark: "Lark"
    host: Text
    app_host: Union[Text, None]
    browser: Text


@unique
class AllureAttachmentType(Enum):
    """ allure 报告的文件类型枚举 """
    TEXT = "txt"
    CSV = "csv"
    TSV = "tsv"
    URI_LIST = "uri"

    HTML = "html"
    XML = "xml"
    JSON = "json"
    YAML = "yaml"
    PCAP = "pcap"

    PNG = "png"
    JPG = "jpg"
    SVG = "svg"
    GIF = "gif"
    BMP = "bmp"
    TIFF = "tiff"

    MP4 = "mp4"
    OGG = "ogg"
    WEBM = "webm"

    PDF = "pdf"


@unique
class AssertMethod(Enum):
    """ 断言类型 """
    equals = "=="  # 等于
    less_than = "lt"  # 小于
    less_than_or_equals = "le"  # 小于等于
    greater_than = "gt"  # 大于
    greater_than_or_equals = "ge"  # 大于等于
    not_equals = "not_eq"  # 不等于
    string_equals = "str_eq"  # 字符串相等
    length_equals = "len_eq"  # 长度相等
    length_greater_than = "len_gt"  # 长度大于
    length_greater_than_or_equals = 'len_ge'  # 长度大于等于
    length_less_than = "len_lt"  # 长度小于
    length_less_than_or_equals = 'len_le'  # 长度小于等于
    contains = "contains"  # 包含
    contained_by = 'contained_by'  # 被包含
    startswith = 'startswith'  # 以什么开头
    endswith = 'endswith'  # 以什么结尾
