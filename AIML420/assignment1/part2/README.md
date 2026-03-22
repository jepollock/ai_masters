# AIML420 - Introduction to AI Assignment #1

## Part2 - Exploring Classification Algorithms

Tested on `barretts`. Code is in question2.ipynb.

To generate the report, run from the command line:

```
jupyter nbconvert question2.ipynb \
--ExecutePreprocessor.kernel_name=python3 \
--TagRemovePreprocessor.remove_input_tags='{"remove_cell"}' \
--Exporter.preprocessors='["nbconvert.preprocessors.ExecutePreprocessor","nbconvert.preprocessors.TagRemovePreprocessor"]' \
--to html
```

Expected output is all in the HTML, and it should reproduce the Question 2 section of the submitted PDF.

There is an expected, ignorable error during generation:

```
[NbConvertApp] ERROR | Notebook JSON is invalid: Additional properties are not allowed ('jetTransient' was unexpected)

Failed validating 'additionalProperties' in display_data
```

## Bugs

* PDF generation doesn't currently work, the correlation table ends up being broken.
* One code block is included in the resulting report, even with remove_cell tag applied.

```
jupyter nbconvert question2.ipynb \
--ExecutePreprocessor.kernel_name=python3 \
--TagRemovePreprocessor.remove_input_tags='{"remove_cell"}' \
--Exporter.preprocessors='["nbconvert.preprocessors.ExecutePreprocessor","nbconvert.preprocessors.TagRemovePreprocessor"]' \
--to pdf
```

