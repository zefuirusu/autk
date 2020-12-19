#!/usr/bin/env python
# coding=utf-8
'''
Plan before sampling.
'''
class PreScan:
    def __init__(self,wshtdir):
        '''
        Working Sheet Directory is acquired.
        '''
        self.wshtdir=wshtdir
        return
    def walk(self):
        import os
        import re
        for i,j,k in os.walk(self.wshtdir):
            for na in k:
                regitem=re.compile(r'xls[xm]$')
                if re.search(regitem,na) != None:
                    fpath=os.path.abspath(os.path.join(i,na))
                    # print('-'*5)
                    # print(fpath)
                    # print(na)
                    yield fpath
                    pass
                else:
                    pass
        return
    def scan(self):
        import re
        from openpyxl import load_workbook
        from pandas import read_excel
        fileli=self.walk()
        for i in fileli:
            wb=load_workbook(i,keep_vba=True)
            shtli=wb.sheetnames
            # print(shtli)
            for j in shtli:
                if re.search('审定',j) !=None:
                    print(j)
                    ws=wb.get_sheet_by_name(j)
                    print(ws)
                    for n in range(19,25):
                        for m in range(1,10):
                            print(ws.cell(n,1).value)
                            # print(read_excel(i,sheet_name=j).iloc[19,1])
                        continue
                    pass
                else:
                    # print('failed!')
                    pass
            continue
        return
