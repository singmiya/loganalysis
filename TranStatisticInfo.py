#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import time

class TranStatisticInfo(object):
    def __init__(self):
        '''消息长度 byte'''
        self.msgLength = 0
        '''回复消息长度'''
        self.rMsgLength = 0
        '''解码耗时 (ms)'''
        self.decodeCost = 0.0
        '''编码耗时 (ms)'''
        self.encodeCost = 0.0
        '''业务处理耗时, 包含网络请求耗时 (ms)'''
        self.bizCost = 0.0
        '''http网络请求耗时 (ms)'''
        self.netCost = 0.0
        self.recvCost = 0.0
        '''发送消息时间 System.nanoTime()'''
        self.sendTime = 0
        '''将数据发送至对端耗时'''
        self.sendCost = 0.0
        '''总耗时'''
        self.totalCost = 0.0
        '''请求命令'''
        self.tranCode = None
        self.retCode = None
        self.retMsg = None
        self.payType = None
        '''支付方式名称'''
        self.payTypeName = None
        '''写速率'''
        self.writeRate = 0
        '''读速率'''
        self.readRate = 0
        '''channel id'''
        self.channelId = None
        '''System.nanoTime()'''
        self.startTime = 0
        '''System.nanoTime()'''
        self.endTime = 0
        '''终端编号'''
        self.terminalNo = None
        '''终端流水号'''
        self.tranJnl = None
        '''租户id'''
        self.renter = None
        '''实例id'''
        self.instanceId = None
        '''收集时间'''
        self.collectTime = 0

    
    @staticmethod
    def toObject(info):
        if info is None:
            return None
        info_attrs = info.split(', ')
        tran = TranStatisticInfo()
        for att in info_attrs:
            if att is None:
                continue
            kv = att.split('=')
            if kv is None:
                continue
            if len(kv) > 1 and kv[1] != 'null':
                setattr(tran, kv[0], kv[1])
        return tran
    
    

if __name__ == '__main__':
    info = 'msgLength=346, rMsgLength=597, decodeCost=0.004, encodeCost=0.007, bizCost=3.0, netCost=0.0, recvCost=0.0, sendTime=15036506382740277, sendCost=0.285, totalCost=4.145, tranCode=sync_white_list, retCode=0000, retMsg=成功, payType=null, payTypeName=null, writeRate=2464, readRate=2383, channelId=506b8dfffeaabfd4-00002617-000020c1-5578bb264193497c-776728fe, startTime=15036506378880052, endTime=15036506383025198, terminalNo=POS41016, tranJnl=POS-41016-20230614125929, renter=, instanceId=1, collectTime=1686718768508'
    tran = TranStatisticInfo.toObject(info)
    print(tran)