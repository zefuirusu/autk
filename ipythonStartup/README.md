# ipython configure files
## Deploy This Tool
```bash
function multilink(){
    fromdir=$1;
    todir=$2;
    echo 'from here:'$fromdir;
    echo 'link to there:'$todir;
    for i in $(ls $fromdir);
    do 
        ln -s $fromdir/$i $todir/$i;
    done
}
```
With the function above in `~/.bashrc`, you will be able to create soft link to `~/.ipython/profile_default/startup`.
''
## Join Sheets of `Microsoft Excel` files.

