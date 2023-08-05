#! /usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools

setuptools.setup(
    name='restsql',
    version='0.1.51',
    description=(
        'RestSQL库。用json与数据库交互。'
    ),
    url='',
    long_description='restsql',
    author="venzozhang",
    author_email='venzozhang@tencent.com',
    maintainer='oliverdding',
    maintainer_email='oliverdding@tencent.com',
    license='MIT License',
    packages=['restsql'],
    install_requires=[
        'bitarray==1.6.1',
        'mysqlclient==1.4.6',
        'psycopg2_binary==2.8.6',
        'certifi==2020.11.8',
        'elasticsearch==5.5.3',
        'elasticsearch-dsl==5.4.0',
        'impyla==0.16.3',
        'numpy==1.16.6',
        'pandas==0.24.2',
        'peewee==3.14.0',
        'python-dateutil==2.8.1',
        'pytz==2020.4',
        'six==1.15.0',
        'thrift==0.9.3',
        'urllib3==1.25.11'
    ],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
