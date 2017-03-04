import time

def make_time(utstime, time_period):
    res = time.gmtime(utstime)
    if time_period == 'year':
        return res.tm_year
    if time_period == 'month':
        return res.tm_mon
    if time_period == 'wday':
        return res.tm_wday
    if time_period == 'hour':
        return res.tm_hour

def make_dict(pd_series):
    count_series = pd_series.value_counts()
    length = len(count_series)
    time_dict = dict()
    
    for i in range(length):
        time_dict[int(count_series.index[i])] = int(count_series.values[i])

    return time_dict

# 根据传入的UTS时间戳返回年、月、日
def make_date(utstime):
    res = time.gmtime(utstime)
    return (res.tm_year, res.tm_mon, res.tm_mday)
