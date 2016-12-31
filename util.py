#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from urllib import parse
import os

def get_cookie():
    '''Get cookie from cookie_file'''
    with open('cookie_file') as f:
        cookie = f.read()
    cookie = cookie.replace('\n', '')

    return cookie

cookie = get_cookie()

headers = {'host': 'h5.qzone.qq.com',
            'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0',
            'Accept': '*/*',
            'Accept-Language': 'zh,zh-CN;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cookie': cookie,
            'connection': 'keep-alive'}

def get_g_tk():
    ''' make g_tk value'''

    pskey_start = cookie.find('p_skey=')
    pskey_end = cookie.find(';', pskey_start)
    p_skey = cookie[pskey_start+7: pskey_end]

    h = 5381

    for s in p_skey:
        h += (h << 5) + ord(s)

    return h & 2147483647

g_tk = get_g_tk()

def parse_moods_url(qqnum):
    '''This method use to get every friend's mood cgi url
       So it needs the friend's qqnumber to get their url
    '''

    params = {"cgi_host": "http://taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6",
              "code_version": 1,
              "format": "jsonp",
              "g_tk": g_tk,
              "hostUin": qqnum,
              "inCharset": "utf-8",
              "need_private_comment": 1,
              "notice": 0,
              "num": 20,
              "outCharset": "utf-8",
              "sort": 0,
              "uin": qqnum}
    host = "https://h5.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?"

    url = host + parse.urlencode(params)
    return url

def parse_friends_url():
    '''This method only generate the friends of the owner
       So do not need to get qq number, just get it from
       self cookie
    '''

    cookie = headers['Cookie']
    qq_start = cookie.find('o_cookie=')
    qq_end = cookie.find(';', qq_start)
    qqnumber = cookie[qq_start+9 : qq_end]
    params = {"uin": qqnumber,
              "fupdate": 1,
              "action": 1,
              "g_tk": g_tk}

    host = "https://h5.qzone.qq.com/proxy/domain/base.qzone.qq.com/cgi-bin/right/get_entryuinlist.cgi?"
    url = host + parse.urlencode(params)

    return url

def check_path(path):
    '''This method use to check if the path is exists.
       If not, create that
    '''

    if not os.path.exists(path):
        os.mkdir(path)
