#!/usr/local/bin/python3.6
# -*- coding: utf-8 -*-
import os
import re
import time

import matplotlib.pyplot as plt

from filetool import FileTool

basedir = os.path.dirname(__file__)


def process_log_file(start, end):
    """
    处理log文件
    :param start:
    :param end:
    :return:
    """
    x = []
    y = []
    startT = -1
    endT = -1
    output = FileTool.readObject(basedir + '/static/log/info-2020-09-01-4.log')
    pattern = '^\\[\d{2}:\d{2}:\d{2}:\d{3}\\]'
    time_formatter = '%y-%m-%d %H:%M:%S.%f'
    for line in output:
        # 匹配时间
        mlis = -1
        st = re.match(pattern, line)
        if None != st:
            sts = re.sub('[\\[\\]]', '', st.group(0))
            mlis = format_date(sts)
        if None != re.search(start, line):
            if endT == -1:
                startT = mlis
        if None != re.search(end, line):
            if startT != -1:
                endT = mlis
        if startT != -1 and endT != -1:
            # x.append(time.localtime(startT / 1000.0).strftime(time_formatter)[:-3])
            y.append(endT - startT)
            startT = -1
            endT = -1

    return y


def draw_line_chart(x, y):
    """
    绘制折线图
    :param x:
    :param y:
    :return:
    """
    plt.plot(x, y, label='AuthCodePay', linewidth=2, color='r', marker='o', markerfacecolor='blue', markersize='12')
    plt.xlabel = 'cost (ms)'
    plt.ylabel = 'time'
    plt.title = 'Request Cost'

    plt.legend()
    plt.show()


def format_date(str):
    """
    格式化时间，返回当前毫秒数据
    :param str:
    :return:
    """
    mlis = re.sub('\d{2}:\d{2}:\d{2}:', '', str)
    timeStr = '2019-01-01 ' + re.sub(':\d{3}', '', str)
    time_formatter = '%Y-%m-%d %H:%M:%S'
    time_mlis = time.mktime(time.strptime(timeStr, time_formatter))

    return time_mlis * 1000 + int(mlis)


if __name__ == '__main__':
    print('123')
    y = process_log_file('AuthCodePayHandler.java:53', 'AuthCodePayHandler.java:62')
    x = range(0, len(y))
    # x = range(0, 10)
    # y = range(0, 10)
    draw_line_chart(x, y)
