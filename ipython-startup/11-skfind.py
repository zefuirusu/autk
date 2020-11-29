#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
#
def wtlog(logline,logdir):
    '''
    writing printing log file.
    logline is what you write and logdir is the log file location.
    '''
    with open(logdir,mode='a',encoding = 'utf-8') as f:
        f.write(logline)
        f.write('\n')
    return
#
def skfind(item,fdir=os.path.abspath(os.curdir),match=False):
    '''
    Find the file you need in a directory (default current directory).
    Regular Expression is supported.
    return a multi-dimensional list like:
    results=[file list, folder list]
    '''
    # import os
    import re
    rs_file=[]
    rs_dir=[]
    for i,j,k in os.walk(fdir):
        for na in k:
            if match==True:
                regitem=re.compile(item)
                d=re.match(regitem,na)
                if d is not None:
                    rs_file.append(os.path.abspath(os.path.join(i,na)))
            else:
                regitem=re.compile(item)
                d=re.search(regitem,na)
                if d is not None:
                    real_na=os.path.join(i,na)
                    # real_na=re.sub(re.compile(r'\s+'),r'',real_na)
                    rs_file.append(os.path.abspath(real_na))
        for fpath in j:
            if match==True:
                regitem=re.compile(item)
                d=re.match(regitem,fpath)
                if d is not None:
                    full_fpath=os.path.abspath(fpath)
                    # full_fpath=re.sub(re.compile(r'\s+'),r'',full_fpath)
                    rs_dir.append(full_fpath)
                    # rs_dir.append(fpath)
            else:
                regitem=re.compile(item)
                d=re.search(regitem,fpath)
                if d is not None:
                    rs_dir.append(os.path.abspath(os.path.join(i,fpath)))
                    # rs_dir.append(fpath)
    # if rs_file==[]:
    #     pass
    #     print(r"Can't find any files!")
    # else:
    #     pass
    # if rs_dir==[]:
    #     pass
    #     print(r"Can't find any folders!")
    # else:
    #     pass
    rs=[rs_file,rs_dir]
    return rs
#
tpdir=r'D:\skandha\a-Project\zhongTang'
def findfi(st):
    '''
    find files in TangShanProject directory.
    '''
    rs=skfind(st,tpdir)
    rs=rs[0]
    print(rs)
    pass
    return rs
def findfo(st):
    '''
    find folders in TangShanProject directory.
    '''
    rs=skfind(st,tpdir)
    rs=rs[1]
    print(rs)
    pass
    return rs
#
def find(item,fdir=os.path.abspath(os.curdir),match=False):
    '''
    Find the file you need in a directory (default current directory).
    Regular Expression is supported.
    return a multi-dimensional list like:
    results=[file list, folder list]
    '''
    # import os
    import re
    rs_file=[]
    rs_dir=[]
    for i,j,k in os.walk(fdir):
        for na in k:
            if match==True:
                regitem=re.compile(item)
                d=re.match(regitem,na)
                if d is not None:
                    rs_file.append(os.path.abspath(os.path.join(i,na)))
            else:
                regitem=re.compile(item)
                d=re.search(regitem,na)
                if d is not None:
                    real_na=os.path.join(i,na)
                    # real_na=re.sub(re.compile(r'\s+'),r'',real_na)
                    rs_file.append(os.path.abspath(real_na))
        for fpath in j:
            if match==True:
                regitem=re.compile(item)
                d=re.match(regitem,fpath)
                if d is not None:
                    full_fpath=os.path.abspath(fpath)
                    # full_fpath=re.sub(re.compile(r'\s+'),r'',full_fpath)
                    rs_dir.append(full_fpath)
                    # rs_dir.append(fpath)
            else:
                regitem=re.compile(item)
                d=re.search(regitem,fpath)
                if d is not None:
                    rs_dir.append(os.path.abspath(os.path.join(i,fpath)))
                    # rs_dir.append(fpath)
    # if rs_file==[]:
    #     pass
    #     print(r"Can't find any files!")
    # else:
    #     pass
    # if rs_dir==[]:
    #     pass
    #     print(r"Can't find any folders!")
    # else:
    #     pass
    rs=[rs_file,rs_dir]
    return rs
#
