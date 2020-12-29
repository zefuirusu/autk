#!/usr/bin/env python
# coding=utf-8
class EntryRecord:
    '''
    Input file must be E-Audit output general ledgers of Excel.
    ['凭证日期', '字', '号', '摘要', '科目编号', '科目全路径', '借方发生金额', '贷方发生金额', '汇率', '外币金额', '外币名称', '数量额', '单价', '计量单位', '核算编号', '核算名称']
    '''
    def __init__(self,df_iterrows_element,glid_cols=[0,1,2]):
        def transType(element):
            if isinstance(element,float):
                element=str(int(element))
            elif isinstance(element,int):
                element=str(element)
            elif isinstance(element,str):
                element=element
            else:
                element=str(element)
            return element
        idli=[df_iterrows_element[1][glid_cols[0]],df_iterrows_element[1][glid_cols[1]],str(int(df_iterrows_element[1][glid_cols[2]]))]
        idli=map(transType,idli)
        idli=list(idli)
        # idli=[df_iterrows_element[1][0],df_iterrows_element[1][1],str(int(df_iterrows_element[1][2]))]
        # idli=[]
        # for i in glid_cols:
        #     part_glid=df_iterrows_element[1][i]
        #     # print(type(part_glid))
        #     if isinstance(part_glid,float):
        #     # if type(part_glid)==type('float'):
        #         part_glid=str(int(part_glid))
        #     else:
        #         pass
        #     idli.append(part_glid)
        # print(idli)
        if idli !=['0','0','0']:
        # if type(idli[1]) != '0':
            self.glid=r'-'.join(idli)
            self.date=df_iterrows_element[1][0]
            self.month=self.date[5:7]
            self.accid=df_iterrows_element[1][4]
            self.top_accid=self.accid[0:4]
            self.dr_amount=df_iterrows_element[1][6]
            self.cr_amount=df_iterrows_element[1][7]
            self.accna=df_iterrows_element[1][5]
            self.scan=df_iterrows_element[1][3]
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
    '''
    Journal Entry.
    '''
    # __slots__=('glid','date','scan','debit','credit') # static limit of S ?
    def __init__(self,glid,one_entry_df):
        dr_sum=one_entry_df['dr_amount'].sum(axis=0)
        cr_sum=one_entry_df['cr_amount'].sum(axis=0)
        if dr_sum-cr_sum>=-0.009 and dr_sum-cr_sum<=0.009:
            print('OK! Debit = Credit!')
        else:
            print('Woc! Dr and Cr not balenced!')
        self.glid=glid # glid is the unique id of JEntry.
        self.date=self.glid[0:10] # date of the Journal Entry Recording.
        self.scan=one_entry_df['scan'] # summary or comments of each EntryRecord.
        self.debit=[]
        self.credit=[]
        for i in one_entry_df.iterrows():
            er=i[1]
            if er.cr_amount==0.00:
                self.debit.append({"accid":er.accid,"amount":er.dr_amount,"accna":er.accna})
            elif er.dr_amount==0.00: # er.dr_amount==0:
                self.credit.append({"accid":er.accid,"amount":er.cr_amount,"accna":er.accna})
            pass
        # self.debit=[
        #     {
        #         "accid":"",
        #         "accna":"",
        #         "amount":""
        #     },
        #     {
        #         "accid":"",
        #         "accna":"",
        #         "amount":""
        #     }
        # ]
        # self.credit=[
        #     {
        #         "accid":"",
        #         "accna":"",
        #         "amount":""
        #     },
        #     {
        #         "accid":"",
        #         "accna":"",
        #         "amount":""
        #     }
        # ]
        pass
