#!/usr/bin/env python
# coding=utf-8
from autk.financialtk.zhgl import Gele
from autk.financialtk.journal import EntryRecord,JEntry
from autk.financialtk.logwriter import wtlog
from pandas import DataFrame
# gldir1='/mnt/e/skandha/z-Sync/a-Project/xin新雷能/glandtb/北京/bjgl-1-10月-output2020-1228.xlsx'
gldir1='./bjXinLeiNeng-GL-1-10月-output2020-1228.xlsx'
gldir2='./joinGL-bjXinLeiNeng-1-10月-output2020-1228.xlsx'
# gl1=Gele(gldir1,'表页-1')
# print(gl1.getshtli())
# print(gl1.getcols())
logdir='./glid1502.txt'
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
def filter1502(gl):
    import re
    from pandas import Series
    records=gl.iterate_record()
    # data=gl.getgldata()
    def get_glid_li():
        for i in records:
            if re.search(r'^1502.*$',i.accid) != None:
                # print(i.__dict__)
                yield i.glid
    glid_li=list(get_glid_li())
    glid_li=Series(glid_li).drop_duplicates()
    for i in glid_li:
        # wtlog(i,logdir)
        # print(i)
        yield i
def  test_journal_entries():
    # df=gl1.getgldata()
    # df=gl1.get_yield_record()
    # print(df)

    # test one_entry_df:
    one_entry_df=gl1.get_journal_entries()
    n=0
    for i in one_entry_df:
        print('glid:',i.glid,'\n','date:',i.date,'\n','debit:',i.debit[0],'\n','credit:',i.credit[0])
        print('-'*5)
        n+=1
        if n==400:
            break
        else:
            continue
    pass
def test_entries():
    import re
    with open('./glid1502.txt',mode='r',encoding='utf-8') as f:
        glid_li=f.readlines()
    def get_glid_li():
        for i in glid_li:
            i=re.sub('\n*$','',i)
            yield i
    li=[]
    for i in get_glid_li():
        li.append(i)
    gl=Gele(gldir2,'Sheet1',title=0)
    print(gl.getcols())
    je=gl.get_journal_entries()
    for j in je:
        if j.glid in li:
            yield j
        pass
    pass
def main():
    # test_entries()
    for i in test_entries():
        print(i.credit)
    # test_journal_entries()
if __name__=='__main__':
    main()
    pass
