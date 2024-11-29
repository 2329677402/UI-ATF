#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@ Date        : 2024/11/2 下午6:00
@ Author      : Poco Ray
@ File        : read_file.py
@ Description : 读取各种文件工具类
"""
import os, yaml
import pandas as pd
from typing import Union
from faker import Faker

fake = Faker('zh_CN')  # 生成虚拟数据


class ExcelReader:
    """
    功能: 读取Excel文件数据
    使用:
        excel_reader = ExcelReader(file_path='../data/case_xlsx/test_web.xlsx', sheet_name='Sheet1', header=True)
        data = excel_reader.read_excel()[0].get("邮箱")
        print(data)  # dongdong@qq.com
    """

    def __init__(self, file_path: str, sheet_name: str = "Sheet1", header: bool = True):
        """
        :param file_path: Excel文件路径.
        :param sheet_name: sheet工作表名称(字符串或索引)，默认为第一个sheet.
        :param header: 表头行, True:包含, False:不包含.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")

        self.file_path = file_path
        self.sheet_name = sheet_name
        self.header = 0 if header else None
        self._data = None

    def read_excel(self):
        """
        功能: 读取excel数据
        :return: 将Excel数据转换为字典列表
        """
        if self._data is None:
            self._data = pd.read_excel(self.file_path, sheet_name=self.sheet_name, header=self.header)
            if self.header is None:
                self._data.columns = [f"Column{i}" for i in range(1, len(self._data.columns) + 1)]
        return self._data.to_dict(orient='records')


class CSVReader:
    """
    功能: 读取CSV文件数据
    使用:
        csv_reader = CSVReader(file_path='../data/case_csv/test_web.csv', header=True)
        data = csv_reader.read_csv()[0].get("邮箱")
        print(data)  # test1@example.com
    """

    def __init__(self, file_path: str, header: bool = True):
        """
        :param file_path: CSV文件路径.
        :param header: 表头行, True:包含, False:不包含.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")

        self.file_path = file_path
        self.header = 0 if header else None
        self._data = None

    def read_csv(self):
        """
        功能: 读取CSV数据
        :return: 将CSV数据转换为字典列表
        """
        if self._data is None:
            self._data = pd.read_csv(self.file_path, header=self.header)
            if self.header is None:
                self._data.columns = [f"Column{i}" for i in range(1, len(self._data.columns) + 1)]
        return self._data.to_dict(orient='records')


class YamlReader:
    """
    功能: Yaml文件读取
    使用:
        yaml_reader = YamlReader(file_path='../data/locator/loc_web.yaml')
        data = yaml_reader.read_yaml("common_page").get("home_model")
        print(data)  # span:contains('首页')
    """

    def __init__(self, file_path: str):
        """
         :param file_path: Yaml文件路径.
         """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件路径不存在: {file_path}")

        self.file_path = file_path

    def read_yaml(self, key: str = None) -> Union[dict, list, str]:
        """
        功能: 读取yaml文件
        :param key: yaml文件中的键, 可选
        :return: yaml文件数据
        """
        with open(self.file_path, encoding='utf-8') as f:
            _data = yaml.load(f, Loader=yaml.FullLoader)  # yaml.FullLoader: 用于加载yaml文件内容
            if key:
                for item in _data:
                    if item.get(key) is not None:
                        return item.get(key)
            else:
                return _data

    def write_yaml(self, key: str, value) -> int:
        """
        功能: 更改yaml文件中的值, 并且保留注释内容.
        :param key: 字典的key
        :param value: 写入的值
        :return: 成功写入返回1, 否则返回0
        """
        with open(self.file_path, 'r', encoding='utf-8') as file:
            lines = [line for line in file.readlines() if line.strip()]

        flag = 0  # 写入失败
        with open(self.file_path, 'w', encoding='utf-8') as file:
            for line in lines:
                left_str = line.split(":")[0].strip()
                if key == left_str and '#' not in line:
                    line = f"{left_str}: {value}\n"
                    flag = 1  # 写入成功
                file.write(line)
        return flag


class RandomDataGenerator:
    """
    功能: 基于 faker库 随机测试数据
    使用:
        generator = RandomDataGenerator()
        data = generator.random_name
        print(data)  # 随机姓名: 张三
    """

    @property
    def random_name(self):
        """随机中文姓名, 格式: 蔡徐坤"""
        return fake.name()

    @property
    def random_phone(self):
        """随机手机号, 格式: 18766895523"""
        return fake.phone_number()

    @property
    def random_email(self):
        """随机邮箱, 格式: taopan@example.com"""
        return fake.email()

    @property
    def random_job(self):
        """随机职业, 格式: 质量管理/测试工程师(QA/QC工程师)"""
        return fake.job()

    @property
    def random_ssn(self):
        """随机中国居民证身份证号, 格式: 340406193710180483"""
        return fake.ssn()

    @property
    def random_company(self):
        """随机公司, 格式: 深圳市华为技术有限公司"""
        return fake.company()

    @property
    def random_city(self):
        """随机城市, 格式: 北京市"""
        return fake.city_name()

    @property
    def random_province(self):
        """随机省份, 格式: 浙江省"""
        return fake.province()

    @property
    def random_country(self):
        """随机国家, 格式: 中国"""
        return fake.country()

    @property
    def random_address(self):
        """随机地址+邮编, 格式: 江西省长沙市孝南罗路x座 806153"""
        return fake.address()

    @property
    def random_time(self):
        """随机时间, 格式: 18:00:00"""
        return fake.time()

    @property
    def random_year(self):
        """随机年份, 格式: 2024"""
        return fake.year()

    @property
    def random_month(self):
        """随机月份, 格式: 11"""
        return fake.month()

    @property
    def random_current_month(self):
        """随机生成当前月份内的日期, 格式: 2024-11-02 18:00:00"""
        return fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None)

    @property
    def random_current_year(self):
        """随机生成当前年份内的日期, 格式: 2024-11-02 18:00:00"""
        return fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)

    @property
    def random_current_century(self):
        """随机生成当前世纪内的日期, 格式: 2000-04-12 18:34:11"""
        return fake.date_time_this_century(before_now=True, after_now=False, tzinfo=None)

    @property
    def random_week(self):
        """随机周, 格式: 星期一"""
        return fake.day_of_week()

    @staticmethod
    def random_birth(age):
        """
        功能: 随机生成生日, 格式: 2002-11-02
        :param age: 年份
        :return: 生日在 [当前年份-age, 当前日期] 之间, 如当前日期为2024-10-01,将age设置为1,则随机数据在 [2023-01-01, 2024-10-01] 之间
        """
        return fake.date_of_birth(tzinfo=None, minimum_age=0, maximum_age=age)


# 测试功能是否正常
if __name__ == '__main__':
    # 验证RandomDataGenerator功能
    generator = RandomDataGenerator()
    data = generator.random_name
    print(data)  # 随机姓名: 张三

    # 验证ExcelReader功能
    excel_reader = ExcelReader(file_path='../../data/case_xlsx/test_web.xlsx', sheet_name='Sheet1', header=True)
    data = excel_reader.read_excel()[0].get("邮箱")
    print(data)  # dongdong@qq.com

    # 验证CSVReader功能
    csv_reader = CSVReader(file_path='../../data/case_csv/test_web.csv', header=True)
    data = csv_reader.read_csv()[0].get("邮箱")
    print(data)  # test1@example.com

    # 验证YamlReader功能
    yaml_reader = YamlReader(file_path='../../data/locator/loc_web.yaml')
    data = yaml_reader.read_yaml("common_page").get("home_model")
    print(data)  # span:contains('首页')
