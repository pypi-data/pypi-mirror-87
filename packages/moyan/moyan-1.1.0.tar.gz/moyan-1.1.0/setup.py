#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from setuptools import setup, find_packages
 
setup(name='moyan',
      version='1.1.0',
      description='moyan private tools',
      author='moyan',
      author_email='ice_moyan@163.com',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
        # 'Twisted>=13.1.0',
        # 'w3lib>=1.17.0',
        # 'queuelib',
        'lxml',
        # 'pyOpenSSL',
        # 'cssselect>=0.9',
        'six>=1.5.2',
        # 'parsel>=1.1',
        # 'PyDispatcher>=2.0.5',
        # 'service_identity',
        # 'opencv-python',
        'numpy',
      ]
)

''''
name/version: 是整个项目的名字，打包后会使用此名字和版本号。
description: 是一个简短的对项目的描述，一般一句话就好，会显示在pypi上名字下端。
long_description: 是一个长的描述，相当于对项目的一个简洁，如果此字符串是rst格式的，PyPI会自动渲染成HTML显示。这里可以直接读取README.rst中的内容。
url: 包的连接，通常为GitHub上的链接或者readthedocs的链接。
packages: 需要包含的子包列表，setuptools提供了find_packages()帮助我们在根路径下寻找包，这个函数distutil是没有的。
          需要处理的包目录（包含__init__.py的文件夹） 
install_requires: 申明依赖包，安装包时pip会自动安装：格式如下（我上面的setup.py没有这个参数，因为我不依赖第三方包
      install_requires=[
        'Twisted>=13.1.0',
        'w3lib>=1.17.0',
        'queuelib',
        'lxml',
        'pyOpenSSL',
        'cssselect>=0.9',
        'six>=1.5.2',
        'parsel>=1.1',
        'PyDispatcher>=2.0.5',
        'service_identity',
    ]
py_modules 需要打包的python文件列表
'''