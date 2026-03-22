# AIML420 - Introduction to AI Assignment #1

## Part2 - Exploring Classification Algorithms

The Correlation Matrix keeps the PDF conversion from working.

To generate the report, run from the command line:

```
jupyter nbconvert question2.ipynb \
--ExecutePreprocessor.kernel_name=python3 \
--TagRemovePreprocessor.remove_input_tags='{"remove_cell"}' \
--Exporter.preprocessors='["nbconvert.preprocessors.ExecutePreprocessor","nbconvert.preprocessors.TagRemovePreprocessor"]' \
--to html
```

This doesn't currently work, the correlation table ends up being broken.

```
jupyter nbconvert question2.ipynb \
--ExecutePreprocessor.kernel_name=python3 \
--TagRemovePreprocessor.remove_input_tags='{"remove_cell"}' \
--Exporter.preprocessors='["nbconvert.preprocessors.ExecutePreprocessor","nbconvert.preprocessors.TagRemovePreprocessor"]' \
--to pdf
```

