#!/bin/bash

read -r -d '' FILELIST <<EOF
assignment1/bbc_converted.csv
assignment1/convert_all.sh
assignment1/convert.sh
assignment1/README.md
assignment1/Report.pdf
assignment1/step1-3.html
assignment1/step1-3.ipynb
assignment1/step4_cnn.html
assignment1/step4_cnn.ipynb
assignment1/step5_pretrained_embedding.html
assignment1/step5_pretrained_embedding.ipynb
assignment1/step6_bert.ipynb
EOF

tar -cvzf pollocjaso_aiml428_asst1.tgz $FILELIST
