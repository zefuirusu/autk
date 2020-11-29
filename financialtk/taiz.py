#!/usr/bin/env python
# coding=utf-8
class findata:
    # __slots__=('fdir','shtna','title')
    def __init__(self,infoli=[]):
        '''
        infoli is a list whose length is 3, elements in which are String, String, and Integer.
        '''
        if len(infoli) !=3:
            print('Error:length of infoli must be 3.')
        else:
            self.fdir=infoli[0]
            self.shtna=infoli[1]
            self.title=infoli[2]
        return
class taiz:
    def __init__(self,sourcedata):
        self.srdata=sourcedata
        self.regtitle=['省份','地市','区域']
        self.datatitle=['收款金额','开票金额','应确认收入金额']
        self.fltitle=['会计主体','收入归属年份','类型','收款渠道','开票类型']
        return
    def getdata(self):
        from pandas import read_excel
        return read_excel(self.srdata.fdir,sheet_name=self.srdata.shtna,header=self.srdata.title)
    def filter(self,regitem,label=r'',match=False):
        '''
        filter the specific column of the table by regular expression.
        '''
        import re
        self.data=self.getdata()
        reg=re.compile(regitem)
        fli=[]
        for i in list(self.data[label].drop_duplicates()):
            if match==False:
                b=re.search(reg,str(i))
            else:
                b=re.match(reg,str(i))
            if b != None:
#                 print(b,i)
                fli.append(i)
            else:
                pass
#         print(fli)
        from pandas import DataFrame,concat
        ftable=DataFrame([])
        for j in fli:
            ftable_fake=self.data[self.data[label]==j]
#             print(ftable_fake)
            ftable=concat([ftable,ftable_fake],join='outer',axis=0)
        return ftable
def getjoin(tinfo1,tinfo2):
    if type(tinfo1)==list and len(tinfo1)==3:
        print('tinfo1 is OK!')
    else:
        print('invalid argument tinfo1!')
        pass
    if type(tinfo2)==list and len(tinfo2)==3:
        print('tinfo2 is OK!')
    else:
        print('invalid argument tinfo2!')
        pass
    f1=findata(tinfo1)
    f2=findata(tinfo2)
    t1=taiz(f1).getdata()
    t2=taiz(f2).getdata()
    from pandas import concat
    t3=concat([t1,t2],axis=0,join='outer')
    return t3
#
def getdif(df1,df2,label=[''],tolerance=3):
    '''
    df1 and df2 are two DataFrames who have columns in common, in which label is included.
    tolerance.
    '''
    dif=df1[label]-df2[label]
    dif_1=dif[dif[label]>tolerance]
    dif_2=dif[dif[label]<-tolerance]
    from pandas import concat
    dif_final=concat([dif_1,dif_2],axis=0,join='outer')
    return dif_final
