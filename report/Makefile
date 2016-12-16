REPORT	=	report
LATEX		= pdflatex
BIBTEX	= bibtex -min-crossrefs=100
REF1		=	ref
REF2		=	rfc

TEX 	= $(wildcard *.tex)
SRCS 	= $(TEX)
FMT 	= cmds.tex hdr.tex fmt.tex
REFS 	= $(REF1).bib
OPTS 	= -interation=batchmode 
UNAME	=	$(shell uname -s)

ifeq ($(UNAME), Linux)
	VIEWER	=	evince
endif 
ifeq ($(UNAME), Darwin)
	VIEWER	=	open
endif
ifeq ($(OS),Windows_NT)
	VIEWER	=	$(shell echo "Yolo does not support stupid Windows ^.^  >> file: ")
endif

all: pdf

############################################################

spell:
	make clean
	for i in $(filter-out $(FMT), $(SRCS)); do ispell $$i; done

loud: $(SRCS) $(REFS)
	$(LATEX) $(REPORT) $(OPTS)
	$(BIBTEX) $(REPORT)
	perl -pi -e "s/%\s+//" $(REPORT).bbl
	$(LATEX) $(REPORT) $(OPTS)
	$(LATEX) $(REPORT) $(OPTS)

pdf: $(SRCS) $(REFS)
	$(LATEX) $(REPORT) $(OPTS) 1>/dev/null
	$(BIBTEX) $(REPORT)
	perl -pi -e "s/%\s+//" $(REPORT).bbl
	$(LATEX) $(REPORT) $(OPTS) 1>/dev/null
	$(LATEX) $(REPORT) $(OPTS) 1>/dev/null

tidy:
	rm -f *~ *.dvi *.aux *.log *.blg *.bbl $(REPORT).ps *.out *.bcf

clean:
	rm -f *~ *.dvi *.aux *.log *.blg *.bbl $(REPORT).ps *.out *.bcf $(REPORT).pdf

view: all
	$(VIEWER) $(REPORT).pdf


#$(REPORT).ps: $(REPORT).dvi
#       dvips -t letter -G0 -P cmz $(REPORT).dvi -o $(REPORT).ps
#view: $(REPORT).dvi
#       xdvi $(REPORT).dvi
#print: $(REPORT).dvi
#       dvips $(REPORT).dvi
#pdf: $(REPORT).ps
#       ps2pdf14 -dPDFSETTINGS=/prepress -dSubsetFonts=true -dEmbedAllFonts=true $<
#       ps2pdf $< $(REPORT).pdf
#printer: $(REPORT).ps
#       lpr $(REPORT).ps
