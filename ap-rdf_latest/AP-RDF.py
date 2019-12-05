#AP-RDF.py


# Need all the CIF files as .CIF. 													*Done
# obabel allCIFfiles.cif --fillUC -OallCIFfiles.pdb									*Done
# obabel -icif CIF.cif --fillUC -opdb -OCIF.pdb
# Test begge.																		*trenger kanskje ikke dette?

# Run code:																			#TO DO
# ./ap-rdf.x -i CIF.pdb -bfac 1.0 -rmin 3.0 -rmax 50.0 -ngrid 50 -repcell F -of  CIF.aprdf
# Husk aa bruk -repcell T/F

# Writes all files in './cif_info_dir/' from .dat/csv to
# .cif in a new folder named './cif_info_dir/cif_for_aprdf/'

#######################################################################
import pandas as pd
import json

def readcif(filename):
    #Reads things you want form file 
    with open(filename) as json_file:
        data = json.load(json_file)[0]
        cif = data['cif']
    return cif

#Load data
csvfile = '../manualOKT.csv'
cif_info_dir = '../cif_info_dir/'
outdir = '../cif_info_dir/cif_for_aprdf/'
data = pd.read_csv(csvfile, sep=',')

def getCIFfromcsvfile():
	for id in ['Charged_ID','Discharged_ID']:
		for struc_id in data[id]:
		#	print(struc_id)
			output_filename = outdir + struc_id + '.cif'
			fn = cif_info_dir + struc_id + '_prop.dat'
			cif = readcif(fn)
			output = open(output_filename,'w+')
			output.write(cif)
	print('Done, CIF can now be found in ./cif_info_dir/cif_for_aprdf/')
	return
#getCIFfromcsvfile()


######################################################################
# Takes all the CIF files, runs Obabel 
# and makes pdb files of all files in './cif_info_dir/cif_for_aprdf/'

import os
import fnmatch

dirin = '../cif_info_dir/cif_for_aprdf/'
dir_pdb_for_aprdf = '../cif_info_dir/pdb_for_aprdf/'
files = os.listdir(dirin)
def cif_to_pdb():
	for file in files:
		if fnmatch.fnmatch(file, 'm*.cif'):
			cmd = 'obabel ' + dirin + file + ' --fillUC ' + '-O' + dir_pdb_for_aprdf + file.replace(".cif","") + '.pdb'
			print('Running: ' + cmd)
			os.system( cmd )
	return

#cif_to_pdb()

#####################################################################
# Run code:																			#TO DO
# Koden er avhengig av filsystemet på en teit måte. Gjør noe med dette.
# utility missing: gfortran -C -cpp -o ap-rdf.x neighlist_mod.f90 ap-rdf.f90

dirin = '../cif_info_dir/pdb_for_aprdf/'
dir_aprdf = '../cif_info_dir/aprdf_for_rf/'
files = os.listdir(dirin)
def pdb_to_aprdf():
	for file in files:
		print('This is file: ', file)
		filein = dir_aprdf + file.replace(".pdb","")+ '.aprdf'
		print(filein)
		if fnmatch.fnmatch(file, "m*.pdb"):
			#Fix the parameters!
			cmd = "./ap-rdf.x -i " + file +" -bfac 1.0 -rmin 3.0 -rmax 50.0 -ngrid 50 -of " + filein
			print("running: " + cmd)
			os.system(cmd)
		exit()
	return
pdb_to_aprdf()
#./ap-rdf.x -i mp-18900.pdb -bfac 1.0 -rmin 3.0 -rmax 50.0 -ngrid 50 -of mp-18900.aprdf



'''
dirin = './cif_info_dir/cif_for_aprdf/'
appin = './AP-RDF/'
files = os.listdir(dir_aprdf)
i = 0
for file in files:
	if fnmatch.fnmatch(file, 'm*.pdb'):
		print(file)
		cmd = 'cd '+ appin+ '; ' + './ap-rdf.x -i ' + file + ' -bfac 1.0 -rmin 3.0 -rmax 10.0 -ngrid 50 -repcell T -of ' + file.replace('.pdb','') + '.aprdf'
		print(cmd)
		os.system( cmd )
		exit()
	i =+ 1 
	if i == 4: 
		exit()
'''
#./ap-rdf.x -i mp-1043530.pdb -bfac 1.0 -rmin 3.0 -rmax 50.0 -ngrid 50 -of mp-1043530.aprdf








