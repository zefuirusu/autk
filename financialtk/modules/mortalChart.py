#!/usr/bin/env python
# coding=utf-8
import re
from numpy import nan
from pandas import read_excel,DataFrame,concat
class Acct:
    def __init__(self,accid=r'6001',accna='MainRevenue'):
        '''
        class of Account.
        Acct is short for Account, with two main attributes, 'name' and 'accid'.
        parameters:
            accid: Account ID Number. The most important attribute of class Acct.
            accna: Account Name.
        '''
        self.accid=str(accid) # id number of the account, Account ID.
        self.top_accid=self.accid[0:4]
        self.accna=name # name of the account, Account Name
        self.start_balance=None
        self.dr_amount=None
        self.cr_amount=None
        self.end_balance=None
        pass
    pass
class ChartAccount:
    '''
    Chart of Account is a table where you can get reference from Account ID to Account Name.
    '''
    def __init__(self,fpath,shtna,title=0):
        self.fpath=fpath
        self.shtna=shtna
        self.title=title
        self.raw_data=None
        self.data=None
        self.cols=None
        pass
    def get_cols(self):
        if self.cols == None:
            self.cols=list(read_excel(self.fpath,sheet_name=self.shtna,header=self.title,engine='openpyxl').columns)
        else:
            pass
        return self.cols
    def get_raw_data(self):
        self.raw_data=read_excel(self.fpath,sheet_name=self.shtna,header=self.title,engine='openpyxl')
        return self.raw_data
    def filter(self,regitem,label=r'',match=False):
        '''
        Filter the specific column of the table by regular expression.
        '''
        import re
        self.get_raw_data()
        indf=self.raw_data
        reg=re.compile(regitem)
        fli=[]
        for i in list(indf[label].drop_duplicates()):
            if match==False:
                b=re.search(reg,str(i))
            else:
                b=re.match(reg,str(i))
            if b != None:
                fli.append(i)
            else:
                pass
        from pandas import DataFrame,concat
        ftableli=[]
        for j in fli:
            ftable_fake=indf[indf[label]==j]
            ftableli.append(ftable_fake)
            continue
        if len(ftableli)==0:
            ftable=DataFrame([],index=[],columns=self.getcol())
            pass
        else:
            ftable=concat(ftableli,axis=0,join='outer')
        return ftable
