#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : zb
# @Time    : 2020/11/18 00:50
# @Blog    : https://blog.zbmain.com

import time as t


def cuttentDateTime():
    '''2020-01-01 00:00:00'''
    return t.strftime("%Y-%m-%d %H:%M:%S")


def cuttentTime():
    '''00:00:00'''
    return t.strftime("%H:%M:%S")


# 作用：减少主函数import time
def time():
    return t.time()


def timeSince(since):
    '''
    阶段耗时
    :param since: 开始时间
    :return: 开始 >> 此刻
    '''
    s = t.time() - since
    m = int(s / 60)
    s -= m * 60
    return '%dm %ds' % (m, s)


if __name__ == "__main__":
    since = t.time() - 9.9 * 60
    print(timeSince(since))
    t.sleep(5)
    print(cuttentTime())
    print(t.strftime("%Y-%m-%d %H:%M:%S"))
    print(cuttentDateTime())
