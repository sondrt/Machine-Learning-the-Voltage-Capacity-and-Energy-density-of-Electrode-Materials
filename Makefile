# Convenient makefile for Creten_Stuff

all:
	python fillproperties.py
	python elements.py
	python forPoreblazer.py
	python process_cif.py
	python merger.py
	python prep_csv.py
	python randomforest.py
	python rf_CROSSVAL.py
