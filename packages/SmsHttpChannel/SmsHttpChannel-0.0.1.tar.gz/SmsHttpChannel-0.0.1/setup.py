#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools
with open("README.md", "r",encoding='utf-8') as fh:
    long_description = fh.read()
setuptools.setup(
    name="SmsHttpChannel",
    version="0.0.1",
    author="suk",
    author_email="277667028@qq.com",
    description="Python异步提交短信的模块",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),  # 自动找到项目中导入的模块
    # 模块相关的元数据
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 依赖模块
    install_requires=[
        'tornado==6.1',
    ],
    python_requires='>=3',
)