all: document.pdf 

TEXFILES= $(shell find . -name '*.tex')
FIGS= 

document.pdf: $(TEXFILES) $(FIGS)
	cd figures && ./makeGraph && cd ..
	texi2pdf document.tex
