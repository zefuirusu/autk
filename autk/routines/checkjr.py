#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pandas import DataFrame,concat
from autk import find_regex,f2list,save_df,relative_path
def update_jr_status(
    jrli_path, # file path of journal entry id list;
    sdir, # search directory;
    version_str, # name of the output sheet;
    savepath, # file path of the output Excel file;
    relative=False, # whether to export relative path;
    ref_path=None # to what base path does the output relative path relative to?
):
    if ref_path is None:
        ref_path=savepath
    haveli=[]
    noli=[]
    jrli=f2list(jrli_path)
    for jr in jrli:
        search_resu=find_regex(jr,sdir)[0]
        if len(search_resu)==0:
            noli.append([jr,0])
        elif len(search_resu)==1:
            if relative==True:
                haveli.append(
                    [jr,relative_path(
                            search_resu[0],
                            ref_path)]
                )
            else:
                haveli.append([jr,search_resu[0]])
        elif len(search_resu)>1:
            if relative==False:
                haveli.append(
                    [jr,';'.join(search_resu)]
                )
            else:
                multi_resu=[]
                for single_resu in search_resu:
                    multi_resu.append(
                        relative_path(single_resu,ref_path)
                    )
                haveli.append(
                    [jr,';'.join(multi_resu)]
                )
        else:
            pass
        continue
    print('we have %d:'%len(haveli),haveli)
    print('not have %d:'%len(noli),noli)
    d_have=DataFrame(haveli,columns=['jrid','location'])
    d_have['status']='√'
    d_no=DataFrame(noli,columns=['jrid','location'])
    d_no['status']='×'
    d=concat([d_have,d_no],axis=0,join='outer')
    d.sort_values(
        'jrid',
        ascending=True,
        inplace=True,
        ignore_index=True
    )
    print(d)
    save_df(d,version_str,savepath)
    return
if __name__=='__main__':
    pass
