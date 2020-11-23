#!/usr/bin/env python
# -*- coding: utf-8 -*-
import shutil
import os
default_todir=os.path.abspath(os.curdir)
def wcp(frdir,todir=default_todir,nickName=r''):
    '''
    frdir is the 'from' directory, todir is the 'to' directory.
    easy copy function using with the find function and then yelling out a big wocao.
    works well with the find function.
    '''
    pass
    file_name=str(frdir.split(os.sep)[-1]+nickName)
    destination_dir=os.path.abspath(os.path.join(todir,file_name))
    try:
        shutil.copy(frdir,destination_dir)
    except:
        shutil.copytree(frdir,destination_dir)
    else:
        pass
    finally:
        print('%s is copied.'%frdir)
    return
