#!/usr/bin/env python
# -*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: iRabbit
# Mail: 8381595@qq.com
# Created Time:  2020.10.10
#############################################
from setuptools import setup, find_packages  # 这个包没有的可以pip一下

setup(
    name='iRabbitPro',
    version='36.0.0',
    description='a automated post tools',
    author='iRabbit',
    author_email='8381595@qq.com',
    url='https://github.com/irabbit666/iRabbitPro',
    packages=find_packages(),
    install_requires=['httpx', 'jsonpath', 'pycryptodome']
)
