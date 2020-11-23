#!/usr/bin/env python
'''
需要预装软件Adobe Acrobat DC 来打开和打印pdf文件.
'''
import os
import time
import pywinauto
from pywinauto.application import Application
#
indir=os.path.abspath(os.curdir)
# indir=input(r'=>where are the files that you want to print?(type in directory)')

# set up parameters.参数设置:
prtlogdir=indir+r'-prtlog.txt'
appdir=r'C:\Program Files (x86)\Adobe\Acrobat DC\Acrobat\Acrobat.exe'
# create new log file.新建日志文件,并写入初始信息:
# print('printing log file:',prtlogdir)
# print(indir)
# print pdf once.
def oneprintpdf(pdfdir):
    '''
    print a file once.
    '''
    fname=pdfdir.split(os.sep)
    fname=fname[-1]
    pdfprinter=Application(backend='uia').start(appdir+r' '+pdfdir)
    #
    # pdfprinter['Dialog'].menu_select("文件 -> 打印(P)... Ctrl+P")
    pdfprinter['Dialog'].type_keys("^p", with_spaces = False)
    #
    # pdfprinter['Dialog'].type_keys("ENTER", with_spaces = False)
    pdfprinter['Dialog']['打印2'].click()
    #
    try:
        pdfprinter[fname+r' - Adobe Acrobat Pro DC']['关闭'].click()
        # pdfprinter[fname+r' - Adobe Acrobat Pro DC'].type_keys("^q", with_spaces = False)
    except pywinauto.timings.TimeoutError:
        # time.sleep(3)
        pdfprinter=Application(backend='uia').start(appdir+r' '+pdfdir)
        pdfprinter['Dialog'].type_keys("^p", with_spaces = False)
        # pdfprinter['Dialog'].type_keys("^p", with_spaces = False)
        pdfprinter['Dialog']['打印2'].click()
    except pywinauto.findwindows.ElementNotFoundError:
        pdfprinter['Dialog'].type_keys("^q", with_spaces = False)
        # pdfprinter['Dialog']['Button9'].click()
    else:
        pass
    finally:
        # pass
        time.sleep(1.3)
    # try:
    #     # pdfprinter['Adobe Acrobat']['否(N)'].click()
    #     pdfprinter['Adobe Acrobat'].type_keys('{ESC}')
    # except:
    #     pass
    return
# writing print log file.
def wtprtlog(logline):
    '''
    writing printing log file.
    '''
    with open(prtlogdir,mode='a',encoding = 'utf-8') as f:
        f.write(logline)
        f.write('\n')
    return
# start to print pdf files in a directory.
def start():
    '''
    start printing the files in the given directory one after another.
    '''
    with open(prtlogdir,mode='a',encoding = 'utf-8') as f_fake:
        f_fake.write(r'=====')
        f_fake.write('\n')
        f_fake.write(r'printing '+indir+r':')
        f_fake.write('\n')
        f_fake.write(r'-----')
        f_fake.write('\n')
    ct=0
    for i,j,k in os.walk(indir):
        print(j)
        for na in k:
            na=os.path.abspath(os.path.join(i,na))
            print(ct,r':',na)
            # oneprintpdf(str(na),timegap=12)
            wtprtlog(na)
            try:
                oneprintpdf(str(na))
            # except _ctypes.COMError:
            # except:
            #     oneprintpdf(str(na))
            except pywinauto.timings.TimeoutError:
                oneprintpdf(str(na))
            finally:
                pass
            ct+=1
    finishword = '%s files have been submitted to the printing device.'%ct
    wtprtlog(finishword)
    wtprtlog(r'-----')
    print(r'-'*5,'\n')
    print(finishword ,'\n')
#
