# Define the source and target files
NB_SOURCES=$(wildcard *.ipynb)
PDF_TARGETS=$(NB_SOURCES:.ipynb=.pdf)

.PHONY: all clean release

all: $(PDF_TARGETS)

release: all
	tar -czf pollockjaso_aiml420_asst2.tgz -s ",^,pollockjaso_asst2/," $(NB_SOURCES) $(PDF_TARGETS)

clean:
	rm -f $(PDF_TARGETS)


%.pdf: %.ipynb
	jupyter nbconvert $< \
	--TagRemovePreprocessor.remove_cell_tags='{"remove_cell"}' \
	--TagRemovePreprocessor.remove_all_outputs_tags='{"remove_output"}' \
	--TagRemovePreprocessor.remove_input_tags='{"remove_input"}' \
	--ExecutePreprocessor.kernel_name=python3 \
	--Exporter.preprocessors='["nbconvert.preprocessors.TagRemovePreprocessor"]' \
	--to pdf


# 	--Exporter.preprocessors='["nbconvert.preprocessors.ExecutePreprocessor","nbconvert.preprocessors.TagRemovePreprocessor"]' \
