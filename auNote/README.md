# Notes in Auditing
Taking notes is a good habbit/choice when participating in an auditing project near the end of the year.
This file is the list of link references.
## 1.Reference Links List
### 1.1 Financial Accounting
- [在建工程](https://zhuanlan.zhihu.com/p/148759446)
- [融资租赁](http://www.chinaacc.com/new/635_649_/2009_11_16_le831487161119002960.shtml)
### 1.2 Management Accounting

### 1.3 Auditing
- [存货底稿](https://zhuanlan.zhihu.com/p/84144157)
- [审计重要性水平计算基准及百分比选择总结](https://bbs.esnai.com/thread-5419178-1-1.html)
- [函证的替代测试](http://shuo.news.esnai.com/article/202004/201554.shtml)
    - 如果审计后重要性水平的基准金额变小，意味着重要性变小，一般会用审计后的基准数据来修改重要性水平；
    - 如果果审计后重要性水平的基准金额变大，如果大的不是特别离谱，出于谨慎性原则一般不需要修改重要性水平，因为此时工作已经按计划的重要性水平执行，工作是做多了而不是做少了.
- [审计中重要性水平是如何应用的](https://www.zhihu.com/question/354188659)
## 2.Algorithm (算法概述)
### 2.1 折旧计提分配差异查验
1. 从余额表中找到相应的会计科目[成本费用类,累计折旧],获取其[科目编码,费用类借方发生额,累计折旧贷方发生额].
2. 先计算其计提分配的总数是否相等,如总数相等则结束分析.
3. 从贷方出发,开始分析.从序时账中筛选,[科目编码=累计折旧相关编码,借方发生额=0],获取记账凭证编号[glid].
4. 在序时账中筛选上述glid,对[借方发生额!=0]的记录汇总分析,按[科目名称,科目编码]分类汇总.
- 注意
    - 序时账除了[借方发生额,贷方发生额]之外,必须有[科目编码,glid,月份]三个字段.
    - 职工薪酬计提和分配的差异算法大同小异.
### 2.2 对序时账摘要分析的
1. 分词分析并统计词频
2. 输出结果,保存到文件.
3. 代码详见`./zhaiyAna_byJieba.py`
### 2.3 货币资金流向分析
- 筛选序时账数据，获取与银行存款有关的所有完整凭证数据`class CashEntryRecord(MGL)`，并验证借贷方合计是否平衡；将上述数据分为两部分：`CashOutEntry(MGL)`(depth=0)和`CashInEntry(MGL)`(depth=0)，两者都以`glid`字段唯一标识每一个`class EntryRecord`；
- 现金流出分析
    - 对`CashOutEntry`进行数据透视，统计本期借方发生额的分布情况；
    - 在序时账中索引`CashOutEntry.glid_list`，得到`class CashOutEntry(depth=1)`并数据透视，统计本期贷方发生额分布情况；
