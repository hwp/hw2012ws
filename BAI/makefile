NAME = seminarpaper_hwp

$(NAME).pdf : stage
	xelatex $(NAME)

.PHONY : stage
stage : $(NAME).blg
	xelatex $(NAME)

$(NAME).blg : bib.bib $(NAME).aux
	bibtex $(NAME)

$(NAME).aux : $(NAME).tex
	xelatex $(NAME)

.PHONY : clean
clean :
	rm *.bbl *.blg *.log *.aux *.toc

