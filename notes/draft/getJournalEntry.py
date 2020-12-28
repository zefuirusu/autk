#!/usr/bin/env python
# coding=utf-8
from autk.financialtk.zhgl import Gele
from autk.financialtk.journal import EntryRecord,JEntry
from pandas import DataFrame
def getjentry():
    # gldir1='/mnt/e/skandha/z-Sync/a-Project/xin新雷能/glandtb/北京/bjgl-1-10月-output2020-1228.xlsx'
    gldir1='./bjXinLeiNeng-GL-1-10月-output2020-1228.xlsx'
    gl1=Gele(gldir1,'表页-2')
    print(gl1.getcols())
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
        # yield  EntryRecord(i).__dict__
def main():
    # getjentry()
    # n=0
    # for i in getjentry():
        # print("0:\n",i[0])
        # print("1:\n",i[1])
        # print('[1,1]:\n',i[1][1])
        # glid='-'.join(map(str,i[1][0:3]))
        # glid='-'.join([i[1][0],i[1][1],str(int(i[1][2]))])
        # date=i[1][0]
        # scan=i[1][3]
        # accid=i[1][4]
        # accna=i[1][5]
        # er=EntryRecord(i)
        # print(er.__dict__)
        # n+=1
        # if n==5:
        #     break
        # else:
        #     continue
        # continue
    # li=[]
    # for i in getjentry():
    #     li.append(i)
    # testJ=EntryRecord(li[-1])
    # print(testJ.__dict__)
    df=DataFrame(getentries())
    print(df)
    pass
if __name__=='__main__':
    main()
    pass
