#!/usr/bin/env python
# coding=utf-8
class EntryRecord:
    '''
    Must be E-Audit output general ledgers of Excel.
    '''
    def __init__(self,df_iterrows_element):
        idli=[df_iterrows_element[1][0],df_iterrows_element[1][1],str(int(df_iterrows_element[1][2]))]
        # print(idli)
        if idli !=[0.0,0.0,'0']:
            self.glid=r'-'.join(idli)
            self.date=df_iterrows_element[1][0]
            self.scan=df_iterrows_element[1][3]
            self.accid=df_iterrows_element[1][4]
            self.accna=df_iterrows_element[1][5]
            self.dr_amount=df_iterrows_element[1][6]
            self.cr_amount=df_iterrows_element[1][7]
        else:
            # self.glid=None
            # self.date=None
            # self.scan=None
            # self.accid=None
            # self.accna=None
            # self.dr_amount=None
            # self.cr_amount=None
            pass
        pass
class JEntry:
    __slots__=('glid','date','scan','debit','credit') # static limit of S ?
    def __init__(self):
        self.glid="" # glid是序时账唯一索引,即主键
        self.date="" # 记账日期
        self.scan="" # 摘要
        self.debit=[
            {
                accid:"",
                accna:"",
                amount:""
            },
            {
                accid:"",
                accna:"",
                amount:""
            }
        ]
        self.credit=[
            {
                accid:"",
                accna:"",
                amount:""
            },
            {
                accid:"",
                accna:"",
                amount:""
            }
        ]
        pass
