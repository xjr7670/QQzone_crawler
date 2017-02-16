'''
1. 从数据库中读取数据
2. 把数据读入到Pandas中的DataFrame中
3. 把数据进行分析
4. 分析结果json化
5. 把json化的结果返回给模板文件
6. 在HTML中进行文字陈述说明和作图（使用Echarts）
'''

import sqlite3
import time

import pandas as pd
#import matplotlib.pyplot as plt

from sqlalchemy import create_engine
from flask import Flask
from flask import jsonify

app = Flask(__name__)
engine = create_engine('sqlite:///../moods.sqlite')

def make_time(t1, t2):
    res = time.gmtime(t1)
    if t2 = 'year':
        return res.tm_year
    if t2 = 'month':
        return res.tm_mon
    if t2 = 'wday':
        return res.tm_wday
    if t2 = 'hour':
        return res.tm_hour

@app.route('/qqnum=<qqnum>')
def index(qqnum=None):
    
    # 根据QQ号码读取数据记录
    sql = 'SELECT * FROM moods WHERE qq = ' + str(qqnum)
    df = pd.read_sql_query(sql, engine) 
    
    # 获得年、月、星期、小时
    df['year'] = df.ctime.apply(make_time, args=['year'])
    df['month'] = df.ctime.apply(make_time, args=['month'])
    df['wday'] = df.ctime.apply(make_time, args=['wday'])
    df['hour'] = df.ctime.apply(make_time, args=['hour'])

    # 各个时间周期内分别发表了多少条动态
    year_total = df.year.value_counts()
    month_total = df.month.value_counts()
    wday_total = df.wday.value_counts()
    hour_total = df.hour.value_counts()

    # 获得说说总数
    mood_count = df.id.count()

    return jsonify(mod=int(mood_count))

if __name__ == "__main__":
    app.debug = True
    app.run()
