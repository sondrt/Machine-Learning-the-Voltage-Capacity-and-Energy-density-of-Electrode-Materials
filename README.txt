
Steps for use of python scripts:


	0: Scrape batteries with a given working ion from the Materials Project battery explorer(https://www.materialsproject.org/#search/batteries)


	1:	Download all materials that match a material_id correlated to a battid.
			Output files: directory cif_info_dir/<material_id>_prop.dat 

	2:	Calculate the density fractions for all materials. 
			Output files: out_csv_dis.csv

	3:	Download the CIF files as JSON for all materials correlated to a battid. 
			Output files: directory cif_for_poreblazer/<material_id>_cif.dat

	4:	Extract the CIF information from the previous JSON data.
			Output files: directory cif_for_poreblazer/cif_files/<material_id>_cif.dat.csv

	5:	Extract void fraction with poreblazer using the CIF files.
			Output files: helvol_geomvol.csv 
	
	6:	Merge charged and discharged helvol and geomvol
			Output files: allFiles.csv

	7:	Select predictors and targets for ML
			Output files: for_ML.csv

	8: 	Run randomforrest
			Output files: Depending on what being saved: ./Results/*

	9: 	???


	10:	Profit!


cmd: 
 python fillproperties.py; python elements.py; python forPoreblazer.py; python process_cif.py; python merger.py; python prep_csv.py; python randomforest.py; python rf_CROSSVAL.py