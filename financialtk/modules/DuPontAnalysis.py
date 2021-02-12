#!/usr/bin/env python
# encoding='utf-8'

##财务比率分析体系
###短期偿债能力
###长期偿债能力
###营运能力
###盈利能力
###市价比率

class ROE:
    #def __init__(self,netIncome=0,equity=1):
        #roe=netIncome/equity
        #return roe
    def dupontAna(self,netIncome=0,revenue=1,liability=0,asset=1):
        npm=netIncome/revenue
        atr=revenue/asset
        dar=liability/asset
        roa=npm*atr
        em=1/(1-dar)
        du=roa*em
        duDict={'roe':du,
                'npm,atr,em':[npm,atr,em],
                'npm,atr,dar':[npm,atr,dar]
                }
        return duDict
class ROA:
    def __init__(self,netIncome=0,asset=1):
        roa=netIncome/asset
        #return roa
class EM:
    # equity multiplier
    def __init__(self,equity=0,asset=1):
        em=equity/asset
        #return em
class DAR:
    # debt to asset ratio
    def __init__(self,liability=0,asset=1):
        dar=liability/asset
        #return dar
class NPM:
    # net profit margin on sales
    def __init__(self,netIncome=0,revenue=1):
        npm=netIncome/revenue
        #return npm
class ATR:
    # asset turnover ratio
    def __init__(self,revenue=1,asset=1):
        atr=revenue/asset
        #return atr
#class PS:
    # price-to-sales ratio 市销率=每股市价/每股销售额=总市值/总收入revenue
#class PBR:
    # price-to-book ratio 市净率=每股市价/每股净资产=总市值/总资产asset
#class PER:
    # price earnings ratio 市盈率=每股市价/每股收益(EPS,earnings per share)=总市值/净利润，eps=净利润/股本总数
#

a1=ROE()
b1=a1.dupontAna()
print(b1)
