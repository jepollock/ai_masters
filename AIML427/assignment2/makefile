# MI.csv - field description
# MI.data - CSV
# Note - missing data is ?

.PHONY: clean data all release part3 part2

all: data part2 part3

clean:
	-rm MI_header.csv
	-rm MI_with_header.csv
	-rm MI_missing_removed.csv
	-rm *.pdf
	-rm *.txt

data: MI_with_header.csv

part3: part3.txt

part2: clustering.pdf

MI_missing_removed.csv: MI.data
	sed s'/\?//g' $< >$@

MI_header.csv: MI_field_descriptions.csv
	tail +2 $< | cut -d"," -f 1  | paste -sd ',' - > $@

MI_with_header.csv: MI_header.csv MI_missing_removed.csv
	cat $^ > $@

part3.txt: part3.R
	Rscript part3.R

%.pdf: %.ipynb
	jupyter nbconvert --execute $< \
	--TagRemovePreprocessor.remove_cell_tags='{"remove_cell"}' \
	--TagRemovePreprocessor.remove_all_outputs_tags='{"remove_output"}' \
	--TagRemovePreprocessor.remove_input_tags='{"remove_input"}' \
	--ExecutePreprocessor.kernel_name=python3 \
	--Exporter.preprocessors='["nbconvert.preprocessors.TagRemovePreprocessor"]' \
	--to pdf


# MI_booleans_fixed.csv:
# 	awk 'BEGIN{FS=OFS=","} \
# 		$3==0 {$3="FALSE"} $3==1 {$3="TRUE"} \
# 		$8==0 {$8="FALSE"} $8==1 {$8="TRUE"} \
# 		1' MI_with_header.csv

