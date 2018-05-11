#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
把包含动态的文件下载下来
"""


import requests
import os
import sys
import time
import util


class Get_moods(object):
    '''Get moods file with cookie'''

    def __init__(self):
        self.session = requests.Session()
        self.headers = util.headers
        self.g_tk = util.g_tk

    def get_moods(self, qqnumber):
        '''Use cookie and header to get moods file and save it to result folder with QQnumber name'''

        referer = 'http://user.qzone.qq.com/' + qqnumber
        self.headers['Referer'] = referer

        # Create a folder with qq number to save it's result file
        util.check_path('mood_result/' + qqnumber)

        # Get the goal url, except the position argument.
        url_base = util.parse_moods_url(qqnumber)

        pos = 0
        key = True

        while key:
            print("\tDealing with position:\t%d" % pos)
            url = url_base + "&pos=%d" % pos
            # print(url)   # for debug use
            res = self.session.get(url, headers = self.headers)
            con = res.text
            with open('mood_result/' + qqnumber + '/' + str(pos), 'w', encoding="utf-8") as f:
                f.write(con)

            if '''"msglist":null''' in con:
                key = False

            # Cannot access...
            if '''"msgnum":0''' in con:
                with open('crawler_log.log', 'a', encoding="utf-8") as log_file:
                    log_file.write("%s Cannot access..\n" % qqnumber)
                key = False

            # Cookie expried
            if '''"subcode":-4001''' in con:
                with open('crawler_log.log', 'a', encoding="utf-8") as log_file:
                    log_file.write('Cookie Expried! Time is %s\n' % time.ctime())
                sys.exit()

            pos += 20
            time.sleep(5)

    #below method only make for me to get the friend's mood
    #which havn't download yet.
    #
    #def get_rest_number(self):

    #    exists_number = os.listdir('mood_result')
    #    with open('qqnumber_backup.inc') as f:
    #        con = f.read()
    #    con = eval(con)
    #    for item in con:
    #        qq = item['data']
    #        if qq not in exists_number:
    #            print("Dealing with:\t%s" % qq)
    #            self.get_moods(qq)
    #    else:
    #        print('Finish!')


class Get_moods_start(object):

    def __init__(self):
        print('Start to get all friend\'s mood file and save it to the mood_result folder')

    def get_moods_start(self):
        app = Get_moods()
        #app.get_rest_number()

        with open('qqnumber.inc', encoding="utf-8") as qnumber_file:
            qnumber_string = qnumber_file.read()
        qnumber_list = eval(qnumber_string)

        # check if there is a mood_result folder to save the result file
        # if not create it
        util.check_path('mood_result')

        while qnumber_list != []:
            save_back_qnumber = qnumber_list[:]
            item = qnumber_list.pop()
            qq = item['data']
            print("Dealing with:\t%s" % qq)

            start_time = time.ctime()
            with open('crawler_log.log', 'a', encoding="utf-8") as log_file:
                log_file.write("Program run at: %s\tGetting %s data...\n" % (start_time, qq))

            try:
                app.get_moods(qq)
            except KeyboardInterrupt:
                print('User Interrupt, program will exit')
                sys.exit()
            except Exception as e:
                # Write the rest item back to qqnumber.inc
                with open('qqnumber.inc', 'w', encoding="utf-8") as qnumber_file:
                    qnumber_file.write(str(save_back_qnumber))

                # Write the log
                with open('crawler_log.log', 'a', encoding="utf-8") as log_file:
                    exception_time = time.ctime()
                    log_file.write("Exception occured: %s\n%s\n" % (exception_time, e))
            else:
                print("%s Finish!" % qq)
        else:
            print("Finish All!")
