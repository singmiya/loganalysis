#!/usr/local/bin/python3.6
# -*- coding: utf-8 -*-
import re

import matplotlib.pyplot as plt
import numpy as np
import time
from matplotlib.ticker import FuncFormatter

from analysis import basedir
from filetool import FileTool
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

def process_log_file(keyword):
    """
    处理log文件
    :param keyword:
    :return:
    """
    x = []
    y = []
    output = FileTool.readObject(basedir + '/static/log/info.log')
    for line in output:
        # 匹配时间

        pattern = re.compile(keyword)
        matcher = re.search(pattern, line)
        if None is not matcher:
            mlis = matcher.group().replace('Somiya', '')
            y.append(int(mlis) / 1000.0)

    return y


def changey(temp, position):
    return float(temp / 1000)

def changex(temp, position):
    return float(temp / 1000)


def draw_line_chart(name, x, y):
    """
    绘制折线图
    :param x:
    :param y:
    :return:
    """
    plt.plot(x, y, label=name, linewidth=2, color='r', marker='o', markerfacecolor='blue', markersize='12')
    plt.xlabel = 'cost (s)'
    plt.ylabel = 'time'
    plt.title = 'Request Cost'

    plt.legend()
    plt.show()


def draw_bar_chart(y):
    SECTION5_ = 0 # 统计大于5秒响应的
    SECTION4_5 = 0 # 统计4-5秒内响应的
    SECTION3_4 = 0 # 统计3-4秒内响应的
    SECTION2_3 = 0 # 统计2-3秒内响应的
    SECTION1_2 = 0 # 统计1-2秒内响应的
    SECTION0_1 = 0 # 统计小于1秒响应的

    for ts in y:
        if ts >= 5:
            SECTION5_ += 1
        elif ts >= 4 and ts < 5:
            SECTION4_5 += 1
        elif ts >= 3 and ts < 4:
            SECTION3_4 += 1
        elif ts >= 2 and ts < 3:
            SECTION2_3 += 1
        elif ts >= 1 and ts < 2:
            SECTION1_2 += 1
        else:
            SECTION0_1 +=1
    yy = [SECTION0_1, SECTION1_2, SECTION2_3, SECTION3_4, SECTION4_5, SECTION5_]
    names = ['0-1秒', '1-2秒', '2-3秒', '3-4秒', '4-5秒', '大于5秒']
    SUM = len(y)
    yy1 = []

    for num in range(len(yy)):
        yy1.append(round((yy[num] * 1.0 / SUM) * 100, 2))
        plt.text(names[num], yy[num] + 0.05, '%.0f' % yy[num], ha='center', va='bottom', fontSize=11)
    x_axis = tuple(range(len(yy1)))
    y_axis = tuple(yy1)
    plt.bar(names, yy1, color='rgb')

    plt.xlabel(u'区间')
    plt.ylabel(u'时间')
    plt.title('请求耗时分布')
    plt.ylim(0, 100)
    # plt.savefig('{}.png'.format(time.strftime('%Y%m%d%H%M%S')))
    plt.show()


if __name__ == '__main__':
    print('test')
    y = process_log_file('Somiya\d+Somiya')
    x = range(0, len(y))
    # draw_line_chart('query-acc-balance', x, y)
    draw_bar_chart(y)
