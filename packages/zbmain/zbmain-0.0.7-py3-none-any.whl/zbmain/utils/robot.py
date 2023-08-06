#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : zb
# @Time    : 2020/12/01 12:43
# @Blog    : https://blog.zbmain.com

from zbmain.utils import config
import json
import random
import requests

app_id = ""
secret_key = ""


class UnitRobot(object):
    def __init__(self,
                 app_id,
                 secret_key,
                 unit_url='https://aip.baidubce.com/oauth/2.0/token',
                 robot_url='https://aip.baidubce.com/rpc/2.0/unit/service/chat',
                 chat_reply='不好意思，俺们正在学习中，随后回复你。'):
        '''官方api'''
        grant_type = 'client_credentials'
        self.unit_url = unit_url + f'?grant_type={grant_type}&client_id={app_id}&client_secret={secret_key}'
        self.robot_url = robot_url
        self.chat_reply = chat_reply

    def __call__(self, chat_input, robot_id='S40811', user_id='88888'):
        '''
        调用百度UNIT接口，回复聊天内容
        :param chat_input: 输入上文
        :param user_id: 用户id（日志记录）
        :return:
        输出下文（答复）
        '''
        res = requests.get(self.unit_url)
        access_token = eval(res.text)["access_token"]
        self.robot_url = self.robot_url + '?access_token=' + str(access_token)
        post_data = {
            "log_id": str(random.random()),
            "request": {
                "query": chat_input,
                "user_id": user_id
            },
            "session_id": "",
            "service_id": robot_id,
            "version": "2.0"
        }
        res = requests.post(url=self.robot_url, json=post_data)
        unit_chat_obj = json.loads(res.content)
        if unit_chat_obj["error_code"] != 0: return self.chat_reply

        unit_chat_obj_result = unit_chat_obj["result"]
        unit_chat_response_list = unit_chat_obj_result["response_list"]

        unit_chat_response_obj = random.choice(
            [unit_chat_response for unit_chat_response in unit_chat_response_list if
             unit_chat_response["schema"]["intent_confidence"] > 0.0])
        unit_chat_response_action_list = unit_chat_response_obj["action_list"]
        unit_chat_response_action_obj = random.choice(unit_chat_response_action_list)
        unit_chat_response_say = unit_chat_response_action_obj["say"]
        return unit_chat_response_say
