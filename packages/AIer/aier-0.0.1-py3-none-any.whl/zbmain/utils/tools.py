#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : zb
# @Time    : 2020/11/18 01:05
# @Blog    : https://blog.zbmain.com
import torch


# devices
class devices():
    torch = torch.device(torch.cuda.is_available() and 'cuda' or 'cpu')
    '''torch方式'''
    tensorflow = 'GPU:0'
    '''tensorflow方式'''

# others
