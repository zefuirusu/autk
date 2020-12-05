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
        theAcct=self.gl.filter(inAcct.accid,r'glid',acquired_rate=0.81,drcrdesc=[r'借方',r'贷方'])
        acct_li=self.char.getdata()
        from pandas import DataFrame
        acct_sum=DataFrame([acct_li[2],acct_li[3]],index=inAcct.accid,columns=drcrdesc)
        # acct_sum=theAcct[drcrdesc].sum(axis=0) # 被指定的科目借方贷方求和.这里要修改,要从余额表读取此数.
        sub_count=theAcct[drcrdesc].count(axis=0)
        averAmount=acct_sum/sub_count # 平均每个样本的金额
        target_sum=acct_sum*acquired_rate # 依据目标金额比例,确定目标累计合计金额.
        # start_nums=target_sum/averAmount # 计算初始样本容量,如acct_sum为0,start_nums会报错.
        def get_dr_sample():
            # 开始抽借方样本:
            n_dr_start=int(target_sum[0]/averAmount[0]/2)
            # n_dr_start=1
            dr_sample=theAcct.nlargest(n=n_dr_start,columns=[drcrdesc[0]],keep='last')
            # print('dr sample sum:',dr_sample[drcrdesc].sum(axis=0))
            dr_sam_rate=dr_sample[drcrdesc[0]].sum(axis=0)/acct_sum[0]
            while dr_sam_rate<acquired_rate:
                # n_dr_start+=1
                dr_sample=theAcct.nlargest(n=n_dr_start,columns=[drcrdesc[0]],keep='last')
                dr_sam_rate=dr_sample[drcrdesc[0]].sum(axis=0)/acct_sum[0]
                continue
            return dr_sample
        def get_cr_sample():
            # 开始抽贷方样本:
            n_dr_start=int(target_sum[1]/averAmount[1]/2)
            # n_cr_start=1
            cr_sample=theAcct.nlargest(n=n_cr_start,columns=[drcrdesc[1]],keep='last')
            cr_sam_rate=cr_sample[drcrdesc[1]].sum(axis=0)/acct_sum[1]
            while cr_sam_rate<acquired_rate:
                n_cr_start+=1
                cr_sample=theAcct.nlargest(n=n_cr_start,columns=[drcrdesc[1]],keep='last')
                cr_sam_rate=cr_sample[drcrdesc[1]].sum(axis=0)/acct_sum[1]
                continue
        return cr_sample
        # 将借方贷方样本拼接在一起:
        if acct_sum[0] !=0: 
            dr=get_dr_sample()
            pass
        else:
            dr=DataFrame([],columns=theAcct.columns)
            pass
        if acct_sum[1] !=0:
            cr=get_cr_sample()
            pass
        else:
            cr=DataFrame([],columns=theAcct.columns)
            pass
        from pandas import concat
        final_sample=concat([dr,cr],axis=0,join='outer',ignore_index=True)
        final_sample=final_sample.reset_index(drop=True)
        return final_sample
