#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re

import time
import wx

import comands
from filetool import FileTool

import matplotlib.pyplot as plt   # 导入模块 matplotlib.pyplot，并简写成 plt
import numpy as np                # 导入模块 numpy，并简写成 np

class AnalysisFrame(wx.Frame):
    def __init__(self):
        super(AnalysisFrame, self).__init__(parent=None, title='Analysis', size=(600, 800))
        self.Center()
        self.panel = wx.Panel(self)
        self.fileText = wx.TextCtrl(self, pos=(20, 20), size=(320, 23), style=wx.TE_READONLY)
        self.selectBtn = wx.Button(self, label='选择文件', pos=(350, 20), size=(100, 23))
        self.selectBtn.Bind(wx.EVT_BUTTON, self.__select_file)

        wx.StaticText(self, label='选择命令:', pos=(20, 66), size=(60, 30))
        self.cmdSelector = wx.ComboBox(self, value='请选择', choices=comands.cmds, pos=(80, 60), size=(250, 30),
                                       style=wx.CB_SORT | wx.CB_READONLY)
        self.cmdSelector.Bind(wx.EVT_COMBOBOX, self.__select_cmd)

        self.analysisBtn = wx.Button(self, label='开始分析', pos=(350, 60), size=(100, 30))
        self.analysisBtn.Bind(wx.EVT_BUTTON, self.__do_analysis)

        self.warnLabel = wx.StaticText(self, pos=(20, 100))
        self.warnLabel.SetForegroundColour(wx.Colour(255, 0, 0))

        self.cmd = ''

        self.desc = wx.StaticText(self, pos=(20, 110), size=(560, 290))
        self.desc1 = wx.StaticText(self, pos=(20, 420), size=(560, 290))

    def __select_file(self, event):
        """
        选择要分析的文件
        :return:
        """
        wildcard = 'All files(*.*)|*.*'
        dialog = wx.FileDialog(parent=None, message='选择要分析的日志', defaultDir=os.getcwd(), defaultFile='',
                               wildcard=wildcard, style=wx.FC_OPEN)
        if wx.ID_OK == dialog.ShowModal():
            self.fileText.SetValue(dialog.GetPath())
        dialog.Destroy()

    def __select_cmd(self, event):
        """
        选择要分析的命令
        :param event:
        :return:
        """
        print("cmd:{}".format(event.GetString()))
        self.cmd = event.GetString()

    def __do_analysis(self, event):
        """
        开始分析
        :param event:
        :return:
        """
        if self.fileText.GetValue() == '':
            self.warnLabel.SetLabel('请选择日志！！')
            return

        if self.cmd not in comands.cmds:
            self.warnLabel.SetLabel('请选择命令！！')
            return
        output = FileTool.readObject(self.fileText.GetValue())
        x1 = []
        y1 = []
        statisticInfo1 = StatisticInfo('post request cost:')
        x2 = []
        y2 = []
        statisticInfo2 = StatisticInfo('sum cost')
        p1 = 'post_request_cost:.*:{}:'.format(self.cmd)
        pattern1 = '{}\d+'.format(p1)
        p2 = '耗时:{}:'.format(self.cmd)
        pattern2 = '{}\d+'.format(p2)
        time_pattern = '^\\[\d{2}:\d{2}:\d{2}:\d{3}\\]'
        for line in output:
            time = re.match(time_pattern, line)
            if time is None:
                continue
            timestr = re.sub('[\\[\\]]', '', time.group(0))
            mlis = self.format_date(timestr)

            st = re.search(pattern1, line)
            if st is not None:
                t = re.sub(p1, '', st.group(0))
                x1.append(mlis)
                y1.append(int(t))
                statisticInfo1.count(int(t))
                continue

            st1 = re.search(pattern2, line)
            if st1 is not None:
                t = re.sub(p2, '', st1.group(0))
                x2.append(mlis)
                y2.append(int(t))
                statisticInfo2.count(int(t))

        self.desc.SetLabel(statisticInfo1.printStatisticInfo())

        self.desc1.SetLabel(statisticInfo2.printStatisticInfo())

        self.draw(x1, y1, x2, y2, self.cmd)

    def draw(self, x1, y1, x2, y2, cmd):
        plt.title('POS GATEWAY')

        x1 = [i for i in range(len(y1))]
        x2 = [i for i in range(len(y2))]

        plt.plot(x1, y1, color='green', label='{} post cost'.format(cmd))

        plt.plot(x2, y2, color='red', label='{} sum cost'.format(cmd))

        plt.legend()  # 显示图例

        plt.xlabel('time')

        plt.ylabel('cost(ms)')

        plt.show()

    def format_date(self, str):
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

class StatisticInfo(object):
    def __init__(self, title=''):
        self.title = title
        self.c5 = 0
        self.c10 = 0
        self.c15 = 0
        self.c20 = 0
        self.c25 = 0
        self.c30 = 0
        self.c50 = 0
        self.c100 = 0
        self.c200 = 0
        self.cxx = 0
        self.sum = 0

    def count(self, t):
        self.sum += 1
        if t <= 500:
            self.c5 += 1
        elif 500 < t <= 1000:
            self.c10 += 1
        elif 1000 < t <= 1500:
            self.c15 += 1
        elif 1500 < t <= 2000:
            self.c20 += 1
        elif 2000 < t <= 2500:
            self.c25 += 1
        elif 2500 < t <= 3000:
            self.c30 += 1
        elif 3000 < t <= 5000:
            self.c50 += 1
        elif 5000 < t <= 10000:
            self.c100 += 1
        elif 10000 < t <= 20000:
            self.c100 += 1
        else:
            self.cxx += 1

    def printStatisticInfo(self):
        return '======{}======\n' \
               '总数         ：{} 笔\n' \
               '< 500     ms：{} 笔，百分比：{}%\n' \
               '500-1000  ms：{} 笔，百分比：{}%\n' \
               '1000-1500 ms：{} 笔，百分比：{}%\n' \
               '1500-2000 ms：{} 笔，百分比：{}%\n' \
               '2000-2500 ms：{} 笔，百分比：{}%\n' \
               '2500-3000 ms：{} 笔，百分比：{}%\n' \
               '3000-5000 ms：{} 笔，百分比：{}%\n' \
               '5-10       s：{} 笔，百分比：{}%\n' \
               '10-20      s：{} 笔，百分比：{}%\n' \
               '20 >       s：{} 笔，百分比：{}%\n'\
            .format(self.title, self.sum,
                    self.c5, self.countPercent(self.c5),
                    self.c10, self.countPercent(self.c10),
                    self.c15, self.countPercent(self.c15),
                    self.c20, self.countPercent(self.c20),
                    self.c25, self.countPercent(self.c25),
                    self.c30, self.countPercent(self.c30),
                    self.c50, self.countPercent(self.c50),
                    self.c100, self.countPercent(self.c100),
                    self.c200, self.countPercent(self.c200),
                    self.cxx, self.countPercent(self.cxx))

    def countPercent(self, c):
        return round((c * 1.0 / self.sum) * 100, 2)

class AnalysisApp(wx.App):
    def OnInit(self):
        frame = AnalysisFrame()
        frame.Show()
        return True

    def OnExit(self):
        return 0

if __name__ == '__main__':
    app = AnalysisApp()
    app.MainLoop()