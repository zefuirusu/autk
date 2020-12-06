#!/usr/bin/env python
# coding=utf-8
from autk.zhchart import ChartAccount
from autk.zhgl import Gele,Acct
class AuSample:
    '''
    无论是序时账还是余额表,发生额的名字都叫['借方','贷方'].
    '''
    def __init__(self,gl_object,chart_object):
        '''
        self.gl is an instance of class Gele and self.chart is an instance of class ChartAccount.
        '''
        self.gl=gl_object
        self.chart=chart_object
        return
    def getSample(self,inAcct,acquired_rate=0.81,drcrdesc=[r'借方',r'贷方']):
        theAcct=self.gl.filter(inAcct.accid,r'科目编码') # 系统导出的序时账/余额表里是"科目编号".
        acct_data=self.chart.getAcct(inAcct)
        from pandas import DataFrame,Series
        # acct_sum=DataFrame({drcrdesc[0]:acct_data[2],drcrdesc[1]:acct_data[3]},index=[inAcct.accid],columns=drcrdesc)
        acct_sum=Series([acct_data[2],acct_data[3]],name=inAcct.accid,index=drcrdesc)
        # acct_sum=theAcct[drcrdesc].sum(axis=0) # 被指定的科目借方贷方求和.这里要修改,要从余额表读取此数.
        sub_count=theAcct[drcrdesc].count(axis=0)
        target_sum=acct_sum*acquired_rate # 依据目标金额比例,确定目标累计合计金额.
        averAmount=acct_sum/sub_count # 平均每个样本的金额
        # start_nums=target_sum/averAmount # 计算初始样本容量,如acct_sum为0,start_nums会报错.
        print(target_sum)
        # print(target_sum[drcrdesc[0]])
        # print(target_sum['借方'])
        def loop_sample(dcr):
            '''
            dcr is one of ['借方','贷方']
            '''
            if acct_sum[dcr] ==0:
                print('%s :no need to sample.'%dcr)
                from pandas import DataFrame
                sloop=DataFrame([],columns=theAcct.columns)
                pass
            else:
                n_start=int(target_sum[dcr]/averAmount[dcr]/2)
                sloop=theAcct.nlargest(n=n_start,columns=[dcr],keep='last')
                sam_rate=sloop[dcr].sum(axis=0)/acct_sum[dcr]
                while sam_rate<acquired_rate:
                    n_start+=1
                    sloop=theAcct.nlargest(n=n_start,columns=[dcr],keep='last')
                    sam_rate=sloop[dcr].sum(axis=0)/acct_sum[dcr]
                    continue
                print(sam_rate)
            return sloop
        def drcr_sample():
            for i in drcrdesc:
                yield loop_sample(i)
        from pandas import concat
        final_sample=concat(drcr_sample(),axis=0,join='outer',ignore_index=True)
        final_sample=final_sample.reset_index(drop=True)
        return final_sample
    def multiSample(self,acctli_dir,savedir,acquired_rate=0.81,drcrdesc=[r'借方',r'贷方']):
        '''
        在savedir处的Excel文件必须事先创建.
        '''
        logdir='./sampleFailed.txt'
        from autk.logwriter import wtlog
        from openpyxl import load_workbook
        from pandas import ExcelWriter
        wb=load_workbook(savedir)
        wter=ExcelWriter(savedir,engine='openpyxl')
        wter.book=wb
        with open(acctli_dir,mode='r',encoding='utf-8') as f:
            acctli=f.readlines()
            acctli=''.join(acctli).split('\n')
            acctli.pop()
            pass
        wtlog('==multiSample==',logdir)
        for i in acctli:
            acct=Acct(self.chart.getna(i),i)
            try:
                m_sample=self.getSample(acct)
            except:
                print('sample for this account failed:')
                print(acct.accid,'\t',acct.name)
                wtlog('sample for this account failed:',logdir)
                lgline=acct.accid+'\t'+acct.name
                wtlog(lgline,logdir)
                pass
            if m_sample.shape[0]==0:
                wtlog('no sample for this account:',logdir)
                no_sample_line=acct.accid+'\t'+acct.name
                wtlog(no_sample_line,logdir)
                pass
            else:
                m_sample.to_excel(wter,sheet_name=str(acct.accid+acct.name))
                # yield list(m_sample.loc[:,'glid'].drop_duplicates())
                print(m_sample)
                wter.save()
        wter.close()
        return
