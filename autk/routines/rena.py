#!/usr/bin/env python
# coding=utf-8
import os
import shutil
from pandas import read_excel
# from autk.parser.funcs import f2list
class Rename:
    def __init__(self,target_dir,meta_path,shtna):
        '''
        Parameters
        ----------
        target_dir : str
            the directory where the files to be renamed locates.
        meta_path : str
            Excel_path.
        shtna : str
            sheet_name, telling you the map of old_name and new_name.

        Returns
        -------
        None.

        '''
        self.meta_path=meta_path
        self.shtna=shtna
        self.target_dir=target_dir
        pass
    def scan(self):
        print(os.listdir(self.target_dir))
        meta=read_excel(self.meta_path,sheet_name=self.shtna,engine='openpyxl')
        print(meta)
        print(meta.dtypes)
        return
    def start_rename(self):
        meta=read_excel(self.meta_path,sheet_name=self.shtna,engine='openpyxl')
        for i in meta.iterrows():
            row_data=i[1]
            old_name=row_data['old_name']
            new_name=row_data['new_name']
            old_file=os.path.abspath(os.path.join(self.target_dir,old_name))
            new_file=os.path.abspath(os.path.join(self.target_dir,new_name))
            # print(old_file)
            # print(new_file)
            try:
                shutil.move(old_file,new_file)
                print('ok!',old_name,'to',new_name)
            except:
                print('rename failed:\n',old_file)
            continue
        return
    pass
if __name__=='__main__':
    pass
