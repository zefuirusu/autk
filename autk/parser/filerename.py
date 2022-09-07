#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import shutil
def suffix(suffix_str,filedir):
    path_list=[]
    for filename in os.listdir(filedir):
        file_path=os.path.abspath(
            os.path.join(
                filedir,
                filename))
        path_list.append(
            file_path
        )
    def single_rename(file_path):
        filename=file_path.split(os.sep)[-1]
        cur_pure_name=re.sub(r'\..*$','',filename)
        new_pure_name=''
    pass
if __name__=='__main__':
    pass
