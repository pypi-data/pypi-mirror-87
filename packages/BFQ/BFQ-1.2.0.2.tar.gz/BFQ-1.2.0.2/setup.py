#!/usr/bin/env python
#coding: utf-8

from setuptools import setup

setup(
    name='BFQ',
    python_requires='>=3.7.0',
    version='1.2.0.2',
    author='Billy',
    author_email='ztqstd@163.com',
    url='https://zhengtq.github.io/',
    description=u'博采众长的人脸质量评价库',
    packages=['BFQ'],
    license='MIT',
    install_requires=[
        'numpy'
        ],
    package_data={  # Optional
                    'BFQ': ['BFQ.cpython-37m-x86_64-linux-gnu.so'],
            },
   
)

