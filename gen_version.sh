#!/bin/bash

function generate() {
    date_part=`date -d "$(stat -c %y $1)" "+%Y-%m-%d %H:%M:%S"`
    file_part=`find $1/ -maxdepth 1 -type f -printf "\"%f\", "`
    echo "[$1]"
    echo "version = \"$date_part\""
    echo "filelist = [ ${file_part%, } ]"    # 去除末尾逗号空格
    echo ""
}

for dir in */; do
    generate ${dir%/}   # 去除末尾/
done
