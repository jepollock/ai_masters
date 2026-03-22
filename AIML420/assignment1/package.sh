#!/bin/bash

read -r -d '' FILELIST <<EOF
assignment1/assignment1.pdf
assignment1/part2/question2.ipynb
assignment1/part2/question2.html
assignment1/part2/question2.pdf
assignment1/part2/README.md
assignment1/part1/standalone.py
assignment1/part1/tree_struct_C_pruned.pdf
assignment1/part1/question1.ipynb
assignment1/part1/standalone.ipynb
assignment1/part1/question1.pdf
assignment1/part1/README.md
assignment1/part1/tree_struct_C.pdf
assignment1/part1/tree_struct_B.pdf
assignment1/part1/tree_struct_A.pdf
assignment1/data/breast-cancer.csv
assignment1/data/rtg_C_pruned.csv
assignment1/data/rtg_A.csv
assignment1/data/rtg_B.csv
assignment1/data/rtg_C.csv
EOF

tar -cvzf pollocjaso_aiml420_asst1.tgz $FILELIST
