PAPER = seminarpaper_hwp
SLIDES = presentation_hwp

all : slides

.PHONY : paper
paper : $(PAPER).pdf

.PHONY : slides 
slides : $(SLIDES).pdf

$(PAPER).pdf : paper_stage
	xelatex $(PAPER)

.PHONY : paper_stage
paper_stage : $(PAPER).blg
	xelatex $(PAPER)

$(PAPER).blg : bib.bib $(PAPER).aux
	bibtex $(PAPER)

$(PAPER).aux : $(PAPER).tex
	xelatex $(PAPER)

$(SLIDES).pdf : slides_stage
	xelatex $(SLIDES)

.PHONY : slides_stage
slides_stage : $(SLIDES).blg
	xelatex $(SLIDES)

$(SLIDES).blg : bib.bib $(SLIDES).aux
	bibtex $(SLIDES)

$(SLIDES).aux : $(SLIDES).tex
	xelatex $(SLIDES)

.PHONY : clean
clean :
	rm *.bbl *.blg *.log *.aux *.toc

