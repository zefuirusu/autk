#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pandas import DataFrame
from autk.reader.base.xlbk import XlBook
from autk.parser.pca import ClusterPca
c1=ClusterPca()
bk=XlBook('./data/hs_manufacture2021.xlsx')
cols=list(bk.select_matrix(
    '152-2-1制造费用分月分项目明细',
    (9,1),(33,1),
    type_df=False,
    has_title=False
).T[0])
manu_data=bk.select_matrix(
    '152-2-1制造费用分月分项目明细',
    (9,2),(33,13),
    type_df=False,
    has_title=False
).T
#  c1.simple_pca(
    #  DataFrame(
        #  data=manu_data,
        #  columns=cols
    #  )
#  )
manu_data=DataFrame(
    manu_data,
    columns=cols
)
manu_data.fillna(0.0)
c1.load_matrix(manu_data)
c1.cov_pca()
if __name__=='__main__':
    pass
