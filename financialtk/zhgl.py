#!/usr/bin/env python
# coding=utf-8
'''
从审计系统里读取账套数据，查询凭证，导出Excel之后，进行抽象，得到zhgl类。
'''
class ChartOfAccount:
    '''
    Chart of Account is a table where you can get reference from Account ID to Account Name.
    会计科目表,可以对应查找科目名称与科目编码。
    '''
    def __init__(self,filedir=''):
        self.filedir=filedir
        return
    def getid(acc_name):
        pass
    def getna(acc_id):
        pass
class Acct:
    def __init__(self,name='主营业务收入',accid=r'6001'):
        '''
        初始化，传入科目名称，科目编码，增加方向，账户类别。
        '''
        self.name=name # 科目名称
        self.accid=str(accid) # 科目编码
        self.isdr=True # 借方主导的科目,共同类科目也归入此类。
        self.iscr=-self.isdr # 贷方主导的科目
        self.cata='' # account catagory
class zhgl:
    '''
    General Ledgers in a sheet from an Excel Workbook.
    Default sheet name is '表页-1'.
    '''
    def __init__(self,fdir,shtna=r'表页-1',title=3):
        self.fdir=fdir
        self.sheetname=shtna
        self.title=title
        # glid 是GL的主键。
        self.columnsk=['凭证日期', '字', '号', '摘要', 'glid', '科目编号', '科目全路径', '借方发生金额', '贷方发生金额', '汇率', '外币金额', '外币名称', '数量额', '单价', '计量单位', '核算编号', '核算名称']
        self.columns=['凭证日期', '字', '号', '摘要', '科目编号', '科目全路径', '借方发生金额', '贷方发生金额', '汇率', '外币金额', '外币名称', '数量额', '单价', '计量单位', '核算编号', '核算名称']
        print('GL初始化之前，需要手动添加glid列。')
        return
    def getdata(self):
        from pandas import read_excel
        d1=read_excel(self.fdir,sheet_name=self.sheetname,header=self.title)
        # self.columns=list(d1.columns)
        d1.dtypes[5]='string'
        # print(d1.dtypes)
        return d1
    # @classmethod
    def filter(self,regitem,label=r'',match=False):
        '''
        filter the specific column of the table by regular expression.
        '''
        import re
        indf=self.getdata()
        reg=re.compile(regitem)
        fli=[]
        for i in list(indf[label].drop_duplicates()):
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
            ftable_fake=indf[indf[label]==j]
#             print(ftable_fake)
            ftable=concat([ftable,ftable_fake],join='outer',axis=0)
        return ftable
    def refilter(self,indf,regitem,label=r'',match=False):
        '''
        filter the specific column of a input table by regular expression.
        '''
        import re
        reg=re.compile(regitem)
        fli=[]
        for i in list(indf[label].drop_duplicates()):
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
        # ftable=DataFrame([])
        tableli=[]
        for j in fli:
            ftable_fake=indf[indf[label]==j]
#             print(ftable_fake)
            # ftable=concat([ftable,ftable_fake],join='outer',axis=0)
            tableli.append(ftable_fake)
            continue
        ftable=concat(tableli,axis=0,join='outer')
        return ftable
    def salaryana(self):
        salary_id=r'2211'
        expense_id=['6601','6602','5001','5301','2211','1604']
        def transReg(accid):
            return str(r'^')+str(accid)+str(r'.*')
        s1=self.filter(transReg(salary_id),label=r'科目编号')
        # s1=self.refilter(s1,'0','借方发生金额')
        s1=s1[s1['借方发生金额']==0.0]
        eli=[]
        for i in expense_id:
            print('-·'*5)
            print('filtering %s'%i)
            e1=self.filter(transReg(i),label=r'科目编号')
            if e1.shape[0]==0:
                print('no results after filter: %s'%i)
                pass
            else:
                # print(e1.columns)
                # e1=self.refilter(e1,'0','贷方发生金额')
                e1=e1[e1['贷方发生金额']==0.0]
                eli.append(e1)
            continue
        from pandas import concat,pivot_table
        e_concat=concat(eli,axis=0,join='outer')
        salaryTable=concat([s1,e_concat],axis=0,join='outer')
        # sumtable=pivot_table(salaryTable,values=['借方发生金额','贷方发生金额'],index='科目编号',columns=['借方发生金额'],aggfunc='sum')
        sumtable1=pivot_table(salaryTable,values=['借方发生金额'],index='科目编号',columns=[],aggfunc='sum')
        print(sumtable1.sum(axis=0))
        sumtable2=pivot_table(salaryTable,values=['贷方发生金额'],index='科目编号',columns=[],aggfunc='sum')
        print(sumtable2.sum(axis=0))
        print(sumtable2.sum(axis=0)-sumtable1.sum(axis=0))
        for i in list(salaryTable['GLID'].drop_duplicates()):
            dr_sum=(pivot_table(salaryTable[salaryTable['GLID']==i],values=['借方发生金额'],index=['GLID'],columns=[],aggfunc='sum'))
            cr_sum=(pivot_table(salaryTable[salaryTable['GLID']==i],values=['贷方发生金额'],index=['GLID'],columns=[],aggfunc='sum'))
            # print(dr_sum)
            # print(cr_sum)
            drcrdif=(dr_sum.sum(axis=0)['借方发生金额']-cr_sum.sum(axis=0)['贷方发生金额'])
            if drcrdif != 0:
                # print('='*5)
                print(i)
                # print(dr_sum)
                # print(cr_sum)
        return 
    # def getAccGl(self,accid):
    #     regitem=str(accid)
    #     km=self.filter(accid,r'科目编码') # km is the Chinese Phonetical Alphabets "Ke Mu".
    #     idli=list(km['glid'].drop_duplicates())
    #     def itersearch(idli):
    #         for i in idli:
    #             yield gl.filter(i,'glid')
    #     resu=pd.concat(itersearch(idli),axis=0,join='outer')
    #     return resu
