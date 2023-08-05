import os
from setuptools import setup

# 根据es版本安装python es库
# pymongo
# "elasticsearch-dsl>=6.3.1",
# "elasticsearch-dsl>=7.2.0",

requirements = [
    "pymongo>=3.10.1",
    'elasticsearch>=6.8.1',
    'elasticsearch_dsl>=6.3.1',
    "python-decouple>=3.1",
    "redis>=3.3.11",
    "pycrypto>=2.6.1",
    "pika>=0.12",
    "python-dateutil>=2.7",
    "sqlalchemy>=1.2",
    'py2neo>=4.3.0'
    'numpy>=1.16.4',
    'pandas>=1.0.1',
    'pypinyin>=0.37.0',
    'requests>=2.22.0',
    'pika>=0.12.0',
    'PyMySQL>=0.9.3',
    'selenium>=3.141.0',
    'shortuuid>=0.5.0',
    'PyHive>=0.6.2',
    'threadpool>=1.3.2',
    'beautifulsoup4>=4.9.1',
    'pycryptodome>=3.9.8',
    'python_dateutil>=2.8.1'
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='general-tools',
    version='0.5.8',
    packages=[
        "general_tools",
    ],
    license='BSD License',  # example license
    description='general tools',
    install_requires=requirements,
    long_description_content_type="text/markdown",
    url='',
    author='xw0102',
    author_email='15200813194@163.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.1',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
