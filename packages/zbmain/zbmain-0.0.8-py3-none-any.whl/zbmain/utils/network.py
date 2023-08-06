#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : zb
# @Time    : 2020/12/02 09:31
import os


def connected():
    '''ping'''
    print('Check Network...')
    result = os.system(u"ping -c2 baidu.com > /dev/null 2>&1")  # 都丢弃，防止输出到控制台
    return result == 0


if __name__ == '__main__':
    print(connected())
