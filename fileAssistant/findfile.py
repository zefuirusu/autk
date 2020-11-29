#!/usr/bin/env python
# coding=utf-8
'''
run this script and search file on your disk with regular expression.
Find files with Regular Expression：正则表达式搜索本地文件/文件夹
'''
# import time
import os
print('Current Directory:')
print(os.path.abspath(os.curdir))
#
def findfile(item,fdir=os.path.abspath(os.curdir),match=False):
    '''
    Find the file you need in a directory.
    Regular Expression is supported.
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
    if rs_file==[]:
        print(r"Can't find any files!")
    else:
        pass
    if rs_dir==[]:
        print(r"Can't find any folders!")
    else:
        pass
    rs=[rs_file,rs_dir]
    return rs
#
def startloop():
    resu=findfile(item,fdir,match=mth)
    print('='*5,'files found:','='*5)
    ct=1
    for i in resu[0]:
        singlefile=[i.split(os.sep)[-1],i]
        print('-->',ct,'-'*10)
        print('\t',singlefile[0])
        print('\t'*2,singlefile[1])
        ct+=1
    #
    print('='*5,'file search finished!','='*5)
    print('='*5,'folders found:','='*5)
    ct=1
    for i in resu[1]:
        # singlefile=[i.split(os.sep)[-1],i]
        print('-->',ct,'-'*10)
        print('\t',i)
        # print(singlefile[0])
        # print(singlefile[1])
        ct+=1
    #
    print('='*5,'folders search finished!','='*5)
    return
#
if __name__=='__main__':
# set the directory to search:
    fdir=r'D:\\skandha\\a-Project\\TangShanProject'
# define the search mode:
    mth=input(r'>>> whether in match mode(y/n; default no.):')
    if mth == r'y':
        mth=True
        print('you must match the whole string.')
    else:
        mth=False
        print('no need to match the whole string.')
    print('\n'*1)
    #
# type in search string:
    item=input(r'>>> type in regular expression to search:')
# start searching:
    while True:
        print('\n','-'*3,r'Search Description','-'*5)
        print(r'search item:',item)
        print(r'search in this path as project root directory:',fdir)
        print('-'*3,r'Search Description','-'*5,'\n')
        startloop()
        item=input(r'>>> type in regular expression to search:')
        if item==r'exit' or len(item)==0:
            break
        else:
            # print('\n')
            continue
    return
    # input("Press <enter> to close the window...")

