#!/bin/bash

out_file=bbc_converted.csv
printf "category,text\n" > $out_file
for i in `find . -name *.txt -print` ; do
    echo "Converting $i"
    ./convert.sh $i >>$out_file
done
