#!/bin/bash
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
