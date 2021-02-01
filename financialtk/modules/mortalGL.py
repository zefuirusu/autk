#!/usr/bin/env python
# coding=utf-8
import re
from numpy import nan
from pandas import read_excel,DataFrame,concat
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
# class JsonEntryRecord(EntryRecord):
#     def __init__(self,df_iterrows_element,glid_cols=[0,1,2]):
#         pass
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
        self.sample_data=None
        pass
    def load_df(self,in_df):
        self.data=in_df
        pass
    def get_raw_data(self):
        '''
        get original DataFrame data.
        '''
        from pandas import read_excel
        self.data=read_excel(self.fpath,sheet_name=self.shtna,header=self.title,engine='openpyxl')
        return self.data
        pass
    def set_glid(self,glid_index):
        if self.data is None:
            print('You need load data first!')
            self.get_raw_data()
            pass
        else:
            def get_glid_li():
                for i in self.data.iterrows():
                    row=i[1]
                    glid=[]
                    for j in glid_index:
                        a_index=row[j]
                        a_index=str(a_index)
                        glid.append(a_index)
                    glid='-'.join(glid)
                    # i['glid']=glid
                    d=dict(row)
                    d['glid']=glid
                    # yield {glid:row}
                    yield d
            data=DataFrame(get_glid_li())
            self.load_df(data)
            print(self.data.shape)
            return data
            pass
        pass
    def get_cols(self):
        if self.data is not None:
            return list(self.data.columns)
        else:
            self.get_raw_data()
            return list(self.data.columns)
    def iterate_jsfile(self,jspath):
        import re
        import json
        # from pandas import Series,concat
        with open(jspath,mode='r',encoding='utf-8') as f:
            jslines=f.readlines()
            pass
        for i in jslines:
            js_record=re.sub(re.compile(r'\s*$'),'',i)
            yield json.loads(js_record,encoding='utf-8')
        pass
    def iterate_record(self):
        '''
        iterate rows of self.data(DataFrame) and yield data of EntryRecord object.
        '''
        # self.get_raw_data()
        if self.data is not None:
            for i in self.data.iterrows():
                yield EntryRecord(i)
                continue
            pass
        else:
            self.get_raw_data()
            for i in self.data.iterrows():
                yield EntryRecord(i)
                continue
            pass
        pass
    def iterate_json_record(self):
        '''
        iterate rows of self.data(DataFrame) and yield data of json(python dict) of format.
        '''
        # self.get_raw_data()
        if self.data is not None:
            for i in self.data.iterrows():
                yield dict(i[1])
                continue
            pass
        else:
            self.get_raw_data()
            for i in self.data.iterrows():
                yield dict(i[1])
                continue
            pass
    def iterate_filter(self,regitem,label=r'',match=False):
        '''
        iterate row_data of self.data and yield.
        '''
        import re
        def start_iterate():
            reg=re.compile(regitem)
            indf=self.data
            for i in self.data.iterrows():
                row_index=i[0]
                row_data=i[1]
                key_str=str(row_data[label])
                if match==False:
                    b=re.search(reg,key_str)
                else:
                    b=re.match(reg,key_str)
                if b is not None:
                    # glid=r'-'.join([row_data['账簿编码'],row_data['期间年'],row_data['期间月'],row_data['凭证编码']])
                    # yield {glid,row_data}
                    yield row_data
                    pass
                else:
                    # yield None
                    pass
                continue
            pass
        if self.data is not None:
            return start_iterate()
        else:
            self.get_raw_data()
            return start_iterate()
            pass
    def filter(self,regitem,label=r'',match=False):
        '''
        Filter the specific column of the table by regular expression.
        '''
        import re
        # self.get_raw_data()
        # self.set_glid()
        indf=self.data
        reg=re.compile(regitem)
        fli=[]
        for i in list(indf[label].drop_duplicates()):
            if match==False:
                b=re.search(reg,str(i))
            else:
                b=re.match(reg,str(i))
            if b is not None:
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
            ftable=DataFrame([],index=[],columns=self.get_cols())
            pass
        else:
            ftable=concat(ftableli,axis=0,join='outer')
        return ftable
    def getAcct(self,accid_item,accid_label='科目编码'):
        '''
        Get all and full records about given 'accid'.
        '''
        # self.set_glid()
        id_li=list(self.filter(accid_item,accid_label)['glid'].drop_duplicates())
        def get_relevant_row():
            for i in id_li:
                yield self.data[self.data['glid']==i]
        return concat(get_relevant_row(),axis=0,join='outer')
    def rand_sample(self,ss=None, percent=None, replace=False, weights=None, random_state=None, axis=None):
        '''
        DataFrame.sample(n=None, frac=None, replace=False, weights=None, random_state=None, axis=None)
        parameters:
            ss:sample_size;
            percent:percentage of total to sample;
            axis: 0 for rows_sampling and 1 for colums_sampling;
        '''
        if self.data is not None:
            self.sample_data=self.data.sample(n=ss, frac=percent, replace=False, weights=None, random_state=None, axis=None)
            return self.sample_data
        else:
            self.get_raw_data()
            self.sample_data=self.data.sample(n=ss, frac=percent, replace=False, weights=None, random_state=None, axis=None)
            return self.sample_data
        pass
