# -*- coding: UTF-8 -*-
import os
from collections import Counter
import jieba.analyse
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt


class wc:
    def __init__(self, wordin, img_file, font_file, qqnum):
        self.text = wordin  # 把分词链接起来，加空格因为英文靠空格分词
        self.img = plt.imread(img_file)
        self.wc = WordCloud(font_path=font_file, background_color='white', max_words=100, mask=self.img,
                            max_font_size=80)
        # font_path指的是字体文件路径，因为wordcloud自带的字体不支持中文所以我们要指定一个字体文件，否者输出的图片全是框框
        # background_color 默认是黑色　我设置成白色
        # max_words最大显示的词数
        # mask 背景图片
        # max_font_size　最大字体字号
        # print(str(self.text))
        self.word_cloud = self.wc.generate(str(self.text))
        self.qqnum = qqnum

    def show_wc(self):
        # img_color = ImageColorGenerator(self.img)
        plt.imshow(self.word_cloud)
        # plt.imshow(self.wc.recolor(color_func=img_color))  # 使图片颜色跟字体颜色一样
        plt.axis("off")
        plt.savefig('./static/'+str(self.qqnum) + '.jpg')
        # plt.show()
        return '../static/'+str(self.qqnum) + '.jpg'


# 分词模板
def cut_word(datapath):
    with open(datapath, 'r', encoding='utf-8') as fr:
        string = fr.read()
        # 对文件中的非法字符进行过滤
        data = re.sub(r"[\s+\.\!\/_,$%^*()【】：\]\[\-:;+\"\']+|[+——！，。？?=、~@<>《》#￥；“”%……&*（）{}\\\]+|[A-Za-z0-9_]+", "",
                      string)
        word_list = jieba.cut(data)
        return word_list


# 词频统计模块
def statistic_top_word(word_list):
    # 统计每个单词出现的次数，别将结果转化为键值对（即字典）
    result = dict(Counter(word_list))
    # sorted对可迭代对象进行排序
    # items()方法将字典的元素转化为了元组，而这里key参数对应的lambda表达式的意思则是选取元组中的第二个元素作为比较参数
    # 排序后的结果是一个列表，列表中的每个元素是一个将原字典中的键值对转化为的元祖
    sortlist = sorted(result.items(), key=lambda item: item[1], reverse=True)
    return sortlist


# 获得单词
def wordlist(qqnum):
    sum_list = {}
    sum_string = []
    # 设置数据集地址
    datapath = '../mood_result/' + str(qqnum) + '/'
    # 对文本进行分词
    try:
        for files in os.listdir(datapath):
            if files is not None:
                word_list = cut_word(datapath + files)
                # 统计文本中的词频
                statistic_result = statistic_top_word(word_list)
                # 输出统计结果
                for result in statistic_result:
                    if str(result[0]) == '年月日':
                        continue
                    else:
                        if str(result[0]) in sum_list.keys():
                            sum_list[str(result[0])] = str(int(result[1]) + int(sum_list[str(result[0])]))
                        else:
                            sum_list[str(result[0])] = str(result[1])
        for key_sum in sum_list.keys():
            sum_string.append(key_sum + ' ')
        return ''.join(sum_string)
    except BaseException:
        return '请 输入 正确 的 号码'


def get_wordcloud(qqnum):
    # 这里需要注意的是'C:\\Windows\\Fonts\\simfang.ttf'这个为字体文件，本路径为Windows下。如果为Linux系统请在/usr/share/fonts目录下选择自己想要的字体
    mywc = wc(wordlist(qqnum), 'mask.jpg', 'C:\\Windows\\Fonts\\simfang.ttf', qqnum)
    return mywc.show_wc()
