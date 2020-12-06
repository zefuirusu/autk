# Tutorial
## Automatic Sampling
1. 新建`'./sampleAcctID_list.txt'`,将要抽样的科目编码列在上边,一行一科目,不要有空行.
2. `sample.py`写了一半,尚未完成,该脚本会读取上述被抽科目.还应该写一个对待抽凭证号去重并输出的功能.
### Expample:
```python
#!/usr/bin/env python
# coding=utf-8
from autk.zhchart import ChartAccount
from autk.zhgl import Gele,Acct
from autk.sample import AuSample

acctlidir1='./bj-acctli.txt'
acctlidir2='./xa-acctli.txt'

sdir1='./bj-testMulti.xlsx'
sdir2='./xa-testMulti.xlsx'

cht1=ChartAccount('../序时账和余额表/北京余额表.xlsx')
cht2=ChartAccount('../序时账和余额表/西安余额表.xlsx')

gl1=Gele('../序时账和余额表/北京-joinsheetplus.xlsx',shtna='bjgl10',title=0)
gl2=Gele('../序时账和余额表/西安序时账-202001-10.xlsx',shtna='xagl10',title=0)

# start sampling:
# acct1=Acct('固定资产','1501')
s1=AuSample(gl1,cht1)
s1.multiSample(acctlidir1,sdir1)

s2=AuSample(gl2,cht2)
s2.multiSample(acctlidir2,sdir2)
```
