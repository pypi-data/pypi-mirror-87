# -*- coding:utf-8 -*-
"""
作者：jiangshuo
日期：2020年12月01日
"""


from setuptools import find_packages, setup
setup(
    name='grant',  # 包名
    python_requires='>=3.4.0',  # python环境
    version='1.0.1',  # 包的版本
    description="Test publish own pypi.",  # 包简介，显示在PyPI上
    long_description_content_type="text/markdown",  # 指定包文档格式为markdown
    author="jiangshuo",  # 作者相关信息
    author_email='jiangshuo-ghq@sinosig.com',
    # 指定包信息，还可以用find_packages()函数
    packages=find_packages(),
    # package_data = {
    #     'parser_code': ['metadata/shared/*.json']
    # },#读取需要的数据文件
    install_requires=[
        'cx_Oracle',
    ],  # 指定需要安装的依赖
    include_package_data=True,
    license="MIT",
    keywords=['jiangshuo6'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Utilities'
    ],
)
