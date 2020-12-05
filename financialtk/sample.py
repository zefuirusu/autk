#!/usr/bin/env python
# coding=utf-8
from autk.zhchart import ChartAccount
from autk.zhgl import Gele,Acct
class AuSample:
    def __init__(self,gl_object,chart_object):
        self.gl=gl_object
        self.chart=chart_object
        return
    def getSample(self,inAcct):
        theAcct=self.gl.filter(inAcct.accid,r'科目编号',acquired_rate=0.81,drcrdesc=[r'借方',r'贷方'])
        acct_li=self.char.getdata()
        from pandas import DataFrame
        acct_sum=DataFrame([acct_li[2],acct_li[3]],index=inAcct.accid,columns=drcrdesc)
        # acct_sum=theAcct[drcrdesc].sum(axis=0) # 被指定的科目借方贷方求和.这里要修改,要从余额表读取此数.
        sub_count=theAcct[drcrdesc].count(axis=0)
        averAmount=acct_sum/sub_count # 平均每个样本的金额
        target_sum=acct_sum*acquired_rate # 依据目标金额比例,确定目标累计合计金额.
        # start_nums=target_sum/averAmount # 计算初始样本容量,如acct_sum为0,start_nums会报错.
        return final_sample
