# Define the source and target files
DOT_SOURCES := $(wildcard *.dot)
PDF_TARGETS := $(DOT_SOURCES:.dot=.pdf)
TEX_SRCS := assignment1.tex
TEX_TARGETS := $(TEX_SRCS:.tex=.pdf)

.PHONY: all clean

# Default target
all:  $(TEX_TARGETS) $(PDF_TARGETS)


# MAIN LATEXMK RULE
# -pdf tells latexmk to generate PDF directly (instead of DVI).
# -pdflatex="" tells latexmk to call a specific backend with specific options.
# -use-make tells latexmk to call make for generating missing files.
# -interaction=nonstopmode keeps the pdflatex backend from stopping at a
# missing file reference and interactively asking you for an alternative.
%.pdf: %.tex
	latexmk -pdf -pdflatex="pdflatex -interaction=nonstopmode" -use-make $<

# Pattern rule to convert .dot to .pdf
%.pdf: %.dot
	dot -Tpdf $< -o $@

# "raw2tex" and "dat2tex" are just placeholders for whatever custom steps
# you might have.
%.tex: %.raw
	./raw2tex $< > $@

%.tex: %.dat
	./dat2tex $< > $@

# Clean up generated files
clean:
	rm -f $(PDF_TARGETS)
	latexmk -CA



