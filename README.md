# Audit Toolkit
## 1. Description
### 1.1 What is AUTK
Audit Toolkit for those who are working hard near the end of the year.
### 1.2 Key Traits
1. To perform audit procedures quickly.
2. To enjoy your auditing work.
3. To make benefit for the auditors.
## 2. Deployment
### 2.1 Requirements
```json
{
    "python_version":"python 3.8 at least",
    "libs_require":[
        "xlrd",
        "xlwt",
        "openpyxl",
        "numpy",
        "pandas"
    ],
    "libs_optional":[
        "scipy",
        "sk-learn"
    ]
}
```
#### 2.1.1 Quick Install Requirements
To quickly install all these dependent libs, run:<br>
```
pip3 install -r ./libs_require.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```
#### 2.1.2 Recommended
1. About virtual environment builder, `virtualenv` is recommended, run `sudo pacman -S python-virtualenv` to install.<br>
2. About IDE, `SpaceVim` is highly recommended, which is also the very tool to develop this repository, see: [https://spacevim.org/](https://spacevim.org/) or [https://spacevim.org/cn/](https://spacevim.org/cn/).<br>
3. For more information about `tuna pypi source`, see:[https://mirrors.tuna.tsinghua.edu.cn/help/pypi/](https://mirrors.tuna.tsinghua.edu.cn/help/pypi/).<br>

### 2.2 Clone this repository
Clone this repository into your local file disk and place it under the python `$PATH`:<br>
```
git clone 'https://github.com/zefuirusu/autk.git' ~/Downloads/
```
## 3. To Contribute
Feel free to fork.<br>
Any questions or suggestions, start an issue.<br>
## 4. Declaration
1. This repository is still growing and being tested..
2. Financial Auditors and relevant developers are the target users of this repository.
3. This repository is built by,with and for the auditors.
