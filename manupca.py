#!/home/sk008/.local/skpyenv/bin/python3
# -*- coding: utf-8 -*-

from autk.reader.base.xlbk import XlBook
from autk.parser.pca import ClusterPca
c1=ClusterPca()
manu_data=XlBook(
    './data/hs_manufacture2021.xlsx'
).select_matrix(
    '152-2-1制造费用分月分项目明细',
    (9,2),(33,13),
    type_df=False,
    has_title=False
)
print(manu_data.sum())
if __name__=='__main__':
    pass
