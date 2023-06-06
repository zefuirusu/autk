#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pandas import DataFrame,Series,concat

from autk.parser.funcs import f2list,save_df,relative_path
from autk.handf.findfile import find_regex

def locate_by_func(
    by_func, # to transform glid into glid_item; one parameter;
    jrli_path, # file path of journal entry id (in string form) list; list can be passed as well;
    sdir, # search directory;
    relative=False, # whether to export relative path;
    ref_path=None, # to what base path does the output relative path relative to?
):
    '''
    Input jrs to search by file at `jrli_path`; 
    Tansform jrs into regular expression through `by_func`;
    Search jrs-regex in `sdir`;
    `relative:bool` determines whether results are relative
    from `ref_path`, if true, you must provide `ref_path`;
    Output data looks like:
    _________________________________________
    |glid|regex|file|directory|fcount|dcount|
    |----|-----|----|---------|-----|-------|
    -----------------------------------------
    Output data will be sort by column 'glid';
    '''
    from os.path import isfile,isdir
    if relative==True and ref_path is None:
        print('check argument: ref_path')
        return
    if isinstance(jrli_path,list):
        jrli=jrli_path
    elif isfile(jrli_path):
        jrli=f2list(jrli_path)
    else:
        print('check argument:jrli_path')
        return
    resu_df=DataFrame(
        [],
        index=jrli,
        columns=[
            'glid',
            'regex',
            'file',#'location',
            'directory',
            'fcount',#'count',
            'dcount'
        ]
    )
    def rel_path_list(path_list):
        # list of relative_path;
        return [
            relative_path(p,ref_path) for p in path_list
        ]
    def parse_result(count,results):
        if count==0:
            location=''
        elif count==1:
            location=results[0] if relative==False else relative_path(results[0],ref_path)
        elif count>1:
            location=';'.join(results) if relative==False else ';'.join(rel_path_list(results))
        else:
            pass
        return location
    for raw_jr in resu_df.index:
        jr=by_func(raw_jr) # regex for raw_jr
        f_resu=find_regex(jr,sdir)[0]
        d_resu=find_regex(jr,sdir)[1]
        fcount=len(f_resu)
        dcount=len(d_resu)
        resu_df.loc[raw_jr,:]=Series(
            [
                raw_jr,
                jr,
                parse_result(fcount,f_resu),
                parse_result(dcount,d_resu),
                fcount,
                dcount
            ],
            index=resu_df.columns
        )
        continue
    resu_df.sort_values(
        'glid',
        ascending=True,
        inplace=True,
        ignore_index=False
    )
    return resu_df
def update_jr_status(
    version_str, # name of the output sheet;
    jrli_path, # file path of journal entry id (in regex form) list; list can be passed as well;
    sdir, # search directory;
    savepath, # file path of the output Excel file;
    relative=False, # whether to export relative path;
    ref_path=None, # to what base path does the output relative path relative to?
    dir_resu=False
):
    '''
    This function will be deprecated soon;
    May be fixed as well;
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
