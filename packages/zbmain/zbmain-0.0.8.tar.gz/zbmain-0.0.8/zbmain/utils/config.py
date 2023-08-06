#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : zb
# @Time    : 2020/12/01 12:44
# @Blog    : https://blog.zbmain.com
from zbmain.utils import network
from urllib.request import urlopen
import json
import os

# 机器人配置表
REBOT_CONFIG_PATH = './zbmain/config/robot.json'
REBOT_CONFIG_URL = 'https://zbmain.com/files/config/robot.json'
# 翻译器配置表
TRANSLATE_CONFIG_PATH = './zbmain/config/translate.json'
TRANSLATE_CONFIG_URL = 'https://zbmain.com/files/config/translate.json'


def __getRobotConfigFromJson(type: str = 'baidu'):
    resultJSON = __getJson(REBOT_CONFIG_PATH, REBOT_CONFIG_URL)
    return isinstance(resultJSON, str) and resultJSON or \
           (resultJSON['robot'][type]['appid'], \
            resultJSON['robot'][type]['apiKey'], \
            resultJSON['robot'][type]['secretKey'], \
            resultJSON['robot'][type]['robotid'])  # 返回值是字符串，说明异常


def __getTranslateConfigFromJson(type: str = 'baidu'):
    resultJSON = __getJson(TRANSLATE_CONFIG_PATH, TRANSLATE_CONFIG_URL)
    return isinstance(resultJSON, str) and resultJSON or \
           (resultJSON['translate'][type]['appid'], \
            resultJSON['translate'][type]['secretKey'])  # 返回值是字符串，说明异常


def __getJson(*paths):
    '''自用方法，参数必须是两个元素的列表。若发生异常，返回值为字符串类型'''
    resultJSON = ''
    try:
        with open(paths[0]) as json_file:
            resultJSON = json.load(json_file)
    except:
        print('Local File config.json Not Found')
        if not network.connected():
            return 'Network Unconnected'
        try:
            print('Online config.json Downloading...')
            configUrl = paths[1]
            resultJSON = json.loads(urlopen(configUrl).read())
        except:
            return 'Online File config.json Not Found'
    return resultJSON
