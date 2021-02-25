#!/usr/bin/env python
# coding=utf-8
import os
import sys
from .financialtk.modules.mortalGL import MGL
sys.path.append(os.path.abspath(os.curdir))
def mgl(fpath='',shtna='Sheet1',title=0,glid_index=[]):
    return MGL.__init__(fpath='',shtna='Sheet1',title=0,glid_index=[])
