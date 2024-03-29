#!/usr/bin/env python
# coding=utf-8
import re
import os
import datetime
from threading import Thread

class Walker:
    def __init__(
            self,
            item,
            search_dir=os.path.abspath(os.curdir),
            match=False
        ):
        self.search_dir=search_dir
        self.match=match
        self.item=item
        self.regitem=re.compile(self.item)
        self.resu_files=None
        self.resu_dirs=None
        pass
    def one_match(self,compare_target):
        if self.match==False:
            return re.search(self.regitem,compare_target)
        else:
            return re.match(self.regitem,compare_target)
        pass
    def get_files(self):
        for i,j,k in os.walk(self.search_dir):
            for file_name in k:
                if self.one_match(file_name) is not None:
                    yield os.path.abspath(os.path.join(i,file_name))
        pass
    def get_dirs(self):
        for i,j,k in os.walk(self.search_dir):
            for file_path in j:
                if self.one_match(file_path) is not None:
                    yield os.path.abspath(os.path.join(i,file_path))
        pass
    def start_search(self):
        def th1():
            self.resu_files=self.get_files()
        def th2():
            self.resu_dirs=self.get_dirs()
        t1=Thread(target=th1)
        t2=Thread(target=th2)
        t1.start()
        t1.join()
        t2.start()
        t2.join()
        pass
    pass
def find_regex(item,search_dir=os.path.abspath(os.curdir),match=False):
    '''
    To find and return `files/paths` according to regex `item` given, in `search_dir`.
    Search mode/Match mode are both supported.
    '''
    #  print('start time:',datetime.datetime.now())
    w1=Walker(item=item,search_dir=search_dir,match=match)
    w1.start_search()
    resu=[list(w1.resu_files),list(w1.resu_dirs)]
    #  print('end time:',datetime.datetime.now())
    return resu
def locate(
    by_func,
    strli, # can be a path,or list;
    search_dir,
    savepath=None,
    sheet_name='location',
    relative=False,
    ref_path=None,
    preview=True,
):
    '''
    Note:
        Sometimes `file` and `directory` cannot fit 
        with `regex` both well at the same time;
        This function is more powerful than
        `locate_by_func` at autk.handf.checkjr
    parameters:
        by_func:
            a function to transform strings in `strli` 
            into regular expression so as to search in `search_dir`;
        strli:
            can be list or file path 
            to indicate what you're searching;
        search_dir:
            where to search;
        savepath:
            where to save your output data;
        sheet_name:
            sheet name of the output data saved at `savepath`;
        relative:
            default False.
            if True, locations of `file` and `directory` will be 
            relative path from `ref_path`;
        ref_path:
            if ignored, `ref_path` will be the same as `savepath` on default;
    returns:
        DataFrame
        Output data looks like:
        ___________________________________________
        |target|regex|fcount|dcount|file|directory|
        |------|-----|------|------|----|---------|
        -------------------------------------------
        Output data will be sort by column 'glid';
    '''
    from os.path import isfile,isdir
    from pandas import DataFrame,Series
    from autk.parser.funcs import f2list
    from autk.parser.funcs import save_df
    from autk.parser.funcs import relative_path
    if ref_path is None:
        ref_path=savepath
    if isinstance(strli,list):
        pass
    elif isfile(strli):
        strli=f2list(strli)
    elif isdir(strli):
        strli=os.listdir(strli)
    else:
        print('check argument:strli')
        strli=[]
    resu_df=DataFrame(
        [],
        columns=[
            'target',
            'regex',
            'fcount',
            'dcount',
            'file',
            'directory',
        ]
    )
    resu_df['target']=strli
    resu_df.sort_values(
        'target',
        ascending=True,
        inplace=True,
        ignore_index=True
    )
    for row in resu_df.iterrows():
        row_data=row[1]
        target=row_data['target']
        regex=by_func(target)
        find_results=find_regex(
            regex,
            search_dir,
            match=False
        )
        f_locations=find_results[0]
        d_locations=find_results[1]
        fcount=len(f_locations)
        dcount=len(d_locations)
        if fcount==0:
            f_locations=''
        else:
            if relative==False:
                f_locations=';'.join(f_locations)
            else:
                f_locations=';'.join(
                    [
                        relative_path(f,ref_path)
                     for f in f_locations
                    ]
                )
        if dcount==0:
            d_locations=''
        else:
            if relative==False:
                d_locations=';'.join(d_locations)
            else:
                d_locations=';'.join(
                    [
                        relative_path(d,ref_path)
                     for d in d_locations
                    ]
                )
        row_data['target']=target
        row_data['regex']=regex
        row_data['fcount']=fcount
        row_data['dcount']=dcount
        row_data['file']=f_locations
        row_data['directory']=d_locations
    #  print(resu_df)
    if preview==False:
        save_df(
            resu_df,
            sheet_name=sheet_name,
            save_path=savepath
        )
    return resu_df
if __name__=='__main__':
    pass
