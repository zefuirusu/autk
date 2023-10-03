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

def cal_age(savepath=None):
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
    if savepath is not None:
        save_df(
            c1.data,
            'inventory2020',
            savepath
        )
        save_df(
            c2.data,
            'inventory2021_before', 
            # 这是他原本提供的本年进销存，
            # 可以看到有的存货编码是重复的，这个表本身有缺陷；
            savepath
        )
    else:
        print('inventory2020')
        print(c1.data)
        print('inventory2021_before')
        print(c2.data)
    c2.cal_age_by_merge()
    c2.check()
    if savepath is not None:
        save_df(
            c2.data,
            'inventory2021_after',
            savepath
        )
    else:
        print('inventory2021_after')
        print(c2.data)
    pass
if __name__=='__main__':
    cal_age(None)
    pass
