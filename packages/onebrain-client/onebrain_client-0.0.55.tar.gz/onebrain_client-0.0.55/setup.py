#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/14 15:41
# @Author  : like
# @Site    :
# @File    : setup.py
# @Software: PyCharm
# @Description:

import setuptools


setuptools.setup(
    name = "onebrain_client",
    version = "0.0.55",
    author = "KeLi",
    description = "onebrain客户端",
    packages = setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # basic stuff here
    scripts = [
        'onebrain-client'
    ],
    install_requires=[
        'click',
        'requests',
        'lxml',
        'pyyaml',
        'requests_toolbelt',
    ]

)