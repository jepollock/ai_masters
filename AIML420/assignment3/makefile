# Define the source and target files
NB_SOURCES=$(wildcard *.ipynb)
PY_SOURCES=$(wildcard *.py)
PDF_TARGETS=$(NB_SOURCES:.ipynb=.pdf)
RELEASE_NAME=pollocjaso_aiml420_asst3

.PHONY: all clean release

all: $(PDF_TARGETS)

release: all
	tar -czf $(RELEASE_NAME).tgz -s ",^,$(RELEASE_NAME)/," $(NB_SOURCES) $(PDF_TARGETS) $(PY_SOURCES) makefile data perceptron README.md

clean:
	rm -f $(PDF_TARGETS) $(RELEASE_NAME).tgz


%.pdf: %.ipynb
	jupyter nbconvert $< \
	--TagRemovePreprocessor.remove_cell_tags='{"remove_cell"}' \
	--TagRemovePreprocessor.remove_all_outputs_tags='{"remove_output"}' \
	--TagRemovePreprocessor.remove_input_tags='{"remove_input"}' \
	--ExecutePreprocessor.kernel_name=python3 \
	--Exporter.preprocessors='["nbconvert.preprocessors.TagRemovePreprocessor"]' \
	--to pdf

part1: all

part2_taska:
	./perceptron

part2_taskb:
	./perceptron_b.py

part2_taskc:
	./multi_layer_perceptron.py --max_epoch=300

part2_taskd:
	./multi_layer_perceptron.py
