#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import requests
from time import sleep
import util

class Get_friends_number(object):
    '''Use to get one's friends from their qzone's entry list'''

    def __init__(self):

        self.headers = util.headers
        self.base_url = util.parse_friends_url()
        util.check_path('friends')
        print('Start to get friends list and save it for ./friends folder')

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
            with open('friends/offset' + str(position) + '.json', 'w') as f:
                f.write(html)

            # check whether the friend list is over
            # if that, the uinlist is void list
            with open('friends/offset' + str(position) + '.json') as f2:
                con = f2.read()
            if "请先登录" in con:
                print("登录失败，请检查原因")
                key = False
                break
            if '''"uinlist":[]''' in con:
                print("Get friends Finish")
                break
                key = False

            position += 50
            sleep(5)
