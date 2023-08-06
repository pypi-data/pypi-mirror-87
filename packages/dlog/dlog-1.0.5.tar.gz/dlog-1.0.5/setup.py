# coding:utf-8
# author caturbhuja
# date   2020/9/4 11:00 上午
# wechat chending2012
import os
import pypandoc

from setuptools import setup, find_packages

import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def long_description(filename="./dlog/README.md"):
    if os.path.isfile(os.path.expandvars(filename)):
        ld = pypandoc.convert_file(filename, "rst")
    else:
        ld = ""
    return ld


long_description = long_description("Readme.md")

setup(
    name='dlog',
    version='1.0.5',
    description='Easy log',
    long_description=long_description,
    packages=find_packages(),
    author='Caturbhuja',
    author_email='caturbhuja@foxmail.com',
    url='',
    install_requires=[
        'concurrent-log-handler==0.9.19',
        'portalocker==2.0.0',
    ],
    license='MIT'
)

# os.system('rm -rf README.rst')
