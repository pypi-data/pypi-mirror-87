# -*- coding: utf-8 -*-

# @Date    : 2020-12-03
# @Author  : Changjiale
# @Site    : https://www.05dt.com

from setuptools import setup, find_packages
import io
import os

with io.open("requirements.txt", 'r') as f:
    install_requires = f.read().split(os.sep)

with io.open("README.md", 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    # 以下为必需参数
    name='dtadmin',  # 模块名
    version='0.0.3',  # 当前版本
    description='DTAdmin - a crawler and data visualization management system based on flash framework.',  # 简短描述
    # py_modules=["my_module"],  # 单文件模块写法
    # ckages=find_packages(exclude=['contrib', 'docs', 'tests']),  # 多文件模块写法
    ckages=find_packages(),

    # 以下均为可选参数
    long_description=long_description,  # 长描述
    long_description_content_type='text/markdown',
    url='https://www.05dt.com',  # 主页链接
    author='Changjiale',  # 作者名
    author_email='836333583@qq.com',  # 作者邮箱
    classifiers=[
        'Development Status :: 1 - Planning',   # 当前开发进度等级（测试版，正式版等）

        'Intended Audience :: Developers',   # 模块适用人群
        'Topic :: Software Development',  # 给模块加话题标签

        'License :: OSI Approved :: MIT License',  # 模块的license

        'Programming Language :: Python :: 3.6',  # 模块支持的Python版本
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='crawler',  # 模块的关键词，使用空格分割
    install_requires=install_requires,  # 依赖模块
    package_data={  # 模块所需的额外文件
        'sample': ['package_data.dat'],
    },
    entry_points={  # 新建终端命令并链接到模块函数
        'console_scripts': [
            'dtadmin=dtadmin:main',
        ],
    },
)
"""
一、打包上传
1、先升级打包工具
pip3 install --upgrade setuptools wheel twine

2、打包
python3 setup.py sdist bdist_wheel

3、检查
twine check dist/*

4、上传pypi (https://pypi.org/manage/projects/)
twine upload dist/*

5、命令整合
rm -rf dist build *.egg-info && python3 setup.py sdist bdist_wheel && twine check dist/* && twine upload dist/*

"""

