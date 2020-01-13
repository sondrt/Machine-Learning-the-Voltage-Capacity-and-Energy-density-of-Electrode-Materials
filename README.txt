
Steps for use of python scripts:
#There are two possible rutes for this script. To include the void fractions for all materials you use all steps, to ignore density fraction skip step 4-6.

		mp_battery_scraper.py
	0: Scrape batteries with a given working ion from the Materials Project battery explorer(https://www.materialsproject.org/#search/batteries)


		fillproperties.py
	1: Download all materials that match a material_id correlated to a battid.
		Output files: directory cif_info_dir/<material_id>_prop.dat

		add_features.py
	2: Gets and adds the material specific features from the JSON dump to a csv.
		Output files: material_properties.csv

		elements.py
	3: Calculate the density fractions for all materials. 
		Output files: out_csv_dis.csv

		forPoreblazer.py
	4: Download the CIF files as JSON for all materials correlated to a battid. 
		Output files: directory cif_for_poreblazer/<material_id>_cif.dat

		process_cif.py
	5: Extract the CIF information from the previous JSON data.
		Output files: directory cif_for_poreblazer/cif_files/<material_id>_cif.dat.csv

		process_cif_poreblazer.py
	6: Extract void fraction with poreblazer using the CIF files.
		Output files: helvol_geomvol_output.csv 
	
		merger.py
	7: Merge charged and discharged for all properties
		Output files: allFiles.csv

		prep_csv.py
	8: Select predictors and targets for ML
		Output files: for_ML.csv

		randomforest.py
	9:  Run randomforrest
		Output files: Depending on what being saved: ./Results/*
	
		rf_crossvalidation.py
	10: Run cross-validation, remove outliers.


	
python prep_csv.py >> Results/2020-01-05/2020-01-05.txt; python randomforest.py >>  Results/2020-01-05/2020-01-05.txt; python rf_crossvalidation.py >> Results/2020-01-05/2020-01-05.txt

cmd: 

#Open all relevant files.
open 


#Run point 0 through 10.
python3 mp_battery_scrape.py; python3 fillproperties.py; python3 elements.py; python3 add_features.py; python3 forPoreblazer.py; python3 process_cif.py; python3 merger.py; python3 prep_csv.py; python3 randomforest.py; python3 rf_CROSSVAL.py

#No poreblazer
python3 mp_battery_scrape.py; python3 fillproperties.py; python3 elements.py; python3 add_features.py; python3 merger.py; python3 prep_csv.py; python3 randomforest.py; python3 rf_CROSSVAL.py


#Dont need forPoreblazer?



Things that does not work as it is supposed to.


add_features.py

A program to get the pure cif files in to the ./cif_for_poreblazer/cif_files/ 

To be checked:
- assuming that rf ignores NaN values. 


#GOTTA ADD AP-RDF and run_aprdf