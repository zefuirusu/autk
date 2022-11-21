#!/usr/bin/env python
# -*- coding: utf-8 -*-

from autk.mapper.map import SampleEglMap,EglMap
from autk.reader.table import ImmortalTable
from autk.reader.mortalgl import MGL
from autk.reader.chart import MCA
from autk.reader.xlsht import XlSheet
def calxl(df=None):
    '''
    Calculator Excel.
    '''
    xl=XlSheet(
        file_path='',
        sheet_name='',
        title=0,
        keep_meta_info=True,
        xlmap=None,
        use_map=False,
        key_index=[],
        key_name=''
    )
    xl.accept_data(df)
    return xl
def table(xlmeta,common_title=0,keep_meta_info=True):
    return ImmortalTable(
        xlmeta=xlmeta,
        common_title=common_title,
        auto_load=False,
        key_index=[],
        key_name='key_id',
        xlmap=None,
        use_map=False,
        keep_meta_info=keep_meta_info
    )
def gl(xlmeta,common_title=3,sample_col=True,nick_name='mgl'):
    mgl=MGL(
        xlmeta=xlmeta,
        common_title=common_title,
        key_index=['date','mark','jrid'],
        key_name='glid',
        # accid_col='accid',
        # accna_col='accna',
        # drcrdesc=['dr_amount',
        #           'cr_amount'],
        top_accid_len=4,
        accna_split_by=r'/',
        date_col='date',
        date_split_by=r'-',
        sample_col=sample_col,
        use_map=True,
        auto_load=False,
        nick_name=nick_name
        )
    mgl.rename(nick_name)
    return mgl
def chart(xlmeta):
    return MCA(
        xlmeta=xlmeta,
        common_title=3,
        accid_col='科目编号',
        accna_col='科目名称',
        drcrdesc=['借方发生','贷方发生'],
        top_accid_len=4,
        auto_load=False,
        xlmap=None,
        use_map=False
    )
if __name__=='__main__':
    pass
