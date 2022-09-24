#!/usr/bin/env python
# coding=utf-8
'''
EntryRecord: a recording line in GL;
Side: derive from several EntryRecord, symbolizing Debit or Credit side of a JournalRecord;
JournalEntry: sum of debit side equals to credit side;
OppositeFinder: to find opposite account;
Acct: Account;
'''
from autk.reader.xlsht import XlSheet
from autk.mapper.map import MglMap
class SimpleEntry:
    def __init__(self):
        self.glid=None
        self.dr={}
        self.cr={}
    pass
class RowData:
    pass
class EntryRecord:
    '''
    A row in the general ledgers.
    '''
    def __init__(self,glid,row_series,mglmap=MglMap()):
        self.mglmap=mglmap
        self.glid=glid
        self.data=RowData()
        for k in self.mglmap.__dict__:
            setattr(self.data,k,row_series[k])
        pass
    def __str__(self):
        return 'EntryRecord:'+id(self)
    def show_none(self):
        for k in self.__dict__:
            v=self.__dict__[k]
            if v is None:
                print(k,':',v)
        pass
    def __parse_glid(self):
        pass
    def __parse_acct(self):
        pass
    def __parse_date(self):
        pass
    pass
class Side(XlSheet):
    def __init__(self,glid,df,mglmap,drcrdesc=['dr_amount','cr_amount'],credit=False):
        self.glid=glid
        self.data=df
        self.mglmap=mglmap
        self.drcrdesc=drcrdesc
        self.credit=credit
        self.accept_data(df)
        self.columns=list(self.data.columns)
        self.record_set=[]
        self.__parse_record()
        self.accid_list=list(self.data[self.mglmap.accid_col])
        pass
    def __str__(self):
        return 'EntrySide:'+self.glid
    def __parse_record(self):
        for i in self.data.iterrows():
            row_data=i[1]
            self.record_set.append(EntryRecord(self.glid,row_data,mglmap=MglMap()))
        pass
    def load_entry_record(self,df):
        for i in df.iterrows():
            row_data=i[1]
            enre=EntryRecord(row_data)
            self.record_set.append(enre)
    # @property
    # def accid_list(self):
    #     # print(self.glid,'credit:',self.credit)
    #     # print('side cols:',self.data.columns)
    #     # print('accid:',self.data[self.mglmap.accid_col].drop_duplicates(),'###')
    #     # print(self.data)
    #     return list(self.data[self.mglmap.accid_col])
    def get_amount(self,accid):
        if self.credit == False:
            return self.vlookup(accid, self.mglmap.accid_col, self.drcrdesc[0], if_regex=True, match_mode=True)
        else:
            return self.vlookup(accid, self.mglmap.accid_col, self.drcrdesc[1], if_regex=True, match_mode=True)
    def get_sum_amount(self,accid):
        from numpy import sum
        return sum(self.get_amount(accid))
    def sum(self):
        if self.credit == False:
            return self.data[self.drcrdesc].sum(axis=0)[0]
        else:
            return self.data[self.drcrdesc].sum(axis=0)[1]
    pass
class JournalEntry(XlSheet):
    def __init__(self,glid,df,mglmap,drcrdesc=['dr_amount','cr_amount']):
        self.glid=glid
        self.mglmap=mglmap
        self.accept_data(df)
        self.columns=list(self.data.columns)
        self.drcrdesc=drcrdesc
        self.dr_df=self.filter_num([[self.drcrdesc[0],'>',0]])
        self.cr_df=self.filter_num([[self.drcrdesc[1],'>',0]])
        self.debit=Side(self.glid,self.dr_df,self.mglmap,credit=False,drcrdesc=self.drcrdesc)
        self.credit=Side(self.glid,self.cr_df,self.mglmap,credit=True,drcrdesc=self.drcrdesc)
        self.accid_list=self.debit.accid_list+self.credit.accid_list
        self.single=self.__single()
        pass
    def __str__(self):
        return 'JournalEntry:'+self.glid
    def sum(self):
        if abs(self.debit.sum()-self.credit.sum())<0.004:
            return self.credit.sum()
        else:
            if abs(self.debit.sum()) < 0.004 or abs(self.credit.sum()) < 0.004:
                return 0.0
            else:
                return None
        pass
    # @property
    # def accid_list(self):
    #     return self.debit.accid_list+self.credit.accid_list
    def __single(self):
        if len(self.debit.accid_list)==1:
            # print('single flow')
            return True
        elif len(self.credit.accid_list)==1:
            return True
        else:
            # print('multi flow')
            return False
        pass
    pass
class OppositeFinder:
    def __init__(self,mgl_obj,drcrdesc=['dr_amount','cr_amount']):
        self.mgl=mgl_obj
        self._jr_set=[]
        self.drcrdesc=drcrdesc
        pass
    @property
    def data(self):
        if self.mgl.data is not None:
            return self.mgl.data
        else:
            self.mgl.load_raw_data()
            return self.mgl.data
    def __parse_jr_single(self,glid):
        self._jr_set.append(JournalEntry(glid,self.mgl.filter({'string':[[glid,self.mgl.key_name,True,True]]}),mglmap=self.mgl.mglmap,drcrdesc=self.drcrdesc))
        pass
    def __parse_jr(self):
        '''
        self.mgl.data must be loaded and 'glid' must be set.
        '''
        for glid in self.mgl.glid_list:
            self._jr_set.append(JournalEntry(glid,))
        
        pass
    def find_opposite(self):
        pass
    pass
'''
Below are related to Chart of Account.
'''
class Acct:
    '''
    Account in Chart of Account.
    '''
    def __init__(self):
        self.depth:int=0
        self.accid='6001'
        self.accna='Revenue'
        self.start_amount=None
        self.dr_amount=None
        self.cr_amount=None
        self.end_amount=None
        self.balance=False
        pass
    def is_balance(self):
        try:
            bal=(abs(self.start_amount+self.dr_amount-self.cr_amount-self.end_amount)<=0.004)
        except TypeError:
            bal=None
        return bal
    def accept_key_chart_row(self,key_chart_row):
        '''
        key_chart_row=['accid','accna','start_amount','dr_amount','cr_amount','end_amount']
        '''
        self.accid=key_chart_row[0]
        self.depth=int((len(str(self.accid))-4)/2)
        self.accna=key_chart_row[1]
        self.start_amount=key_chart_row[-4]
        self.dr_amount=key_chart_row[-3]
        self.cr_amount=key_chart_row[-2]
        self.end_amount=key_chart_row[-1]
        self.balance=self.is_balance()
        pass
    pass
if __name__=='__main__':
    pass
