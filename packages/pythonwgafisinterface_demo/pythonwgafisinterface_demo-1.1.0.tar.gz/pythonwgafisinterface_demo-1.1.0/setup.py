#!/usr/bin/python
# -*- coding:utf-8 -*-


from setuptools import setup, find_packages

setup(
    name='pythonwgafisinterface_demo',
    version='1.1.0',
    description='just for test',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    install_requires=[],  # install_requires字段可以列出依赖的包信息，用户使用pip或easy_install安装时会自动下载依赖的包
    author='wyx001',
    url='https://pypi.python.com',
    author_email='wyx1505379627@163.com',
    license='MIT',
    packages=find_packages(),  # 需要处理哪里packages，当然也可以手动填，例如['pip_setup', 'pip_setup.ext']
    include_package_data=False,
    zip_safe=True,
)