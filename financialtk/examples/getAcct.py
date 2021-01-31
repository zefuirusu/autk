#!/usr/bin/env python
# coding=utf-8
from pandas import ExcelWriter
from autk.financialtk.modules.mortalGL import MGL
import os
import threading
acct_li=[
    '2202',
    '1123',
    '1221',
    '2241'
]
bookli=[
    '北京神州汽车租赁有限公司',
    '天津神州汽车租赁有限公司',
    '神州租车\（厦门\）有限公司',
    '浩科融资租赁\（上海\）有限公公司',
    '海科\（平潭\）信息技术有限公司',
    '神州租车\（天津\）有限公司',
    '神州租车服务管理\（福建\）有限公司',
    '神州租车服务管理\（厦门\）有限公司',
    '赫兹汽车租赁\（上海\）有限公司',
    'Haike\ Leasing'
]
def parse_excel(xldir):
    # print(xldir.split(os.sep)[-1])
    savedir=os.path.join(os.curdir,r'sample-四往来-'+xldir.split(os.sep)[-1])
    # savedir='./sample-Output.xlsx'
    print(savedir)
    wter=ExcelWriter(path=savedir,engine='openpyxl')
    mgl=MGL(xldir,'Sheet1',title=0)
    for i in acct_li:
        item_acct=r'^'+str(i)+r'.*'
        # print(item_acct)
        for j in bookli:
            item_book=r'^'+str(j)+r'.*'
            # print(item_book)
            shtna=i+'-'+j
            print(shtna)
            ftable=mgl.filter(item_acct,'科目编码')
            mgl.load_df(ftable)
            ftable=mgl.filter(item_book,'账簿名称')
            ftable.to_excel(wter,sheet_name=shtna)
            wter.save()
        continue
    wter.save()
    pass
class ParseThread(threading.Thread):
    def __init__(self,xldir,name=None):
        self.xldir=xldir
        threading.Thread.__init__(self,name=name)
        pass
    def run(self):
        print(threading.current_thread().name)
        parse_excel(self.xldir)
        pass
basedir='./2020'
fileli=[]
for i in os.listdir(basedir):
    fileli.append(os.path.join(basedir,i))
    continue
# print(fileli)
for i in fileli:
    t=ParseThread(i,name=i.split(os.sep)[-1])
    t.start()
