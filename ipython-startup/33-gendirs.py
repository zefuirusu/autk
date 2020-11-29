#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
def gendirs():
    '''
    make directories according to the name of files in the current directory.
    去掉所有的中文字符,以英文名字命名文件夹.
    '''
    for i in os.listdir():
        b1=re.sub(r'\.pdf$',r'',i)
        b2=re.sub(r'-*[\u4e00-\u9fa5]+.+',r'',b1)
        print('replace 1: %s'%b1)
        print('replace 2: %s'%b2)
        try:
            os.makedirs(b2)
        except FileExistsError:
            print('%s exists!'%b2)
            pass
#
