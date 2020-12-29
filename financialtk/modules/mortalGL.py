#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
形式上更加一般，更加通用的GL类。
'''
import pandas as pd
class GL(object):
    '''
    GL is short for General Ledger.
    'gldir': general ledger directory.
    'shtna':sheet name.
    '''
    def __init__(self,gldir=r'',shtna=r'',indf=None):
        '''
        'gldir': general ledger directory.
        'shtna':sheet name.
        '''
        self.gldir=gldir
        self.shtna=shtna
        self.indf=indf
        self.data=pd.read_excel(gldir,sheet_name=shtna)
        print(self.data.columns)
        pass
    #
    def sample(self,acct_id,filterIdCol,acquired_rate=0.31,drcrdesc=[r'借方',r'贷方']):
        '''
        'acct_id',short for 'account id number', can be regular expression to filter in the column of 'filterIdCol'.
        'acquired_rate' is the accumulate sum rate that is required by the manager.
        'dr' is short for Debit while 'cr' for credit.
        Finally return a pandas.DataFrame as a sample.
        '''
        if self.indf==None:
            gl=pd.read_excel(self.gldir,sheet_name=self.shtna)
        else:
            gl=pd.read_excel(self.gldir,sheet_name=self.shtna)
            # gl=self.indf
        # regitem=r'^'+str(acct_id)+r'.*'
        regitem=str(acct_id)
        theAcct=gl.filter(regitem,filterIdCol)
        print('this account shape:',theAcct.shape)
        # theAcct.to_excel(r'D:\skandha\a-Project\zhongTang\广东中糖贸易发展有限公司\余额表和序时账\filterAcct-test.xlsx')
        acct_sum=theAcct[drcrdesc].sum(axis=0)
        sub_count=theAcct[drcrdesc].count(axis=0)
        averAmount=acct_sum/sub_count
        target_sum=acct_sum*acquired_rate
        start_nums=target_sum/averAmount
        #
        # theAcct=theAcct.drop_duplicates()
        # print(theAcct.shape)
        #
        n_dr_start=int(start_nums[0]/2)
        n_dr_start=1
        dr_sample=theAcct.nlargest(n=n_dr_start,columns=[drcrdesc[0]],keep='last')
        # print('dr sample sum:',dr_sample[drcrdesc].sum(axis=0))
        dr_sam_rate=dr_sample[drcrdesc[0]].sum(axis=0)/acct_sum[0]
        while dr_sam_rate<acquired_rate:
            # print('current dr sum:',dr_sample[drcrdesc[0]].sum(axis=0))
            # print('target dr sum:',acquired_rate*acct_sum[0])
            # print('current dr sum rate:',dr_sam_rate)
            n_dr_start+=1
            dr_sample=theAcct.nlargest(n=n_dr_start,columns=[drcrdesc[0]],keep='last')
            dr_sam_rate=dr_sample[drcrdesc[0]].sum(axis=0)/acct_sum[0]
        n_cr_start=int(start_nums[1]/2)
        n_cr_start=1
        cr_sample=theAcct.nlargest(n=n_cr_start,columns=[drcrdesc[1]],keep='last')
        # print('cr sample sum:',cr_sample[drcrdesc].sum(axis=0))
        cr_sam_rate=cr_sample[drcrdesc[1]].sum(axis=0)/acct_sum[1]
        while cr_sam_rate<acquired_rate:
            # print('current cr sum:',cr_sample[drcrdesc[1]].sum(axis=0))
            # print('target cr sum:',acquired_rate*acct_sum[1])
            # print('current cr sum rate:',cr_sam_rate)
            n_cr_start+=1
            cr_sample=theAcct.nlargest(n=n_cr_start,columns=[drcrdesc[1]],keep='last')
            cr_sam_rate=cr_sample[drcrdesc[1]].sum(axis=0)/acct_sum[1]
        final_sample=pd.concat([dr_sample,cr_sample],axis=0,join='outer',ignore_index=True)
        final_sample=final_sample.reset_index(drop=True)
        print('total account sum:')
        print(acct_sum)
        sample_sum=final_sample[drcrdesc].sum(axis=0)
        print('sample shape:')
        print(final_sample.shape)
        print('sample sum:')
        print(sample_sum)
        print('sampling accsum rate:')
        print(sample_sum/acct_sum)
        return final_sample
    def getAccGl(self,accid):
        regitem=str(accid)
        gl=self.data
        km=gl.filter(accid,r'科目编码')
        idli=list(km['glid'].drop_duplicates())
        def itersearch(idli):
            for i in idli:
                yield gl.filter(i,'glid')
        resu=pd.concat(itersearch(idli),axis=0,join='outer')
        return resu

#
