#!/usr/bin/env python
# -*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: mage
# Mail: mage@woodcol.com
# Created Time: 2018-1-23 19:17:34
#############################################


from setuptools import setup, find_packages
import flasktool
setup(
    name="flasktool",
    version="0.2.2",
    keywords=("pip","flasktool"),
    description="test pip upload",
    long_description="test pip upload",
    license="MIT Licence",

    url="https://github.com/fengmm521/pipProject",
    author="zhangtianming",
    author_email="980152647@qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=['Flask']
)