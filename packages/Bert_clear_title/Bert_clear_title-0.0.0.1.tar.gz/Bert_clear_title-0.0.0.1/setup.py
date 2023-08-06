# -*- coding: utf-8 -*-
from setuptools import find_packages, setup
from os import path as os_path
import time
this_directory = os_path.abspath(os_path.dirname(__file__))

# 读取文件内容
def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description

# 获取依赖
def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]
# long_description="""

# 这里是说明
# 一个借助Bert提取标记的包，这里主要做标题清理
# http://terrychan.org/Bert_clear_title
# """

long_description=read_file("README.md")
setup(
    name='Bert_clear_title', #修改包名字
    version='0.0.0.1',
    description='Terry toolkit Bert_clear_title',
    author='Terry Chan',
    author_email='napoler2008@gmail.com',
    url='http://terrychan.org/Bert_clear_title/',
    # install_requires=read_requirements('requirements.txt'),  # 指定需要安装的依赖
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'regex==2020.2.20',
        'numpy==1.19.4',
        'transformers==2.8.0',
        'torch==1.7.0',
        'tqdm==4.38.0'

    ],
    packages=['Bert_clear_title'])

"""
pip freeze > requirements.txt

python3 setup.py sdist
#python3 setup.py install
python3 setup.py sdist upload
"""