#!/usr/bin/env python3
#-*- coding:utf-8 -*-

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
            with open('friends/' + each_file) as f:
                source = f.read()
                con_dict = source[75:-4].replace('\n', '')
                con_json = json.loads(con_dict)
                friends_list = con_json['uinlist']

                # Get each item from friends list, each item is a dict
                for item in friends_list:
                    i = i + 1
                    qqnumber_item.append(item)
        else:
            with open('qqnumber.inc', 'w') as qqfile:
                qqfile.write(str(qqnumber_item))

    def exact_mood_data(self):
        '''Get mood data from files in result folder
           This method only use for me to test the result
        '''

        os.chdir("result")
        files = [x for x in os.listdir()]
        for each_file in files:
            with open(each_file) as f:
                con = f.read()
            con_dict = eval(con)
            moods = con_dict['msglist']
            if moods == None:
                continue

            for mood in moods:
                content = mood['content']
                create_time = mood['createTime']
                comment_num = mood['cmtnum']
                phone = mood['source_name']
                pic = mood['pic'][0]['url2'] if 'pic' in mood else ''
                locate = mood['story_info']['lbs']['name'] if 'story_info' in mood else ''

                if content == '' and pic != '':
                    # if the mood only has pic but no other thing
                    content = pic
                if content == '' and 'rt_con' in mood:
                    # if the mood is a forward video
                    # it will be in the mood['rt_con']
                    try:
                        content = mood['rt_con']['conlist'][0]['con']
                    except KeyError:
                        content = mood['rt_con']['conlist'][1]['con']

                print("%s\t%s\t%d\t%s\t%s\t%s" % (content[:10], create_time[:10], comment_num, phone, pic[:10], locate[:10]))
        else:
            print("Finish")
