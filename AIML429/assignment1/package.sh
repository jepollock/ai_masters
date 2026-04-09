#!/bin/bash

read -r -d '' FILELIST <<EOF
assignment1/assignment1.pdf
assignment1/belief_prop.py
assignment1/burglar.py
assignment1/gibbs.py
EOF

tar -cvzf pollocjaso_aiml429_asst1.tgz $FILELIST
