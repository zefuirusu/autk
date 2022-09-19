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
        continue
    print(path_list)
    def single_rename(file_path):
        filename=file_path.split(os.sep)[-1]
        cur_pure_name=re.sub(r'\..*$','',filename)
        extension_str=re.sub(r'^.*\.','',filename)
        new_path=os.path.join(
            os.sep.join(
                file_path.split(os.sep)[0:-1]
            ),
            ''.join([
                cur_pure_name,
                '-',suffix_str,
                '.',extension_str
            ])
        )
        print('current name:',file_path)
        print('new name',new_path)
        shutil.move(file_path,new_path)
        pass
    for file in path_list:
        single_rename(file)
        continue
    pass
if __name__=='__main__':
    pass
