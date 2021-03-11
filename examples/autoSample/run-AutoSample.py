#!/usr/bin/env python
# coding=utf-8
# import sys
# sys.path.append('../../../../autk')
import threading
from autk.financialtk.zhtk.zhchart import ChartAccount,Acct
from autk.financialtk.zhtk.zhgl import Gele
from autk.financialtk.routines.sample import AuSample

def start_sample(gldir,chartdir,savedir,acctli_dir,logdir):
    auto_sample=AuSample(gldir,chartdir,savedir,acctli_dir=acctli_dir,logdir=logdir)
    auto_sample.multiSample()
    pass
class SampleThread(threading.Thread):
    def __init__(self,gldir,chartdir,savedir,acctli_dir,logdir):
        self.gldir=gldir
        self.chartdir=chartdir
        self.savedir=savedir
        self.acctli_dir=acctli_dir
        self.logdir=logdir
        threading.Thread.__init__(self)
        pass
    def run(self):
        # auto_sample=AuSample(self.gldir,self.chartdir,self.savedir,acctli_dir=self.acctli_dir,logdir=self.logdir,drcrdesc=['借方发生','贷方发生'])
        auto_sample=AuSample(self.gldir,self.chartdir,self.savedir,acctli_dir=self.acctli_dir,logdir=self.logdir,drcrdesc=['借方','贷方'])
        auto_sample.multiSample()
        pass
# start testing:
def bj_sample():
    s1=AuSample(gl1,cht1,sdir1,acctli_dir=acctlidir1,logdir=lg1)
    s1.multiSample()
    return
def xa_sample():
    s2=AuSample(gl2,cht2,sdir2,acctli_dir=acctlidir2,logdir=lg2)
    s2.multiSample()
    return
if __name__=='__main__':
    gl1=Gele('./inputData/北京序时账-202001-10.xlsx',shtna='bjgl10',title=0)
    gl2=Gele('./inputData/西安序时账-202001-10.xlsx',shtna='xagl10',title=0)

    cht1=ChartAccount('./inputData/北京余额表.xlsx',title=3)
    cht2=ChartAccount('./inputData/西安余额表.xlsx',title=3)
    print(cht2.cols)

    sdir1='./outSample/bj-Multi.xlsx'
    sdir2='./outSample/xa-Multi.xlsx'

    acctlidir1='./acctlidir/bj-acctli.txt'
    acctlidir2='./acctlidir/xa-acctli.txt'

    lg1='./logfiles/bj_sam_log.txt'
    lg2='./logfiles/xa_sam_log.txt'

    # s1=SampleThread(gl1,cht1,sdir1,acctli_dir=acctlidir1,logdir=lg1)
    # s1.start()
    s2=SampleThread(gl2,cht2,sdir2,acctli_dir=acctlidir2,logdir=lg2)
    s2.start()
    pass
