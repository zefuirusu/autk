#!/usr/bin/env python
# coding=utf-8
from threading import Thread
class CashFlow:
    def __init__(self,mgl,accid_list=['1002','1001']):
        self.mgl=mgl
        # if self.mgl.load_count==0:
        #     self.mgl.load_raw_data()
        self.xlmap=self.mgl.xlmap
        self.single_flow=[]
        self.multi_flow=[]
        self.accid_list=accid_list
        self.glid_list=[]
        for accid in self.accid_list:
            self.glid_list.extend(
                list(
                    self.mgl.getAcct(
                        accid,accid_label=None,
                        side='all',
                        pure=False,
                        accurate=False
                    )[self.mgl.key_name].drop_duplicates()
                )
            )
        # self.collect()
        pass
    def collect(self):
        # def __which_flow(glid):
        #     jr=self.mgl.get_jr(glid)
        #     if jr.single == True:
        #         self.single_flow.append(jr)
        #     else:
        #         self.multi_flow.append(jr)
        #     pass
        # thread_list=[]
        # for glid in self.glid_list:
        #     t=Thread(target=__which_flow,args=(glid,),name=glid)
        #     thread_list.append(t)
        #     continue
        # for t in thread_list:
        #     t.start()
        # for t in thread_list:
        #     t.join()
        # for glid in self.glid_list:
        #     jr=self.mgl.get_jr(glid)
        #     if jr.single ==True:
        #         self.single_flow.append(jr)
        #     else:
        #         self.multi_flow.append(jr)
        # pass
        # split glid list by months first;
        def __month_collection(m):
            from copy import deepcopy
            fake_mgl=deepcopy(self.mgl)
            fake_mgl.filter([[m,'month',True,True]],filter_type='str',over_write=True)
            fake_cash_flow=CashFlow(fake_mgl,accid_list=self.accid_list)
            for glid in fake_cash_flow.glid_list:
                jr=fake_cash_flow.mgl.get_jr(glid)
                if jr.single == True:
                    self.single_flow.append(jr)
                else:
                    self.multi_flow.append(jr)
                continue
            pass
        month_thread_list=[]
        for m in self.mgl.data['month'].drop_duplicates():
            t=Thread(target=__month_collection,args=(m,))
            month_thread_list.append(t)
            continue
        for t in month_thread_list:
            t.start()
        for t in month_thread_list:
            t.join()
        pass
    pass
if __name__=='__main__':
    pass