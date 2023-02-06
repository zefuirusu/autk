#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 23:15:30 2021

@author: sk008
"""
from autk.reader.base.table import ImmortalTable
class XlJoin(ImmortalTable):
    @staticmethod
    def __time_monitor(afunc):
        import datetime
        def time_wrapper(*args,**kwargs):
            t1=datetime.datetime.now()
            print('[',t1,']','start_method:',afunc.__name__)
            afunc(*args,**kwargs)
            t2=datetime.datetime.now()
            print('[',t2,']','end_method:',afunc.__name__)
            return afunc(*args,**kwargs)
        return time_wrapper
    @__time_monitor
    def __init__(self, join_meta=None,save_path='./join.xlsx'):
        from os.path import isfile
        if isfile(str(join_meta)):
            super().__init__(self.__get_meta_from_json(join_meta)) # get join_meta from json file if its path is passed as argument.
        else:
            super().__init__(join_meta) # join_meta is the same as MortalTable.xlmeta.
        self.save_path=save_path
        pass
    def __get_meta_from_json(self,json_path):
        from json import load
        with open(json_path,mode='r',encoding='utf-8') as f:
            json_meta=load(f)
        return json_meta
    def scan(self):
        '''
        Parameters
        ----------
        No need to pass an argument.
        Returns
        -------
        None.
        Nothing to return but print output to the terminal.
        '''
        for xl in self._xl_obj_set:
            print('---',xl.file_name,'---')
            print('\tsheet_name:',xl.sheet_name)
            print('\tcolumns:',xl.columns)
        pass
    def join(self, split_sheet=False):
        '''
        Parameters
        ----------
        split_sheet : TYPE, optional
            DESCRIPTION. The default is False.
        Returns
        -------
        None.
        '''
        from pandas import concat
        if split_sheet==True:
            from pandas import ExcelWriter
            from openpyxl import Workbook
            wter=ExcelWriter(self.save_path,engine='openpyxl')
            wb=Workbook()
            wb.save(self.save_path)
            wter.book=wb
            wb.close()
            for xl in self._xl_obj_set:
                xl.save(self.save_path)
            print('One Excel book, different sheets.')
        else:
            print('Join: One Excel book, one sheet.')
            d=concat(self.data_set,axis=0,join='outer')
            d.to_excel(self.save_path)
            pass
        pass
    pass
