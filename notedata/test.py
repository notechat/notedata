#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/06/05 17:08
# @Author  : niuliangtao
# @Site    : 
# @File    : temp.py
# @Software: PyCharm

import logging

from utils import exists

logging.basicConfig(format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%d-%M-%Y %H:%M:%S",
                    level=logging.INFO)

print(exists("/Users/weidian/Documents/MyDiary/notechats/notedata/notedata/temp.py"))
