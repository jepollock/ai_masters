#!/bin/bash

out_file=bbc_converted.csv
cp /dev/null $out_file
printf "category,text\n" > $out_file
for i in `find data/bbc* -name *.txt -print` ; do
    echo "Converting $i"
    ./convert.sh $i >>$out_file
done
