# AIML420 - Introduction to AI Assignment #1

## Part1 - Implement the decision tree algorithm

```
(base) part1 % python standalone.py --help
usage: standalone.py [-h] [-i INFILE] [-o OUTFILE]

options:
  -h, --help            show this help message and exit
  -i, --infile INFILE
  -o, --outfile OUTFILE
```

The code reads INFILE, and writes the tree structure to OUTFILE.pdf. It will print accuracy information to stdout.

To process a CSV using part1's decision tree code:

```
python standalone.py --infile ../data/rtg_A.csv --outfile ../tree_structure
```

The source code for the tree is available in question1.ipynb. The tree structures will be in tree\_struct\_<A|B|C>.pdf

### Report Generation

To generate the question1's PDF report:

```
jupyter nbconvert question1.ipynb \
--TagRemovePreprocessor.remove_input_tags='{"remove_cell"}' \
--Exporter.preprocessors='["nbconvert.preprocessors.ExecutePreprocessor","nbconvert.preprocessors.TagRemovePreprocessor"]' \
--to pdf
```

To generate the standalone script:

```
jupyter nbconvert --to script standalone.ipynb
```
