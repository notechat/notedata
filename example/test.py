#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/05/23 20:04
# @Author  : niuliangtao
# @Site    : 
# @File    : temp.py
# @Software: PyCharm

import logging
import os

logging.info('info 信息')

url = 'http://www.**.net/images/logo.gif'
filename = os.path.basename(url)
print(filename)
