# Tutorial
## Automatic Sampling
1. 新建科目编码文件,将要抽样的科目编码列在上边,一行一科目,不要有空行.
2. `sample.py`已经比较完美了,但尚未有对数量抽样的功能,还应该写一个对待抽凭证号去重并输出的功能.
3. 下边的示例,如果报错则是因为北京的序时账不完整,少了某些科目的序时账记录.
### Expample:
```python
#!/usr/bin/env python
# coding=utf-8
from autk.financialtk.zhchart import ChartAccount
from autk.financialtk.zhgl import Gele,Acct
from autk.financialtk.sample import AuSample

gl1=Gele('./inputData/北京序时账-202001-10.xlsx',shtna='bjgl10',title=0)
gl2=Gele('./inputData/西安序时账-202001-10.xlsx',shtna='xagl10',title=0)

cht1=ChartAccount('../序时账和余额表/北京余额表.xlsx')
cht2=ChartAccount('../序时账和余额表/西安余额表.xlsx')

sdir1='./outSample/bj-Multi.xlsx'
sdir2='./outSample/xa-Multi.xlsx'

acctlidir1='./acctlidir/bj-acctli.txt'
acctlidir2='./acctlidir/xa-acctli.txt'

lg1='./s_log/bj_sam_log.txt'
lg2='./s_log/xa_sam_log.txt'

# start testing:
def bj_sample():
    s1=AuSample(gl1,cht1,sdir1,acctli_dir=acctlidir1,logdir=lg1)
    s1.multiSample()
    return
def xa_sample():
    s2=AuSample(gl2,cht2,sdir2,acctli_dir=acctlidir2,logdir=lg2)
    s2.multiSample()
    return
if __name__=='__main__':
    import threading
    t1=threading.Thread(target=bj_sample)
    t2=threading.Thread(target=xa_sample)
    t1.start()
    t2.start()
    pass
```
