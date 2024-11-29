#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@ Date        : 2024/11/16 下午6:17
@ Author      : Poco Ray
@ File        : exceptions.py
@ Description : 自定义异常
"""


class MyBaseFailure(Exception):
    pass


class JsonpathExtractionFailed(MyBaseFailure):
    pass


class NotFoundError(MyBaseFailure):
    pass


class FileNotFound(FileNotFoundError, NotFoundError):
    pass


class SqlNotFound(NotFoundError):
    pass


class AssertTypeError(MyBaseFailure):
    pass


class DataAcquisitionFailed(MyBaseFailure):
    pass


class ValueTypeError(MyBaseFailure):
    pass


class SendMessageError(MyBaseFailure):
    pass


class ValueNotFoundError(MyBaseFailure):
    pass
