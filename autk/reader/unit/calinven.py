#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
start_array+dr_array-cr_array=end_array;
start_array=cur_amt_df.merge(pre_end_array,how='left',on='invid');
dr_array=parse_dr_amt(dr_amt);
cr_array=parse_cr_amt(cr_amt);
end_array=start_array+dr_array-cr_array;
'''
import os
import re
from copy import deepcopy
from pandas import DataFrame,Series
from threading import Thread

from autk.mapper.map import InvChartMap,InvMonthMap
from autk.reader.base.xlsht import XlSheet

class CalInv(XlSheet):
    def __init__(
        self,
        shmeta=[None,'sheet0',0],
        keep_meta_info=False,
        key_index=['invid'], #['凭证日期','字','号'],
        key_name='invid',
        age_len=3, ## age_len is the same as ages_count in map;
        is_previous=True,
        previous=None,
        xlmap=InvChartMap(3),
        use_map=False,
    ):
        self.data=None
        self.age_len=age_len
        self.is_previous=is_previous
        self.previous=previous
        self.key_index=key_index
        self.key_name=key_name
        self.set_inv_attr(
            xlmap.num_cols,
            xlmap.amt_cols,
            xlmap.get_age_cols(age_len)
        )
        XlSheet.__init__(
            self,
            shmeta=shmeta,
            xlmap=xlmap,
            use_map=use_map,
            keep_meta_info=keep_meta_info,
            key_index=self.key_index,
            key_name=self.key_name
        )
        self.set_key_index(key_index,key_name)
        # columns of data differs if `is_previous` is True or not:
        #  if is_previous==False:
            #  self.xlmap.set_age_cols(0)
        #  else:
            #  self.xlmap.set_age_cols(self.age_len)
        #  self.load_raw_data()
        pass
    def load_raw_data(self):
        super().load_raw_data()
        self.data=self.data[self.get_key_cols(previous=self.is_previous)]
        self.columns=list(self.data.columns)
    def set_inv_attr(self,num_cols,amt_cols,age_cols):
        if (
            num_cols !=[] or
            amt_cols !=[] or
            age_cols !=[]
        ):
            self.num_cols=num_cols
            self.amt_cols=amt_cols
            self.age_cols=age_cols
        elif self.use_map == True and (isinstance(xlmap,InvChartMap) or isinstance(xlmap,InvMonthMap)):
            self.num_cols=self.xlmap.num_cols
            self.amt_cols=self.xlmap.amt_cols
            self.age_cols=self.xlmap.get_age_cols(self.age_len)
        else:
            self.num_cols=num_cols
            self.amt_cols=amt_cols
            self.age_cols=age_cols
            pass
        pass
    def get_key_cols(self,previous=False):
        k=[self.key_name]
        if previous==True:
            k.extend(self.age_cols)
        else:
            k.extend(self.amt_cols)
        return k
    def cal_age_by_merge(self,pre_CalInv=None):
        '''
        same but faster than cal_age_from_previous;
        '''
        if pre_CalInv is None:
            pre_CalInv=self.previous
        left_df=self.data
        right_df=pre_CalInv.data
        print('left(current year):\n',left_df)
        print('right(previous year):\n',right_df)
        resu=left_df.merge(right_df,how='left',on=self.key_name)
        resu.fillna(0.0,inplace=True)
        age_sum_before=resu[self.age_cols].sum(axis=0).sum()
        resu[self.age_cols[-1]]=resu[self.age_cols[-2]]+resu[self.age_cols[-1]]
        for n in range(1,len(self.age_cols)-1):
            resu[self.age_cols[n]]=resu[self.age_cols[n-1]]
            pass
        resu[self.age_cols[0]]=Series([0]*resu.shape[0],index=resu.index)
        age_sum_after=resu[self.age_cols].sum(axis=0).sum()
        print('continue from previous:\n',resu)
        print('if sum of age changed:',age_sum_before,age_sum_after)
        def negative_adjust(series):
            for n in range(len(series)):
                cur_n=len(series)-n-1
                if series[cur_n]<0:
                    series[cur_n-1]=series[cur_n]+series[cur_n-1]
                    series[cur_n]=0.0
                else:
                    pass
                continue
            pass
        def row_age_cal(row_series):
            row_age=row_series[self.age_cols]
            row_age.fillna(0.0,inplace=True)
            vector_in=Series(index=row_age.index)
            vector_out=Series(index=row_age.index)
            vector_in[0]=row_series['amt_in']
            vector_out[-1]=row_series['amt_out']
            vector_in.fillna(0.0,inplace=True)
            vector_out.fillna(0.0,inplace=True)
            if abs(row_age.sum())<0.004:
                resu=Series(index=row_age.index)
                resu[0]=row_series['amt_bal']
                resu.fillna(0.0,inplace=True)
            else:
                resu=row_age+vector_in-vector_out
            negative_adjust(resu)
            return resu
        resu[self.age_cols]=deepcopy(resu.apply(
            row_age_cal,
            axis=1,
            raw=False,
            result_type='reduce'
        ))
        self.data=resu
        return resu
    def cal_age_from_previous(self,pre_CalInv):
        '''
        same but slower than self.cal_age_by_merge;
        '''
        from numpy import zeros
        from numpy import array
        from pandas import Series
        def get_start_amt(inv_id):
            inv_id=inv_id.join([r'^',r'$'])
            start_age_df=pre_CalInv.filter(
                [[inv_id,pre_CalInv.key_name,True,True]],
                filter_type='str',
                over_write=False,
                type_xl=False
            )
            if start_age_df.shape[0]==1:
                start_age_series=Series(
                    start_age_df.iloc[0,:][self.age_cols].values,
                    index=self.age_cols
                )
            elif start_age_df.shape[0]>1:
                print('物料编码重复:',inv_id)
                print(start_age_df)
                start_age_series=Series(
                    [0.0]*self.age_len,
                    index=self.age_cols
                )
            else:
                start_age_series=Series(
                    [0.0]*self.age_len,
                    index=self.age_cols
                )
                #  print('上年无此物料:',inv_id)
            start_age_vector=start_age_series.values
            start_vector=zeros((self.age_len,),dtype=float)
            for n in range(len(start_vector)-1):
                start_vector[n]=start_age_vector[n+1]
            start_vector[-1]=start_vector[-1]+start_age_vector[-1]
            return start_vector
        def parse_dr_amt(dr_amt):
            dr_vector=zeros((self.age_len,),dtype=float)
            if dr_amt<0:
                dr_vector[-1]=dr_amt
            else:
                dr_vector[0]=dr_amt
            return dr_vector
        def parse_cr_amt(cr_amt):
            cr_vector=zeros((self.age_len,),dtype=float)
            cr_vector[-1]=cr_amt
            return cr_vector
        def get_end_amt(start_vector,dr_vector,cr_vector):
            end_vector=start_vector+dr_vector-cr_vector
            #  print('before drop:\n',end_vector)
            end_vector=list(end_vector)
            def drop_negative(left,right):
                if left<0:
                    right=right+left
                    left=0
                return (left,right)
            for n in range(len(end_vector)-1):
                left,right=drop_negative(
                    end_vector[len(end_vector)-1-n],
                    end_vector[len(end_vector)-1-n-1]
                )
                end_vector[len(end_vector)-1-n]=left
                end_vector[len(end_vector)-1-n-1]=right
                pass
            for n in range(len(end_vector)-1):
                left,right=drop_negative(end_vector[n],end_vector[n+1])
                end_vector[n]=left
                end_vector[n+1]=right
            end_vector=array(end_vector)
            #  print('after drop:\n',end_vector)
            return end_vector
        def cal_by_row(row_series):
            end_amt_vector=get_end_amt(
                get_start_amt(row_series[self.key_name]),
                parse_dr_amt(row_series[self.amt_cols[1]]),
                parse_cr_amt(row_series[self.amt_cols[2]])
            )
            end_amt_series=Series(end_amt_vector,index=self.age_cols)
            return end_amt_series
        def cal_current_age(row_series,age):
            end_v=cal_by_row(row_series)
            current_age_amt=end_v[age]
            return current_age_amt
        '''
        testing.....unfinished function;
        for row in self.data.iterrows():
            row_series=row[1]
            print(cal_by_row(row_series))
        #  print(
        #  get_end_amt(
            #  array([1000,-200,400]),
            #  parse_dr_amt(450),
            #  parse_cr_amt(100)
        #  )
        #  )
        '''
        for age in self.age_cols:
            print('current_age:',age)
            self.data.apply(
                cal_current_age,
                axis=1,
                raw=False,
                result_type=None,
                args=(age,)
            )
        pass
    def check(self):
        def check_bal(row_series):
            return (
                row_series[self.amt_cols[0]]+
                row_series[self.amt_cols[1]]-
                row_series[self.amt_cols[2]]
            )
        def check_age_sum(row_series):
            return (
                row_series[self.age_cols].values.sum()-
                row_series[self.amt_cols[3]]
            )
        bal_logic_series=self.data.apply(
            check_bal,
            axis=1,
            raw=False,
            result_type='reduce'
        )
        age_sum_series=self.data.apply(
            check_age_sum,
            axis=1,
            raw=False,
            result_type='reduce'
        )
        return (
            bal_logic_series.sum(),
            age_sum_series.sum()
        )
    pass
