
all: pdf
	make clean

clean:
	rm -f *.aux *.fdb_latexmk *.fls *.ilg *.gz *.tdo *.toc *.out

clean_all: clean
	rm -f *.log *.pdf

pdf: clean_all
	pdflatex main.tex
	pdflatex main.tex
