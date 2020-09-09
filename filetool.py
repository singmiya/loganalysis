#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import logging
import sys

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

__author__ = 'csip'
import os
import pickle

class FileTool:
    def __init__(self):
        pass

    @staticmethod
    def saveObject(filename, obj):
        try:
            with open(filename, 'wb') as f:
                pickle.dump(obj, f)
                return True
        except IOError as e:
            logger.error('发生错误， {}'.format(e.args[-1]))
            return False

    @staticmethod
    def readObject(filename):
        try:
            with open(filename, encoding='utf-8') as f:
                lines = f.readlines()
                return lines
        except IOError as e:
            logger.error('发生错误， {}'.format(e.args[-1]))
            return []

    @staticmethod
    def loadObject(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                obj = pickle.load(f)
                return obj
        except IOError as e:
            logger.error('发生错误， {}'.format(e.args[-1]))
            return None

    @staticmethod
    def saveData(file, data, encoding='utf-8'):
        try:
            with codecs.open(file, 'w', encoding) as f:
                f.write(str(data).decode('unicode-escape'))
                return True
        except IOError as e:
            logger.error('发生错误， {}'.format(e.args[-1]))
            return False


if __name__ == '__main__':
    print(sys.getdefaultencoding())