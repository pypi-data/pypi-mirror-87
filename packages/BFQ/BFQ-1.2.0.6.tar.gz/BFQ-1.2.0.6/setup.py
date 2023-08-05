#!/usr/bin/env python
#coding: utf-8

from setuptools import setup


from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()



setup(
    name='BFQ',
    python_requires='>=3.7.0',
    version='1.2.0.6',
    author='Billy',
    author_email='ztqstd@163.com',
    url='https://zhengtq.github.io/',
    description=u'博采众长的人脸质量评价库',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['BFQ'],
    license='MIT',
    install_requires=[
        'numpy'
        ],
    package_data={  # Optional
                    'BFQ': ['BFQ.cpython-37m-x86_64-linux-gnu.so'],
            },

)

