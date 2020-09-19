#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

if __name__ == '__main__':
    print('123')
    line1 = ' POS-00073-20200919071813201:耗时:hf_heart_beat:185:毫秒'
    line = ' - post_request_cost:POS-00109-20200919082250880:hf_heart_beat:6毫秒'
    p1 = 'post_request_cost:.*:hf_heart_beat:'
    pattern1 = '{}\d+'.format(p1)
    p2 = '耗时:{}:'.format('hf_heart_beat')
    pattern2 = '{}\d+'.format(p2)

    st = re.search(pattern1, line)
    if st is not None:
        t = re.sub(p1, '', st.group(0))

    st1 = re.search(pattern2, line1)
    if st1 is not None:
        t1 = re.sub(p2, '', st1.group(0))

    print(345)