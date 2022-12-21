#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from os.path import isdir,isfile,join
from threading import Thread
from autk.parser.funcs import save_df
from autk.mapper.map import SampleEglMap
from autk.reader.mortal.mortalgl import MGL
class CashFlow:
    def __init__(self,mgl,output_dir):
        self.mgl=mgl
        self.savepath=join(output_dir,r'cashflow_'+mgl.name+r'.xlsx')
        pass
    def load_mgl(self,other_mgl):
        self.mgl=other_mgl
    def new_savedir(self,output_dir):
        self.savepath=join(output_dir,r'cashflow_'+self.mgl.name+r'.xlsx')
    def start(self,cash_accid_item=r'^100[12].*$'):
        def __start_thread(cash_accid_item):
            print(self.mgl.scan_byid(cash_accid_item))
            cash_df=self.mgl.getAcct(cash_accid_item)
            pure_cash_df=self.mgl.getAcct(cash_accid_item,pure=True)
            dr=self.mgl.side_split(cash_accid_item,'dr')
            cr=self.mgl.side_split(cash_accid_item,'cr')
            print(dr)
            print(cr)
            save_df(cash_df,'cash_df',self.savepath)
            save_df(pure_cash_df,'pure_cash',self.savepath)
            save_df(dr,'dr_split',self.savepath)
            save_df(cr,'cr_split',self.savepath)
            pass
        t=Thread(
            target=__start_thread,
            args=(cash_accid_item,),
            name='cash_flow_thread_of_'+self.mgl.name
        )
        t.start()
        t.join()
        pass
    pass
class AcctAnalysis:
    '''
    Not perfect yet.
    Planning to update self.rev_analysis,cost_analysis, and salary_analysis with self.cr_analysis and self.dr_analysis, like self.research_analysis.
    class autk.reader.MGL must use xlmap;
    ----------
    Account Groups -> Account Cycles -> Analysis;
    '''
    def __init__(self,mgl,savepath=None):
        print('---Initializing Analysis---')
        t_start=datetime.datetime.now()
        self.mgl=mgl
        self.xlmap=self.mgl.xlmap
        self.acctmap=self.mgl.acctmap
        self.savepath=savepath
        self._cr_temp_sum=[]
        self._dr_temp_sum=[]
        self.group_regex_map={
            'cash':['银行存款',r'(库存)?现金'],
            'other_pr':[r'其他应[收付]款',],
            'receive':[r'(?<!其他)应收账?款项?',r'预收账?款项?'],
            'revenue':[r'(主?营|其他)业务?收入'],
            'salary':[r'(应付)?职工薪酬|应付工资'],
            'pay':[r'(?<!(其他|长期))应付账?款项?|应付票据',r'预付账?款项?'],
            'material':['原材料','辅料','周转材料','低值易耗品'],
            'production':['生产成本'],
            'manufacture':['制造费用'],
            'goods':['库存商品','存货跌价准备'],
            'cogs':[r'主?营业务?成本|其他业务(成本|支出)'],
            'expense':[r'(销售|营业)费用'],
            'research':[r'[研开]发(费用|支出)'],
            'tax':['所得税(费用)?',r'递延所得税(资产|负债)']
        }
        self.__parse_acct()
        self.__parse_cycle()
        t_end=datetime.datetime.now()
        t_interval=t_end-t_start
        print('Initialize time spent:',t_interval)
        print('---Analysis Initialized ---')
        pass
    def __clear_temp(self):
        self._cr_temp_sum=[]
        self._dr_temp_sum=[]
        pass
    def __show_temp(self):
        print(
            'credit:',
            sum(self._cr_temp_sum),
            'debit:',
            sum(self._dr_temp_sum)
        )
        pass
    def __parse_acct(self):
        def prepare_single(attr_na):
            print('parsing %s ...'%attr_na)
            fake_attr=r'_'+attr_na
            setattr(self,fake_attr,{})
            regitems=self.group_regex_map[attr_na]
            for reg_str in regitems:
                temp_attr=getattr(self,fake_attr)
                temp_attr.update(
                    {**self.mgl.whatna(reg_str)}
                )
                setattr(self,fake_attr,temp_attr)
            setattr(
                self,
                attr_na,
                list(
                    getattr(self,fake_attr).keys()
                )
            )
            pass
        attr_names=list(self.group_regex_map.keys())
        thread_list=[]
        for attr_na in attr_names:
            t=Thread(target=prepare_single,args=(attr_na,),name=str(attr_na))
            thread_list.append(t)
            pass
        for t in thread_list:
            t.start()
        for t in thread_list:
            t.join()
    def __parse_cycle(self):
        #  cash cycle
        self.cash_cycle=self.cash
        __top_cash_cycle=list(map(lambda accid:accid[0:4],self.cash_cycle))
        self.top_cash_cycle=list(set(__top_cash_cycle))
        self.top_cash_cycle.sort()
        #  sales and collection cycle:
        self.sale_cycle=self.revenue+self.receive+self.cash
        __top_sale_cycle=list(map(lambda accid:accid[0:4],self.sale_cycle))
        self.top_sale_cycle=list(set(__top_sale_cycle))
        self.top_sale_cycle.sort()
        #  acquisition and payment cycle; inventory and warehousing cycle:
        self.cost_cycle=self.cash+self.salary+self.pay+self.material+self.manufacture+self.production+self.goods+self.cogs
        __top_cost_cycle=list(map(lambda accid:accid[0:4],self.cost_cycle))
        self.top_cost_cycle=list(set(__top_cost_cycle))
        self.top_cost_cycle.sort()
        #  salary and human resource cycle:
        self.salary_cycle=self.salary+self.expense+self.research
        __top_salary_cycle=list(map(lambda accid:accid[0:4],self.salary_cycle))
        self.top_salary_cycle=list(set(__top_salary_cycle))
        self.top_salary_cycle.sort()
        pass
    def caltable(self):
        cal_unit=self.mgl.caltable(use_meta=False)
        return cal_unit
    def calxl(self,df):
        xl=self.mgl.calxl()
        xl.accept_data(df)
        return xl
    def quick_start(self,cycle_name='top_cost_cycle',save=False):
        '''
        Start MGL.multi_acct_analysis for top acct cycle;
        parameter:
            cycle_name:
                cycle_name must one of names defined in method AcctAnalysis.__parse_cycle();
                str,cycle_name='top_cost_cycle','top_sale_cycle','top_cash_cycle', or 'top_salary_cycle',etc;
        return:
            None, but analysis result will be saved;
        '''
        #  MGL.multi_acct_analysis(accid_list,label=None,save=False,savepath='./',nick_name='multi_acct',multi_thread=False)
        self.mgl.multi_acct_analysis(
            getattr(self,cycle_name),
            label=None,
            save=save,
            savepath=self.savepath,
            nick_name=cycle_name
        )
        pass
    def start_cr2dr(self,cr,dr,accurate=True):
        sheet_name='-'.join([cr,dr])
        df=self.mgl.correspond(cr,dr,accurate=accurate)
        if df.shape[0] != 0:
            print('-'*5,'analysis:',self.acctmap[cr],'->',self.acctmap[dr],'-'*5)
            [cr_sum,dr_sum]=self.mgl.cor_sum(cr,dr,accurate=accurate)
            if cr_sum>dr_sum:
                print('[Warning] Credit > Debit!',cr_sum,dr_sum)
            print(
                "\n",
                "credit:\n\t",
                cr,":",cr_sum,"\n",
                "debit:\n\t",
                dr,":",dr_sum,"\n",
            )
            self._cr_temp_sum.append(cr_sum)
            self._dr_temp_sum.append(dr_sum)
            print(df)
            if (
                    self.savepath is None 
                    or not isfile(self.savepath) 
                    or not isdir(self.savepath)
            ):
                pass
            elif (
                isfile(self.savepath) 
                or isdir(self.savepath) 
                or isinstance(self.savepath,str)
            ):
                save_df(
                    df,
                    sheet_name=sheet_name,
                    save_path=self.savepath,
                    file_nickname='analysis'
                )
            else:
                pass
        else:
            print('[Warning] Empty data:',df.shape)
            pass
        xl=self.calxl(df)
        return xl
    def cr_analysis(self,cr_list,dr_list,accurate):
        print('\ncr_list:\n\t',cr_list)
        print('\ndr_list:\n\t',dr_list)
        self.__clear_temp()
        key_glid_list=[]
        cal=self.caltable()
        for cr in cr_list:
            acct=self.mgl.getAcct(
                cr,
                accid_label=None,
                side='cr',
                pure=False,
                accurate=accurate
            )
            xl=self.calxl(acct)
            cal.xl_obj_set.append(xl)
            key_glid_list.extend(list(xl.data[self.mgl.key_name]))
        key_glid_list=list(set(key_glid_list))
        key_df=cal.filter_list(key_glid_list,self.mgl.key_name,over_write=True)
        key_dr_list=list(
            cal.filter(
                [[self.mgl.drcrdesc[0],'<>',0]],
                filter_type='num',
                over_write=False
            )[self.mgl.accid_col]
        )
        key_dr_list=list(set(key_dr_list))
        for cr in cr_list:
            for dr in dr_list:
                if dr in key_dr_list:
                    self.start_cr2dr(cr,dr,accurate)
                else:
                    pass
                continue
            continue
        self.__show_temp()
        pass
    def dr_analysis(self,cr_list,dr_list,accurate):
        print('\ncr_list:\n\t',cr_list)
        print('\ndr_list:\n\t',dr_list)
        self.__clear_temp()
        key_glid_list=[]
        cal=self.caltable()
        for dr in dr_list:
            acct=self.mgl.getAcct(dr,accid_label=None,side='dr',pure=False,accurate=accurate)
            xl=self.calxl(acct)
            cal.xl_obj_set.append(xl)
            key_glid_list.extend(list(xl.data[self.mgl.key_name]))
        key_glid_list=list(set(key_glid_list))
        key_df=cal.filter_list(key_glid_list,self.mgl.key_name,over_write=True)
        key_dr_list=list(
            cal.filter(
                [[self.mgl.drcrdesc[1],'<>',0]],
                filter_type='num',
                over_write=False
            )[self.mgl.accid_col]
        )
        key_dr_list=list(set(key_dr_list))
        for dr in dr_list:
            for cr in cr_list:
                if cr in key_dr_list:
                    self.start_cr2dr(cr,dr,accurate)
                else:
                    pass
                continue
            continue
        self.__show_temp()
        pass
    def rev_analysis(self,accurate=True):
        self.__clear_temp()
        for cr in self.revenue:
            for dr in self.receive:
                self.start_cr2dr(cr,dr,accurate=accurate)
        print('revenue -> receive\n')
        self.__show_temp()
        self.__clear_temp()
        for cr in self.receive:
            for dr in self.cash:
                self.start_cr2dr(cr,dr,accurate=accurate)
        print('receive -> cash\n')
        self.__show_temp()
        pass
    def cost_analysis(self,accurate=True):
        self.__clear_temp()
        for credit in self.pay:
            for debit in (self.material+self.manufacture):
                self.start_cr2dr(credit,debit,accurate=accurate)
        print('pay -> material/manufacture\n')
        self.__show_temp()
        self.__clear_temp()
        for credit in (self.material+self.salary+self.manufacture):
            for debit in self.production:
                self.start_cr2dr(credit,debit,accurate=accurate)
        print('material/salary/manufacture -> production\n')
        self.__show_temp()
        self.__clear_temp()
        for credit in self.production:
            for debit in self.goods:
                self.start_cr2dr(credit,debit,accurate=accurate)
        print('production-> goods\n')
        self.__show_temp()
        self.__clear_temp()
        for credit in (self.goods+self.material):
            for debit in self.cogs:
                self.start_cr2dr(credit,debit,accurate=accurate)
        print('goods/material -> cogs\n')
        self.__show_temp()
        pass
    def salary_analysis(self,accurate=True):
        print('\nsalary -> production/manufacture/expense/research\n')
        cr_list=self.salary
        dr_list=self.production+self.manufacture+self.expense+self.research
        if len(cr_list) != 0:
            self.cr_analysis(cr_list,dr_list,accurate)
        else:
            print('No salary accounts to analysis!')
        # the following is out-of-date, will be deleted soon:
        #  self.__clear_temp()
        #  for cr in self.salary:
            #  for dr in (self.production+self.manufacture+self.expense+self.research):
                #  self.start_cr2dr(cr,dr,accurate=accurate)
        #  print('salary -> production/manufacture/expense/research\n')
        #  self.__show_temp()
        pass
    def research_analysis(self,accurate=True):
        print('\nsalary/material/expense -> research\n')
        cr_list=self.salary+self.material+self.expense
        dr_list=self.research
        if len(dr_list) != 0:
            self.dr_analysis(cr_list,dr_list,accurate)
        else:
            print('No research accounts to analysis!')
        # the following is out-of-date, will be deleted soon:
        #  self.__clear_temp()
        #  for cr in (self.salary+self.material+self.expense):
            #  for dr in self.research:
                #  self.start_cr2dr(cr,dr,accurate=accurate)
        #  print('salary/material/expense -> research\n')
        #  self.__show_temp()
        pass
    pass
if __name__=='__main__':
    pass
