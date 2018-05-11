#!/usr/bin/env python3
#-*- coding:utf-8 -*-

"""
从上一步获取到的QQ列表文件夹中，提取出QQ号，并保存到qqnumber.inc文件中
"""

import json
import os


class exact_data_from_result(object):
    '''Define method to get my qq friends data from result
       and get my mood data from result'''

    def __init__(self):
        print("Start to exact the qq number item from get_friends result")

    def exact_qq_number(self):
        '''Get qq number data from json file'''
        friendsFiles = [x for x in os.listdir('friends') if x.endswith("json")]

        qqnumber_item = []
        i = 0
        for each_file in friendsFiles:
            with open('friends/' + each_file, encoding='utf-8') as f:
                source = f.read()
                con_dict = source[75:-4].replace('\n', '')
                con_json = json.loads(con_dict)
                friends_list = con_json['uinlist']

                # Get each item from friends list, each item is a dict
                for item in friends_list:
                    i = i + 1
                    qqnumber_item.append(item)
        else:
            with open('qqnumber.inc', 'w', encoding='utf-8') as qqfile:
                qqfile.write(str(qqnumber_item))
