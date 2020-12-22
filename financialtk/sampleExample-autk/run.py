#!/usr/bin/env python
# coding=utf-8
from autk.zhchart import ChartAccount
from autk.zhgl import Gele,Acct
from autk.sample import AuSample

acctlidir1='./acctlidir/bj-acctli.txt'
acctlidir2='./acctlidir/xa-acctli.txt'

sdir1='./outSample/bj-Multi.xlsx'
sdir2='./outSample/xa-Multi.xlsx'

cht1=ChartAccount('./inputData/北京余额表.xlsx')
cht2=ChartAccount('./inputData/西安余额表.xlsx')

gl1=Gele('./inputData/北京序时账-202001-10.xlsx',shtna='bjgl10',title=0)
gl2=Gele('./inputData/西安序时账-202001-10.xlsx',shtna='xagl10',title=0)

lg1='./s_log/bj_sam_log.txt'
lg2='./s_log/xa_sam_log.txt'
# start testing:
def bj_sample():
    s1=AuSample(gl1,cht1,sdir1,acctli_dir=acctlidir1,logdir=lg1)
    s1.multiSample()
    return
# 到这里了:Name: 150142
def xa_sample():
    s2=AuSample(gl2,cht2,sdir2,acctli_dir=acctlidir2,logdir=lg2)
    s2.multiSample()
    return
if __name__=='__main__':
    import threading
    t1=threading.Thread(target=bj_sample)
    t2=threading.Thread(target=xa_sample)
    t1.start()
    t2.start()
    pass
