#!/usr/bin/env python
# coding=utf-8
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
