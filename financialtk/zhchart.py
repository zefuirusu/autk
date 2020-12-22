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
        '''
        Get all data of the input Chart of Account from the Excel file.
        '''
        from pandas import read_excel
        return read_excel(self.path,sheet_name=self.sheetname,header=self.title,engine='openpyxl')
    def getAcct(self,account):
        '''
        Get Account Data.
        "account" is an instance of class Acct, with attributes of name and accid.
        '''
        data=self.getdata()
        acctData=data[data[self.cols[1]]==account.accid]
        start_balance=acctData.loc[:,self.cols[5]].sum(axis=0)
        dr_amount=acctData.loc[:,self.cols[6]].sum(axis=0)
        cr_amount=acctData.loc[:,self.cols[7]].sum(axis=0)
        end_balance=acctData.loc[:,self.cols[8]].sum(axis=0)
        acctDatali=[account.accid,start_balance,dr_amount,cr_amount,end_balance]
        return acctDatali # acctData
    def getid(self,acct_name):
        data=self.getdata()
        data=data.iloc[:,[1,2]]
        data=data.drop_duplicates()
        data=dict(zip(data.iloc[:,1],data.iloc[:,0]))
        resu=data[acct_name]
        return resu
    def getna(self,acct_id):
        data=self.getdata()
        data=data.iloc[:,[1,2]]
        data=data.drop_duplicates()
        data=dict(zip(data.iloc[:,0],data.iloc[:,1]))
        resu=data[acct_id]
        return resu


