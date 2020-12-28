#!/usr/bin/env python
# coding=utf-8
from autk.financialtk.zhgl import Gele
from autk.financialtk.journal import EntryRecord,JEntry
from pandas import DataFrame
# gldir1='/mnt/e/skandha/z-Sync/a-Project/xin新雷能/glandtb/北京/bjgl-1-10月-output2020-1228.xlsx'
gldir1='./bjXinLeiNeng-GL-1-10月-output2020-1228.xlsx'
gl1=Gele(gldir1,'表页-1')
# print(gl1.getcols())
def getjentry():
    data1=gl1.getdata(fillna=True)
    print(list(data1.columns))
    for i in data1.iterrows():
        yield i
    pass
def getentries():
    for i in getjentry():
        er=EntryRecord(i)
        if er.__dict__ != {}:
            yield er.__dict__
        else:
            pass
def getsheets():
    for i in gl1.getshtli():
        gl=Gele(gldir1,i)
        df_generator=gl.get_yield_gl()
        yield df_generator
def main():
    # df=gl1.getgldata()
    # df=gl1.get_yield_record()
    # print(df)
    # glid_li=df['glid'].drop_duplicates()
    # glid_li=list(glid_li)
    # for i in range(5):
    #     one_entry_set=df[df['glid']==glid_li[i]]
        # print(one_entry_set)
    one_entry_df=gl1.entry_yield()
    n=0
    for i in one_entry_df:
        print('glid:',i.glid,'\n','date:',i.date,'\n','debit:',i.debit[0],'\n','credit:',i.credit[0])
        print('-'*5)
        n+=1
        if n==4:
            break
        else:
            continue
    pass
if __name__=='__main__':
    main()
    pass
