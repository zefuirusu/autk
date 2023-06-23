#!/usr/bin/env python
# -*- coding: utf-8 -*-

from autk.mapper.map import InvChartMap
from autk.reader.unit.calinven import CalInv
from autk.reader.base.xlbk import XlBook
from autk import save_df
m20=InvChartMap(3)
m21=InvChartMap(3)
p20='./data/rawMaterial-yl-2020.xlsx'
p21='./data/rawMaterial-yl-2021.xlsx'

def test_age():
    c1=CalInv(
        [p20,'data',0],
        keep_meta_info=False,
        key_index=['invid'],
        key_name='invid',
        age_len=3,
        is_previous=True,
        previous=None,
        xlmap=m20,
        use_map=True
    )
    c2=CalInv(
        [p21,'data',0],
        keep_meta_info=False,
        key_index=['invid'],
        key_name='invid',
        age_len=3,
        is_previous=False,
        previous=c1,
        xlmap=m21,
        use_map=True
    )
    print('columns:\n')
    print(c1.columns)
    print(c2.columns)
    print('maps:\n')
    print(c1.xlmap.show)
    print(c2.xlmap.show)
    print('data:\n')
    print(c1.data)
    print(c2.data)
    print('-'*12)
    print('columns of data 2021 before calculation:',c2.data.columns)
    print('check age_cols:',c2.xlmap.get_age_cols(c2.age_len),c2.age_cols)
    c2.cal_age_from_previous(c1)
    c2.check()
    print('vertical amount sum for year 2021',c2.data[c2.xlmap.amt_cols].sum().sum())
    print('vertical sum for all ages in 2021:',c2.data[c2.age_cols].sum().sum())
    pass
def test_cols():
    b1=XlBook(p20)
    d1=b1.test_map(m20,0)
    print(d1)
    b2=XlBook(p21)
    d2=b2.test_map(m21,0)
    print(d2)
    save_df(d1,'2020','./testmap.xlsx')
    save_df(d2,'2021','./testmap.xlsx')
    pass
if __name__=='__main__':
    #  test_cols()
    test_age()
    pass
