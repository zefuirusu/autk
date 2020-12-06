# Tutorial
## Automatic Sampling
1. 新建科目编码文件,将要抽样的科目编码列在上边,一行一科目,不要有空行.
2. `sample.py`已经比较完美了,但尚未有对数量抽样的功能,还应该写一个对待抽凭证号去重并输出的功能.
### Expample:
```python
#!/usr/bin/env python
# coding=utf-8
from autk.zhchart import ChartAccount
from autk.zhgl import Gele,Acct
from autk.sample import AuSample

acctlidir1='./acctli/bj-acctli.txt'
acctlidir2='./acctli/xa-acctli.txt'

sdir1='./outSample/bj-Multi.xlsx'
sdir2='./outSample/xa-Multi.xlsx'

cht1=ChartAccount('../序时账和余额表/北京余额表.xlsx')
cht2=ChartAccount('../序时账和余额表/西安余额表.xlsx')

gl1=Gele('../序时账和余额表/北京-joinsheetplus.xlsx',shtna='bjgl10',title=0)
gl2=Gele('../序时账和余额表/西安序时账-202001-10.xlsx',shtna='xagl10',title=0)

lg1='./s_log/bj_sam_log.txt'
lg2='./s_log/xa_sam_log.txt'

def bj_sample():
    s1=AuSample(gl1,cht1,sdir1,acctli_dir=acctlidir1,logdir=lg1)
    s1.multiSample()
    return
def xa_sample():
    s2=AuSample(gl2,cht2,sdir2,acctli_dir=acctlidir2,logdir=lg2)
    s2.multiSample()
    return
if __name__=='__main__':
    # start sampling:
    import threading
    t1=threading.Thread(target=bj_sample)
    t2=threading.Thread(target=xa_sample)
    t1.start()
    t2.start()
    pass
```
