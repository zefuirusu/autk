#!/usr/bin/env python
# coding=utf-8
import re
import os
import datetime
import threading
from autk import wtlog,get_time_info
class Walkder:
    def __init__(self,item,search_dir=os.path.abspath(os.curdir),match=False):
        self.search_dir=search_dir
        self.match=match
        self.item=item
        self.regitem=re.compile(self.item)
        self.resu_files=None
        self.resu_dirs=None
        pass
    def one_match(self,compare_target):
        if self.match==False:
            return re.search(self.regitem,compare_target)
        else:
            return re.match(self.regitem,compare_target)
        pass
    def get_files(self):
        for i,j,k in os.walk(self.search_dir):
            for file_name in k:
                if self.one_match(file_name) is not None:
                    yield os.path.abspath(os.path.join(i,file_name))
        pass
    def get_dirs(self):
        for i,j,k in os.walk(self.search_dir):
            for file_path in j:
                if self.one_match(file_path) is not None:
                    yield os.path.abspath(file_path)
        pass
    def start_search(self):
        def th1():
            self.resu_files=self.get_files()
        def th2():
            self.resu_dirs=self.get_dirs()
        t1=threading.Thread(target=th1)
        t2=threading.Thread(target=th2)
        t1.start()
        t1.join()
        t2.start()
        t2.join()
        pass
    pass
def skfind(item,search_dir=os.path.abspath(os.curdir),match=False):
    # print('start time:',get_time_info())
    print('start time:',datetime.datetime.now())
    w1=Walkder(item=item,search_dir=search_dir,match=match)
    w1.start_search()
    resu=[list(w1.resu_files),list(w1.resu_dirs)]
    print('---files:---')
    for i in resu[0]:
        print(i)
    print('---folders:---')
    for j in resu[1]:
        print((j))
    # print('end time:',get_time_info())
    print('end time:',datetime.datetime.now())
    return resu
