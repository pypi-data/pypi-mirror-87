#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: util
@time: 2020/12/7
@email: coderflying@163.com
@desc: 
"""
import hashlib

def get_md5(*args):
    """
    获取传入字符串的md5值
    :param args:
    :return:
    """
    md5 = hashlib.md5()
    [md5.update(arg.encode("utf-8")) for arg in args]
    return md5.hexdigest()
