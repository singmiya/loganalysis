#!/usr/local/bin/python3.6
# -*- coding: utf-8 -*-
import os
import re
import time
import sys
import datetime
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from filetool import FileTool
from TranStatisticInfo import TranStatisticInfo


basedir = os.path.dirname(__file__)

"""
POS网关升级后统计信息分析
"""

def process_log_file():
    """
    处理log文件
    :param start:
    :param end:
    :return:
    """
    originalData = {}
    output = FileTool.readObject('/Users/singsmiya/Downloads/statistic_info.log')
    for line in output:
        tran = process_text(line)
        if tran is None or tran.tranCode is None:
            continue
        if tran.tranCode in originalData:
            originalData[tran.tranCode].append(tran)
        else:
            originalData[tran.tranCode] = [tran]
       

    return originalData


def process_text(info):
    '''
    文本处理
    '''
    # print("processing statistic info ....")
    pattern = '.*TranStatisticInfo\\((.*)\\).*'
    st = re.match(pattern, info)
    if st is not None:
        matchedInfo = st.groups(1)
        return TranStatisticInfo.toObject(matchedInfo[0])

def draw_line_chart(label, xys, title, xl='cost (ms)'):
    """
    绘制折线图
    :param x:
    :param y:
    :return:
    """
    plt.plot(xys[0], xys[1], label=label, linewidth=1, color='r', marker='o', markerfacecolor='blue', markersize='8')
    plt.xlabel = xl
    plt.ylabel = '时间点'
    plt.title = title

    plt.legend()
    plt.show()


def draw_line_chart(label, x1, y1, x2, y2, title, xl='cost (ms)'):
    """
    绘制折线图
    :param x:
    :param y:
    :return:
    """
    # plt.plot(x1, y1, x2, y2, label=label, linewidth=1, color='r', marker='o', markerfacecolor='blue', markersize='8')
    plt.plot(x1, y1, x2, y2)
    plt.xlabel = xl
    plt.ylabel = '时间点'
    plt.title = title

    # plt.legend()
    plt.show()

if __name__ == '__main__':
    print('参数个数为:{}'.format(len(sys.argv)))
    print('参数列表:{}'.format(str(sys.argv)))
    originalData = process_log_file()
    # print(originalData)
    str = '各个命令的请求数：\n'
    total = 0
    for k in originalData.keys():
        total += len(originalData[k])
        str = str + "{:25s} ：{} \n".format(k, len(originalData[k]))
    
    str += "{:25s} ：{} \n".format('总请求数', total)
    print(str)
    
    
    tranCode = sys.argv[1]

##################### 散点图 #####################
    # xyData = []

    # if len(sys.argv) > 2 and tranCode in originalData.keys() and sys.argv[2] != '':
    #     attrs = sys.argv[2].split(',')
    #     handles = []
    #     labels = []
    #     for attr in attrs:
    #         if attr not in dir(TranStatisticInfo()):
    #             continue
    #         x = []
    #         y = []
            
    #         for tran in sorted(originalData[tranCode], key= lambda tran: tran.collectTime):
    #             ct = datetime.datetime.fromtimestamp(int(tran.collectTime) / 1000)
    #             x.append(ct)
    #             y.append(float(getattr(tran, attr)))
            
    #         handles.append(plt.scatter(x, y))
    #         labels.append(attr)
              
    #         # plt.plot(x, y, label=attr)
    #     # draw_line_chart(tranCode, xyData[0], xyData[1], xyData[2], xyData[3], title='统计信息')
    #     plt.legend(handles=handles, labels=labels, loc='best')
    #     plt.ylabel = '时间点'
    #     plt.title = '统计信息'

    #     plt.show()



##################### 折线图 #####################
    # xyData = []

    # if len(sys.argv) > 2 and tranCode in originalData.keys() and sys.argv[2] != '':
    #     attrs = sys.argv[2].split(',')
    #     handles = []
    #     labels = []
    #     for attr in attrs:
    #         if attr not in dir(TranStatisticInfo()):
    #             continue
    #         x = []
    #         y = []
            
    #         for tran in sorted(originalData[tranCode], key= lambda tran: tran.collectTime)[-3000:]:
    #             ct = datetime.datetime.fromtimestamp(int(tran.collectTime) / 1000)
    #             x.append(ct)
    #             y.append(float(getattr(tran, attr)))
            
    #         handles.append(plt.plot(x, y))
    #         labels.append(attr)    
              
    #         # plt.plot(x, y, label=attr)
    #     # draw_line_chart(tranCode, xyData[0], xyData[1], xyData[2], xyData[3], title='统计信息')
    #     plt.legend(handles=handles, labels=labels, loc='best')
    #     plt.ylabel = '时间点'
    #     plt.title = '统计信息'

    #     plt.show()

##################### 堆叠柱状图 #####################

    if len(sys.argv) > 2 and tranCode in originalData.keys() and sys.argv[2] != '':
        attrs = sys.argv[2].split(',')
        handles = []
        labels = []


        subData = sorted(originalData[tranCode], key= lambda tran: tran.collectTime)[-2000:]
        x = []
        ys = {}
        # tranJnls = []
        for tran in subData:
            ct = datetime.datetime.fromtimestamp(int(tran.collectTime) / 1000)
            x.append(ct)
            # tranJnls.append(getattr(tran, 'tranJnl'))
            atotal = 0
            for attr in attrs:
                if attr not in dir(TranStatisticInfo()):
                    continue
                atotal += float(getattr(tran, attr))
            for attr in attrs:
                if attr not in dir(TranStatisticInfo()):
                    continue
                if attr in ys.keys():
                    ys[attr].append(float(getattr(tran, attr)) / atotal)
                    ys[attr].append(float(getattr(tran, attr)))
                else:
                    ys[attr] = [float(getattr(tran, attr)) / atotal]
                    ys[attr] = [float(getattr(tran, attr))]
        
        data1 = np.array([np.array(l) for l in ys.values()])

        for i in range(len(attrs)):
            k = attrs[i]
            v = ys[k]
            plt.bar(range(len(v)), v, width=0.1, bottom=data1[:i].sum(axis=0), label=k)

        plt.legend()
        plt.ylabel = '时间点'
        plt.title = '统计信息'

        plt.show()