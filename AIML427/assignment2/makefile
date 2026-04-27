# MI.csv - field description
# MI.data - CSV
# Note - missing data is ?

.PHONY: clean data all release

clean:
	-rm MI_header.csv
	-rm MI_with_header.csv
	-rm MI_missing_removed.csv

data: MI_with_header.csv

MI_missing_removed.csv: MI.data
	sed s'/\?//g' $< >$@

MI_header.csv: MI_field_descriptions.csv
	tail +2 $< | cut -d"," -f 1  | paste -sd ',' - > $@

MI_with_header.csv: MI_header.csv MI_missing_removed.csv
	cat $^ > $@

# MI_booleans_fixed.csv:
# 	awk 'BEGIN{FS=OFS=","} \
# 		$3==0 {$3="FALSE"} $3==1 {$3="TRUE"} \
# 		$8==0 {$8="FALSE"} $8==1 {$8="TRUE"} \
# 		1' MI_with_header.csv

