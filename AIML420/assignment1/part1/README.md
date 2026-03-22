# AIML420 - Introduction to AI Assignment #1

## Part1 - Implement the decision tree algorithm

To generate the report

```
jupyter nbconvert question1.ipynb \
--TagRemovePreprocessor.remove_input_tags='{"remove_cell"}' \
--Exporter.preprocessors='["nbconvert.preprocessors.ExecutePreprocessor","nbconvert.preprocessors.TagRemovePreprocessor"]' \
--to pdf
```

## Part1 - Run the decision tree algorithm standalone

```
jupyter nbconvert --to script standalone.ipynb
python standalone.py --infile ../data/rtg_A.csv --outfile ../wombat

```



