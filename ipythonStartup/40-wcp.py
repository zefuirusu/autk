#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
from autk import get_time_info
# default_todir=os.path.abspath(os.curdir)
def wcp(frdir,todir=os.path.abspath(os.curdir),nickName=get_time_info()):
    '''
    frdir is the 'from' directory, todir is the 'to' directory.
    easy copy function using with the find function and then yelling out a big wocao.
    works well with the find function.
    '''
    pass
    file_name='-'.join([nickName,str(frdir.split(os.sep)[-1])])
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
