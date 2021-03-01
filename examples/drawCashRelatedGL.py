#!/usr/bin/env python
# coding=utf-8
'''
Get all GL records about 1002 first, and then filter it by 2202/1123/1221/2241.
'''
import os
import re
import threading
from pandas import concat
from autk.financialtk.modules.mortalGL import MGL
acct_li=[
    # '2202',
    # '1123',
    '1221',
    '2241'
]
def trans_reg(instr):
    out_str=r'^'+instr+r'.*'
    out_str=re.compile(out_str)
    return out_str
acct_reg_li=list(map(trans_reg,acct_li))
def one_draw(inxlpath,wt_path):
    savename=r'cash-bjar-'+inxlpath.split(os.sep)[-1]
    savepath=os.path.abspath(os.path.join(wt_path,savename))
    print('starting: %s'%savename)
    mgl=MGL(inxlpath,'Sheet1',0)
    mgl.load_raw_data()
    print('original data loaded:%s'%savename,mgl.data.shape)
    mgl.filter('北京神州汽车租赁有限公司-CAR基准账簿','账簿名称',over_write=True)
    mgl.set_glid(['账簿编码','期间年','期间月','凭证编码'])
    mgl.load_df(mgl.getAcct(r'^1002.*'))
    print('cash data loaded.',mgl.data.shape)
    def get_ar_idli(acct_reg_li):
        for i in acct_reg_li:
            ar_data=mgl.filter(i,'科目编码',over_write=False)
            idli= list(ar_data['glid'].drop_duplicates())
            for j in idli:
                yield j
            continue
        pass
    def get_ar_data_li(idli):
        for i in idli:
            yield mgl.data[mgl.data['glid']==i]
        pass
    data=concat(get_ar_data_li(get_ar_idli(acct_reg_li)),axis=0,join='inner')
    data.to_excel(savepath)
    print('%s written!'%savename)
    pass
class DrawThread(threading.Thread):
    def __init__(self,inxlpath,wt_path):
        self.inxlpath=inxlpath
        self.wt_path=wt_path
        name=inxlpath.split(os.sep)[-1]
        threading.Thread.__init__(self,name=name)
        pass
    def run(self):
        print('threading is started:',threading.current_thread().name)
        one_draw(self.inxlpath,self.wt_path)
        pass
if __name__=='__main__':
    basedir='../gl2020'
    savedir='../bj-output'
    fileli=[]
    for i in os.listdir(basedir):
        fileli.append(os.path.abspath(os.path.join(basedir,i)))
        continue
    for i in fileli:
        dth=DrawThread(i,savedir)
        dth.start()
    pass
