#!/usr/bin/env python
# coding=utf-8
class EntryRecord:
    def __init__(self,df_iterrows_element,glid_cols=[0,1,2]):
        self.index=list(df_iterrows_element[1].index)
        from numpy import nan
        def transType(element):
            '''
            transfer an float/integer object into string.
            '''
            if element is nan:
            # if isinstance(element,type(nan)):
                print('woc!!! %s is nan!'%element )
                element=str(int(0))
            else:
                if isinstance(element,float):
                    element=str(int(element))
                elif isinstance(element,int):
                    element=str(element)
                elif isinstance(element,str):
                    element=element
            return element
        def iterate_id(ids):
            for i in ids:
                yield i
                continue
            pass
        def re_match(in_string,what):
            import re
            what=transType(what)
            regex_item=re.compile(in_string)
            return re.match(regex_item,what)
        def get_id_list():
            id_list=[]
            for i in df_iterrows_element[1].index:
                series_element=df_iterrows_element[1][i]
                series_element_index=transType(i)
                if re_match('.*日期.*',series_element_index) != None: 
                    id_list.append(series_element)
                elif re_match('.*字.*',series_element_index) != None:
                    id_list.append(series_element)
                elif re_match('.*号.*',series_element_index) != None: 
                    id_list.append(series_element)
                continue
            return id_list
        def start_init():
            for i in df_iterrows_element[1].index:
                series_element=df_iterrows_element[1][i]
                series_element_index=transType(i)
                if re_match('.*借方?.*',series_element_index) != None:
                    self.dr_amount=series_element
                elif re_match('.*贷方?.*',series_element_index) != None:
                    self.cr_amount=series_element
                elif re_match(r'.*科目编[号,码].*',series_element_index) != None:
                    self.accid=transType(series_element)
                    self.top_accid=self.accid[0:4]
                elif re_match(r'.*科目(.*路径.*|.*名称.*).*',series_element_index) != None:
                    self.accna=series_element
                elif re_match('.*对[方,应]科目.*',series_element_index) != None:
                    self.opposite=series_element
                elif re_match('.*日期.*',series_element_index) != None:
                    self.date=series_element
                elif re_match('.*月.*',series_element_index) != None:
                    self.month=series_element
                elif re_match(r'.*(摘要|文本).*',series_element_index) != None:
                    self.scan=series_element
                else:
                    pass
                continue
            pass
        id_list=get_id_list()
        if 'glid' in self.index:
            self.glid=df_iterrows_element[1]['glid']
            start_init()
        else:
            if nan not in id_list:
                self.glid=r'-'.join(map(transType,id_list))
                start_init()
            else:
                print('entry record initialize failed.')
        pass
    def getdata(self):
        from pandas import DataFrame
        return [self.glid,DataFrame(self.__dict__)]
    pass
class JEntry:
    '''
    Journal Entry.
    '''
    # __slots__=('glid','date','scan','debit','credit') # static limit of S ?
    def __init__(self,glid,one_entry_df):
        dr_sum=one_entry_df['dr_amount'].sum(axis=0)
        dr_sum=float(dr_sum)
        cr_sum=one_entry_df['cr_amount'].sum(axis=0)
        cr_sum=float(cr_sum)
        if dr_sum-cr_sum>=-0.009 and dr_sum-cr_sum<=0.009:
            pass
            # print('OK! Debit = Credit!')
        else:
            print('%s ! Dr/Cr not balenced!'%glid)
            # print('dr/cr:',dr_sum,'/',cr_sum)
            pass
        self.glid=glid # glid is the unique id of JEntry.
        self.date=self.glid[0:10] # date of the Journal Entry Recording.
        scan=one_entry_df['scan']
        if len(scan.drop_duplicates()) != 1:
            self.scan=list(scan)
        else:
            self.scan=list(scan.drop_duplicates())[0]# summary or comments of each EntryRecord.

        self.debit=[]
        self.credit=[]
        for i in one_entry_df.iterrows():
            er=i[1]
            if er.cr_amount==0.00:
                self.debit.append({"accid":er.accid,"amount":er.dr_amount,"accna":er.accna})
            elif er.dr_amount==0.00: # er.dr_amount==0:
                self.credit.append({"accid":er.accid,"amount":er.cr_amount,"accna":er.accna})
            pass
        pass
class MGL:
    '''
    Mortal General Ledger, a template class of General Ledger.
    '''
    def __init__(self,fpath,shtna,title=0):
        '''
        Three key elements of an General Ledger File is the path, sheet name and the column title location.
        '''
        self.fpath=fpath
        self.shtna=shtna
        self.title=title
        self.data=None
        pass
    def get_cols(self):
        if self.data != None:
            return self.data.columns
        else:
            return None
    def load_df(self,in_df):
        self.data=in_df
        pass
    def get_raw_data(self):
        from pandas import read_excel
        self.data=read_excel(self.fpath,sheet_name=self.shtna,header=self.title,engine='openpyxl')
        pass
    def iterate_record(self):
        self.get_raw_data()
        for i in self.data.iterrows():
            yield EntryRecorb(i)
        pass
    def filter(self,regitem,label=r'',match=False):
        '''
        Filter the specific column of the table by regular expression.
        '''
        import re
        self.get_raw_data()
        indf=self.data
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
