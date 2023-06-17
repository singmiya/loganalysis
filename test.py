#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import time
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    ''''''
    
    # print(time.strftime("%Y-%m-%d %H:%M:%S.%f", time.localtime(15041720415346146/1000000)))
    # print(datetime.datetime.fromtimestamp(1686723983029/1000))
    # print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    np.random.seed(20221220)
    data = np.random.randint(1, 10, (5, 8))
    for index, row in enumerate(data):
        plt.bar(range(len(row)), row, bottom=data[:index].sum(axis=0), label=f'row{index}')

    plt.xlabel('position')
    plt.ylabel('values')
    plt.title('stacked bars', fontsize=18)
    plt.legend()
    plt.show()