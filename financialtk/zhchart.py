#!/usr/bin/env python
# coding=utf-8
'''
ChartAccount是对Chart of Account的抽象.会计科目表.
'''
from autk.zhgl import Acct
class ChartAccount: # Chart of Account
    '''
    Chart of Account is a table where you can get reference from Account ID to Account Name.
    Chart of Account,会计科目表,主要有两个作用,一是索引account_name和account_id,二是知晓各科目余额.
    默认格式为从E审通导出的Excel.
    '''
    def __init__(self,chadir,shtna='表页-1',title=3):
        self.path=chadir
        self.sheetname=shtna
        self.title=title
        self.cols=['核', '科目编号', '科目名称', '数据类型', '科目方向', '期初', '借方发生', '贷方发生', '期末']
        pass
    def getdata(self):
        from pandas import read_excel
        return read_excel(self.path,sheet_name=self.sheetname,header=self.title)
    def getAcct(self,account):
        '''
        "account" is an instance of class Acct, with attributes of name and accid.
        '''
        data=self.getdata()
        acctData=data[data[self.cols[1]]==account.accid]
        start_balance=data.loc[:,self.cols[5]].sum(axis=0)
        dr_amount=data.loc[:,self.cols[6]].sum(axis=0)
        cr_amount=data.loc[:,self.cols[7]].sum(axis=0)
        end_balance=data.loc[:,self.cols[8]].sum(axis=0)
        acctDatali=[account.accid,start_balance,dr_amount,cr_amount,end_balance]
        return acctDatali # acctData
    def getid(self,acct_name):
        pass
    def getna(acct_id):
        pass


