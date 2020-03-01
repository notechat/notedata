#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/06/05 10:35
# @Author  : niuliangtao
# @Site    : 
# @File    : utils.py
# @Software: PyCharm
import logging
import os

from notetool.download import PyCurlDownLoad
from notetool.tool import path_join, path_parse

logger = logging.getLogger(__name__)

__all__ = ['utils', 'data_root', 'raw_root', 'download_file']

data_root = path_parse('~/tmp/')
raw_root = 'https://raw.githubusercontent.com/1007530194/data/master/'


def download(url, file_dir=None, file_path=None, overwrite=False):
    if file_path is not None:
        file_path = path_join(data_root, file_path)
    else:
        if file_dir is not None:
            file_dir = path_join(data_root, file_dir)
        else:
            file_dir = data_root

        basename = os.path.basename(url)
        file_path = path_join(data_root, basename)

    download_file(url, file_path, overwrite=overwrite)


def download_file(url, path, overwrite=False):
    down = PyCurlDownLoad(url=url, path=path, overwrite=overwrite)
    down.download()


def exists(file_path, overwrite=False):
    file_dir, file_name = os.path.split(file_path)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    if os.path.exists(file_path):
        if overwrite:
            logger.info("file:{} exists, overwrite it".format(file_name))
            os.remove(file_path)
            return False
        else:
            logger.info("file:{} exists, return".format(file_name))
            return True
    return False
