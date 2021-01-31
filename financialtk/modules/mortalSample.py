#!/usr/bin/env python
# coding=utf-8
'''
Automatic sampling.
Mortal Sampling class using mortalGL.
'''
import os
import re
import threading
class Strategy:
    def __init__(self,acct_li,gl_book_path,chart_path):
        def trans_regitem(inlist):
            for i in inlist:
                yield re.compile(str(r'^'+i+r'.*'))
        self.cash_acct_item=r'^1002.*'
        self.acct_li=acct_li
        self.acct_reg_li=trans_regitem(acct_li)
        self.acct_dict=dict(zip(self.acct_li,self.acct_reg_li))
        self.gl_book_path=gl_book_path
        self.gl_shtna='Sheet1'
        self.chart_path=chart_path
        pass
class Sample:
    def __init__(self,strategy):
        self.strategy=strategy
        self.cashdata=None
        # self.curdata=None
        from autk.financialtk.modules.mortalGL import MGL
        self.mgl=MGL(self.strategy.gl_book_path,self.strategy.gl_shtna)
        self.get_cash()
        self.mgl.load_df(self.cashdata)
        # print('mgl_obj:',self.mgl.data.shape)
        # print('strategy_obj:',self.strategy.__dict__)
        pass
    def get_cash(self):
        self.cashdata=self.mgl.filter(self.strategy.cash_acct_item,'科目编码')
        return
        pass
    def single_filter(self,acct_reg):
        # self.get_cash()
        # self.mgl.load_df(self.cashdata)
        return self.mgl.filter(acct_reg,'科目编码')
        pass
    def get_relevant_data(self):
        '''
        Get entry records of relevant account id.
        '''
        # self.get_cash()
        # self.mgl.load_df(self.cashdata)
        for i in self.strategy.acct_dict:
            name=i
            regitem=self.strategy.acct_dict[i]
            # d=self.single_filter(i)
            # print(d)
            yield [name,self.single_filter(regitem)]
            pass
        # print(self.mgl.filter(self.strategy.cash_acct_item,'科目编码'))
        pass
class WtOnce(threading.Thread):
    def __init__(self,accid,savedir,strategy_obj,sample_obj):
        self.sample_obj=sample_obj
        # self.sample_obj=Sample(strategy_obj)
        self.accid=accid
        self.savedir=savedir
        self.savename=r'sample-for-'+strategy_obj.gl_book_path.split(os.sep)[-1]
        self.savepath=os.path.join(self.savedir,self.savename)
        from pandas import ExcelWriter
        self.wter=ExcelWriter(self.savepath,engine='openpyxl')
        threading.Thread.__init__(self,name=accid)
        pass
    def run(self):
        # print('='*5)
        print('sheet writing:',threading.current_thread().name)
        d=self.sample_obj.single_filter(self.accid)
        d.to_excel(self.wter,sheet_name=self.accid)
        self.wter.save()
        print('sheet written:',self.accid)
        # print('-'*5)
        pass
def start_sample(savedir,strategy_obj):
    s1=Sample(strategy_obj) 
    for i in strategy_obj.acct_li:
        t=WtOnce(i,savedir,strategy_obj,s1)
        t.start()
        continue
    pass
if __name__=='__main__':
    testxlpath='../xlGL/81-赫兹上海.xlsx'
    chpath='../xlGL/chart所有主体-两年度-普通余额表.xlsx'
    acct_li=[
        '2202',
        '1123',
        '1221',
        '2241'
    ]
    savedir='../output'
    stg1=Strategy(acct_li,testxlpath,chpath)
    s1=Sample(stg1)
    # start_sample(savedir,stg1)
    # for i in acct_li:
    #     t=WtOnce(i,savedir,stg1)
    #     t.start()
    start_sample(savedir,stg1)
    pass
