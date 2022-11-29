#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import shutil
from threading import Thread
from autk.parser.funcs import start_thread_list,f2list
def tidy_up(
    jr_to_regex_func, # function to transform jr_str into regex;
    jrli_path, # the file which lists which jrs to find;
    fs_dir, # 'from' and 'search' directory;
    to_dir, # 'to' and save/copy-to directory;
    move=False,
    savepath='./',
):
    '''
    Input which jrs to find by file at `jrli_path`; 
    Tansform jrs into regular expression through `jr_to_regex_func`;
    Search jrs by regex in `fs_dir`;
    Copy/move results into `to_dir`;
    Output jr-location mapping data at an Excel file;
    '''
    jrli=f2list(jrli_path)
    def single_tidy(jr_str):
        save_dir=os.path.join(
            to_dir,
            jr_str
        )
        from_path_list=find_regex(
            jr_to_regex_func(jr_str),
            search_dir=fs_dir,
            match=True
        )[0]
        from_dir_path_list=find_regex(
            jr_to_regex_func(jr_str),
            search_dir=fs_dir,
            match=True
        )[1]
        if os.path.isdir(save_dir):
            pass
        else:
            if len(from_path_list)==0:
                pass
            else:
                os.mkdir(
                   save_dir 
                )
        #  print('save to',save_dir)
        #  print('tidy up ',jr_str,':')
        #  print(from_path_list)
        thread_list=[]
        for p in from_path_list:
            file_name=str(p.split(os.sep)[-1])
            thread_list.append(
                Thread(
                    target=shutil.copy,
                    args=(
                        p,
                        os.path.join(save_dir,file_name)
                    ),
                    name='copy_file_'+file_name
                )
            )
            continue
        start_thread_list(thread_list)
        pass
    thread_list=[]
    for jr_str in jrli:
        thread_list.append(
            Thread(
                target=single_tidy,
                args=(jr_str,),
                name='copy_jr_'+jr_str
            )
        )
        continue
    start_thread_list(thread_list)
    pass
