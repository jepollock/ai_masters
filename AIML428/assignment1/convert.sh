#!/bin/bash

in_file=$1

target="$(basename "$(dirname "$in_file")")"

printf "${target},"
cat $in_file | tr '[:upper:]' '[:lower:]' | tr '[:punct:]' ' ' | tr '\n\r\t\v\f' " " | tr -s "[:space:]" | sed 's/^  *//'
printf "\n"
