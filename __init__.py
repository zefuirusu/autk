#!/usr/bin/env python
# coding=utf-8
import os
import sys
sys.path.append(os.path.abspath(os.curdir))
from .financialtk.modules.mortalGL import MGL
from .fileAssistant.skjoinxl import JoinExcel,get_time_str
# from .financialtk.zhtk.logwriter import wtlog
print('with autk, get those quick functions:')
print(['mgl','joinxl','wtlog','get_time_str'])
def mgl(fpath='',shtna='Sheet1',title=0,glid_index=[],auto=False):
    return MGL(fpath=fpath,shtna=shtna,title=title,glid_index=glid_index,auto=auto)
def joinxl(savedir=os.path.abspath(os.curdir),prefix='',suffix=get_time_str(woc=True)):
    return JoinExcel(savedir=savedir,prefix=prefix,suffix=suffix)
def get_time_info(woc=False):
    return get_time_str(woc=woc)
def wtlog(logline,logdir='./log_default.txt'):
    '''
    writing printing log file.
    logline is what you write and logdir is the log file location.
    '''
    with open(logdir,mode='a',encoding = 'utf-8') as f:
        f.write(logline)
        f.write('\n')
    return
#
if __name__=='__main__':
    print('mgl','joinxl','wtlog','get_time_str')
    pass
