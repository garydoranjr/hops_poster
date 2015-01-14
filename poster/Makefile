DOC = hops
TEX = pdflatex
CLEAN = *.log *.aux *.out *.bbl *.blg *.nav *.snm *.toc
CLEANER = *.pdf

all:
	$(TEX) $(DOC)
	$(TEX) $(DOC)

clean:
	rm -f $(CLEAN)

cleaner: clean
	rm -f $(CLEANER)
