#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pandas import DataFrame,concat
from autk.parser.findfile import find_regex
from autk.parser.funcs import f2list,save_df,relative_path
def locate_by_func(
    version_str, # sheet name
    by_func, # to transform glid into glid_item; one parameter;
    jrli_path, # file path of journal entry id (in regex form) list; list can be passed as well;
    sdir, # search directory;
    savepath, # file path of the output Excel file;
    relative=False, # whether to export relative path;
    ref_path=None, # to what base path does the output relative path relative to?
    dir_resu=False
):
    '''
    Input which jrs to find by file at `jrli_path`; 
    Tansform jrs into regular expression through `by_func`;
    Search jrs by regex in `sdir`;
    Save location-mapping results into Excel at `savepath`
    whose sheet name is `version_str`;
    `relative:bool` determines whether results are relative path
    from `ref_path`;
    `dir_resu` determines whether to search directory
    in `sdir`; if False, search files.
    Output data looks like:
    ________________________________
    |glid|glid_item|location|status|
    |----|---------|--------|------|
    ________________________________
    Output data will be sort by column 'glid';
    '''
    if ref_path is None:
        ref_path=savepath
    haveli=[]
    noli=[]
    from os.path import isfile,isdir
    if isinstance(jrli_path,list):
        jrli=jrli_path
    elif isfile(jrli_path):
        jrli=f2list(jrli_path)
    else:
        print('check argument:jrli_path')
        jrli=[]
        pass
    for raw_jr in jrli:
        jr=by_func(raw_jr)
        if dir_resu==True:
            search_resu=find_regex(jr,sdir)[1]
        else:
            search_resu=find_regex(jr,sdir)[0]
        if len(search_resu)==0:
            noli.append([raw_jr,jr,0])
        elif len(search_resu)==1:
            if relative==False:
                haveli.append([raw_jr,jr,search_resu[0]])
            else:
                haveli.append(
                    [
                        raw_jr,
                        jr,
                        relative_path(
                            search_resu[0],
                            ref_path)
                     ]
                )
        elif len(search_resu)>1:
            if relative==False:
                haveli.append(
                    [raw_jr,jr,';'.join(search_resu)]
                )
            else:
                multi_resu=[]
                for single_resu in search_resu:
                    multi_resu.append(
                        relative_path(single_resu,ref_path)
                    )
                haveli.append(
                    [raw_jr,jr,';'.join(multi_resu)]
                )
        else:
            pass
        continue
    print('we have %d:'%len(haveli),haveli)
    print('not have %d:'%len(noli),noli)
    d_have=DataFrame(haveli,columns=['glid','glid_item','location'])
    d_have['status']='√'
    d_no=DataFrame(noli,columns=['glid','glid_item','location'])
    d_no['status']='×'
    d=concat([d_have,d_no],axis=0,join='outer')
    d.sort_values(
        'glid',
        ascending=True,
        inplace=True,
        ignore_index=True
    )
    print(d)
    save_df(d,version_str,savepath)
    return d
def update_jr_status(
    version_str, # name of the output sheet;
    jrli_path, # file path of journal entry id (in regex form) list; list can be passed as well;
    sdir, # search directory;
    savepath, # file path of the output Excel file;
    relative=False, # whether to export relative path;
    ref_path=None, # to what base path does the output relative path relative to?
    dir_resu=False
):
    if ref_path is None:
        ref_path=savepath
    haveli=[]
    noli=[]
    from os.path import isfile,isdir
    if isinstance(jrli_path,list):
        jrli=jrli_path
    elif isfile(jrli_path):
        jrli=f2list(jrli_path)
    else:
        print('check argument:jrli_path')
        jrli=[]
    for jr in jrli:
        if dir_resu==True:
            search_resu=find_regex(jr,sdir)[1]
        else:
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
    d_have=DataFrame(haveli,columns=['glid_item','location'])
    d_have['status']='√'
    d_no=DataFrame(noli,columns=['glid_item','location'])
    d_no['status']='×'
    d=concat([d_have,d_no],axis=0,join='outer')
    d.sort_values(
        'glid_item',
        ascending=True,
        inplace=True,
        ignore_index=True
    )
    print(d)
    save_df(d,version_str,savepath)
    return
if __name__=='__main__':
    pass
