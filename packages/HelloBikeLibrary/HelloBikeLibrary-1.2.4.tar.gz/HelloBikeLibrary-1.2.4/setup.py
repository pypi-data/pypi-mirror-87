# -*- coding: utf-8 -*-
# @Author: yongfanmao
# @Date:   2020-03-11 20:15:52
# @E-mail: maoyongfan@163.com
# @Last Modified by:   yongfanmao
# @Last Modified time: 2020-12-02 21:29:33
# !/usr/local/bin/python 
# coding=utf-8 
# __author__ = 'admin' 
 
 
from setuptools import setup, find_packages 
 
 
with open('README.md', 'r') as rd: 
    long_description = rd.read() 
 
 
setup( 
    name='HelloBikeLibrary', # project Name
    version='1.2.4', # project version number
    packages=find_packages(), 
    # auto find python packages in the project
    description = 'test framework',
    url = None,
    author='maoyongfan', 
    author_email='maoyongfan@163.com', 
    license='MIT',
    long_description = long_description,
    keywords = 'api test python language frameworks',
    # include_package_data=True, #设成True，则自动添加你的工程目录中的所有的文件，如果没有额外的指明，只添加全部的文件
    # zip_safe = True, #指明你的工程是否能够以压缩的格式安装
    # scripts = ['main.py'], #安装时需要执行的脚本列表
    python_requires='>=3', # depand on python version
    # use pip to install these python dependancy libraries. 
    install_requires = [
        "uuid"
		# "certifi==2019.11.28",
		# "chardet==3.0.4",
		# "idna==2.9",
		# "numpy==1.18.1",
		# "Pillow==7.0.0",
		# "psycopg2-binary==2.8.4",
		# "Pygments==2.5.2",
		# "Pypubsub==4.0.3",
		# "requests==2.23.0",
		# "robotframework==3.1.2",
		# "robotframework-databaselibrary==1.2.4",
		# "robotframework-ride==1.7.4.1",
		# "six"
		# "urllib3"
		# "wxPython"
		],
    package_data={
        # If any package contains *.yml ..files, include them:
        '': ['*.yml', '*.ini','*.xlsx', '*.xls', '*.md', '*.rst', '*.txt'],
        # And include any *.xml files found in the 'objMap' package, too:
        'objMap': ['*.xml'],
    }, #指明了需要添加的文件
    
    # if the data file is out of the project directory, use data_files or MANIFEST.in 
    # if to use wheel, here use data_files 
    # if to use source package, here use MANIFEST.in 
    # data_files=[('mydata', ['data/conf.yml'])], 
    
    # add the 'data/conf.yml' to 'mydata' dir 
    # project classify 
    classifiers=[         
        # How mature is this project? Common values are         
        # 3 - Alpha         
        # 4 - Beta         
        # 5 - Production/Stable 
        'Development Status :: 3 - Alpha',   
      
        # Indicate who your project is intended for 
        'Intended Audience :: Developers', 
        'Topic :: Software Development :: Build Tools',  
       
        # Pick your license as you wish (should match "license" above) 
        'License :: OSI Approved :: MIT License',         
 
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both. 
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
    ]#,
 
    # project_urls = { 
    #     "project_git_address" : "http://gitserver-project.git",
    # }

)
