#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import sqlite3
import sys

class Operate_table(object):

    def __init__(self):
        self.conn = sqlite3.connect('moods.sqlite')
        self.cur = self.conn.cursor()

    def create_table(self):
        sql = '''CREATE TABLE moods (
                 id integer primary key Autoincrement not null,
                 qq int not null,
                 content text null,
                 comment_count int not null,
                 ctime int not null,
                 phone text null,
                 image text null,
                 locate text null)'''
        self.cur.execute(sql)

    def drop_table(self):
        self.cur.execute('drop table moods')

if __name__ == '__main__':
    app = Operate_table()
    argv = sys.argv[1]
    eval("app.%s()" % argv)
