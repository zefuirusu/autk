#!/usr/bin/env python
# coding=utf-8
'''
'''
import os
# import sys
# sys.path.append(os.curdir)
from autk import get_time_str,joinxl
# from autk.fileAssistant.skjoinxl import get_time_str,TarSheet,MultiRead,JoinExcel
# from skjoinxl import get_time_str,TarSheet,MultiRead,JoinExcel
if __name__=='__main__':
    testdir1='./bj1123-2202'
    testdir2='./bj1221-2241'
    testdirs=[
        './bj1123-2202',
        './bj1221-2241'
    ]
    savedir='./joinbooks'
    def get_tars(testdir):
        for i in os.listdir(testdir):
            i_fake=[os.path.abspath(os.path.join(testdir,i)),'Sheet1',0]
            ts=TarSheet(i_fake[0],i_fake[1],i_fake[2])
            yield ts
            continue
        pass
    tars=list(get_tars(testdirs[1]))
    # print(get_time_str(True))
    print('start_time:',get_time_str())
    # j1=JoinExcel()
    j1=joinxl()
    j1.load_sheets(tars)
    # j2=j1.join_to_sheet()
    j3=j1.join_to_book(split=False,write=False)
    # print(j2)
    print('end_time:',get_time_str())
    print(j3)
    pass
