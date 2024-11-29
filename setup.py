from setuptools import setup, find_packages

setup(
    name="ui-atf",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        'pytest',
        'selenium',
        'webdriver_manager',
        'Appium-Python-Client'
    ],
) 