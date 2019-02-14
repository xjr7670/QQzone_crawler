#-*- coding:utf-8 -*-
'''
1. 从数据库中读取数据
2. 把数据读入到Pandas中的DataFrame中
3. 把数据进行分析
4. 分析结果json化
5. 把json化的结果返回给模板文件
6. 在HTML中进行文字陈述说明和作图（使用Echarts）
'''

import time
import json
import sqlite3
import os

import pandas as pd
from util import make_time
from util import make_dict
from util import make_date

from sqlalchemy import create_engine
from get_word import get_wordcloud
from flask import Flask
from flask import jsonify
from flask import render_template

app = Flask(__name__)
engine = create_engine('sqlite:///../moods.sqlite')


@app.route('/')
def hello():
    return "Welcome!"


@app.route('/qqnum=<qqnum>')
def index(qqnum=None):
    # 根据QQ号码读取数据记录
    sql = 'SELECT * FROM moods WHERE qq = ' + str(qqnum)
    df = pd.read_sql_query(sql, engine)

    # 用字典来保存各项统计数字
    total_info = dict()

    # 保存QQ号
    total_info['qqnum'] = qqnum

    # 获得说说总数
    total_info['mood_count'] = int(df.id.count())

    # 获得年、月、星期、小时
    df['year'] = df.ctime.apply(make_time, args=['year'])
    df['month'] = df.ctime.apply(make_time, args=['month'])
    df['wday'] = df.ctime.apply(make_time, args=['wday'])
    df['hour'] = df.ctime.apply(make_time, args=['hour'])

    # 各个时间周期内分别发表了多少条动态
    total_info['year_total'] = make_dict(df.year)
    total_info['month_total'] = make_dict(df.month)
    total_info['wday_total'] = make_dict(df.wday)
    total_info['hour'] = make_dict(df.hour)

    # 有多少条动态是带有图片的
    total_info['image_count'] = len(df[df.image != ''])

    # 最早和最晚一条动态的发表年、月、日
    first_mood = df.ctime.min()
    last_mood = df.ctime.max()
    total_info['first_mood'] = make_date(first_mood)
    total_info['last_mood'] = make_date(last_mood)
    total_info['wordcloud_total'] = get_wordcloud(qqnum=qqnum)

    return render_template('index.html', total=total_info)


if __name__ == "__main__":
    app.debug = False
    app.run(host='0.0.0.0', port=5000)
