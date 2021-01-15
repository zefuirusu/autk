# autk
Auditing Toolkit for auditors who are working hard but suffering a lot near the end of the year.
## 1.Microsoft Office Customized User Interface
Import config files at `./MS-Office-UI` into Microsoft Excel/Word, and you'll get a pretty UI which benefits your work.
## 2.GL Processing
### 2.1 Deploy
```bash
#!/usr/bin/bash
git clone https://github.com/zefuirusu/autk.git ./autk
cp -r ./autk ~/.local/lib/python/site-packages/
```
### 2.2 Automatic Sampling
Read account data from Trial Balance and calculate target sum amount, then get a sample of specific account, from the General Ledger.
Three files needed:
- Trial Balance exported from E-Audit.
- General Ledger exported from E-Audit.
- A text file containing account id list which you want to inspect.
### 2.3
## 3.File Handling Assistant
### 3.1 File Searching Tool
Find file on your local disk with `Regular Expression`.
Here's an example:
```python
#!/usr/bin/env python
from autk.fileAssistant.findfile import find
regitem=str(r'^.*\.xlsx$')
resu=find(regitem,fdir=os.path.abspath(os.curdir),match=False)
print(resu)
```
### 3.2 Automatic Print
When you need to print a large sum of `Portable Document Format(PDF)` Files with `Adobe Acrobat DC`, this will help.
## 4.Ipython Start-up Configuration
`ipython` is a marvellous shell.
By configuring python scripts at `~/.ipython/profile_default/startup` you can initialize some `General Ledger Class` to speed up your work with `Microsoft Office Excel` files.
## Namo Amitabha
```cpp
```
## Others
[copy whole sheet in Excel with openpyxl](https://blog.csdn.net/d9394952/article/details/88236217)
