#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pandas import DataFrame
from autk.parser.funcs import save_df,wtlog
from autk.reader.base.xlbk import XlBook
class Sample:
    def __init__(
        self,
        mgl,
        chart,
    ):
        self.mgl=mgl
        self.chart=chart
        self.temp=[]
        self.sample_data=None
        self.sum_df_cols=[
            'id',
            'type',
            'glid',
            'item_name',
            'if_collected',
            'comment',
            'ref_link',
            'regitem',
            'status',
            'location',
            'attachments',
        ]
        pass
    def check(self):
        gl_drcr=self.mgl.xlmap.drcrdesc
        ch_drcr=self.chart.xlmap.drcrdesc
        print(
            'check if gl fits well with chart:',
            gl_drcr==ch_drcr,
            self.mgl.xlmap.accid_col==self.chart.xlmap.accid_col,
            self.mgl.xlmap.accna_col==self.chart.xlmap.accna_col
        )
        return gl_drcr==ch_drcr
    def save(self,savepath):
        self.mgl.load_raw_data()
        self.chart.load_raw_data()
        sum_df=DataFrame([],columns=self.sum_df_cols)
        save_df(
            sum_df,
            'summary',
            savepath
        )
        save_df(
            self.mgl.data,
            'gl',
            savepath
        )
        save_df(
            self.chart.data,
            'chart',
            savepath
        )
        pass
    def test_map(self,xlmap,common_title=0):
        '''
        Output:
            columns_map:.....
            sheet1 real_columns.....
            sheet2 real_columns.....
            ...
        '''
        pass
    def percent_sample(self,p,target_top_accid_list=[]):
        pass
    def num_sample(self,num,target_top_accid_list=[]):
        pass
if __name__=='__main__':
    pass
