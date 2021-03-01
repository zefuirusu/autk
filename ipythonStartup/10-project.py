#!/usr/bin/env python
# coding=utf-8
import os
class Prj:
    def __init__(self,prj_name,basedir):
        self.prj_name=prj_name
        self.basedir=basedir
        self.top_dir=[
            '10-push',
            '20-collection',
            '30-previousRef',
            '40-script',
            '80-expense',
            '90-backup',
            '90-trash'
        ]
        pass
def startprj(prj_name,basedir=os.path.abspath(os.curdir)):
    top_dir=[
        '10-push',
        '20-collection',
        '30-previousRef',
        '40-script',
        '80-expense',
        '90-backup',
        '90-trash'
    ]
    prj_dir=os.path.join(basedir,prj_name)
    os.mkdir(prj_dir)
    for i in top_dir:
        os.mkdir(os.path.join(prj_dir,i))
    pass
if __name__=='__main__':
    print('functions in 10-project:')
    print(['startprj'])
    pass
