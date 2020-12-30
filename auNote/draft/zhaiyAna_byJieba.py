#!/usr/bin/env python
# coding=utf-8
from pandas import read_excel
import re
from autk.financialtk.logwriter import wtlog
def get_zhaiy(indir):
    d=read_excel(indir,header=3)
    print(d.columns)
    z=d['摘要']
    z=list(z)
    return z
def test_thulac(zhaiyao):
    import thulac
    thu1=thulac.thulac(seg_only=True)
    for i in zhaiyao:
        t1=thu1.cut(i,text=True)
        t2=t1.split()
        print(t2)
    return
def test_jieba(zhaiyao,logdir='./jieba_log.txt'):
    import jieba
    jieba.enable_paddle()
    word_count={}
    for i in zhaiyao:
        t1=jieba.cut(i,use_paddle=True)
        for j in t1:
            word_count[j]=word_count.get(j,0)+1
            # print(j)
            pass
    # print(word_count)
    # for i in word_count:
    #     print(i,'\t',word_count[i])
    from pandas import Series
    s=Series(word_count)
    s=s.sort_values(ascending=False)
    for i in s.index:
        print(i,'\t',s[i])
        logline=str(i)+'\t'+str(s[i])
        wtlog(logline,logdir)
    # print(s)
    return # word_count
if __name__=='__main__':
    from threading import Thread
    testdir='../bori/testSample/data/testGL-2020-930.xlsx'
    # th1=Thread(test_thulac(get_zhaiy(testdir)))
    # th1.start()
    th2=Thread(test_jieba(get_zhaiy(testdir)))
    th2.start()
    pass
