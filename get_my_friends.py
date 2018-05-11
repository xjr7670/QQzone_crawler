#!/usr/bin/env python3
#-*- coding:utf-8 -*-

"""
获取自己的QQ好友列表
"""


import requests
from time import sleep
import util


class Get_friends_number(object):
    '''Use to get one's friends from their qzone's entry list'''

    def __init__(self):

        self.headers = util.headers
        self.base_url = util.parse_friends_url()
        util.check_path('friends')
        print('开始获取好友列表，并把文件保存到 friends 文件夹')

    def get_friends(self):

        key = True
        position = 0
        while key:
            url = self.base_url + '&offset=' + str(position)
            referer = 'http://qzs.qq.com/qzone/v8/pages/setting/visit_v8.html'
            self.headers['Referer'] = referer

            print("\tDealing with position\t%d." % position)
            res = requests.get(url, headers=self.headers)
            html = res.text
            with open('friends/offset' + str(position) + '.json', 'w', encoding='utf-8') as f:
                f.write(html)

            # check whether the friend list is over
            # if that, the uinlist is void list
            with open('friends/offset' + str(position) + '.json', encoding='utf-8') as f2:
                con = f2.read()
            if "请先登录" in con:
                print("登录失败，请检查原因")
                key = False
                break
            if '''"uinlist":[]''' in con:
                print("好友列表获取完毕!")
                break
                key = False

            position += 50
            sleep(5)
