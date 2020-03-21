#AP-RDF.py


# This program gets cif files from csv before making .pdb files
# then creating aprdf.csv files for all cif files. 

#######################################################################
import pandas as pd
import json

def readcif(filename):
    #Reads things you want form file 
    with open(filename) as json_file:
        data = json.load(json_file)[0]
        cif = data['cif']
        # print('this is cif: ',cif)
    return cif



def getCIFfromcsvfile():
    #Load data
    csvfile = '../Li_allFiles.csv'
    cif_info_dir = '../cif_info_dir/'
    outdir = '../cif_info_dir/cif_for_aprdf/'
    data = pd.read_csv(csvfile, sep=',')

    for id in ['Charged_ID','Discharged_ID']:
        for struc_id in data[id]:
            # print(struc_id)
            output_filename = outdir + struc_id + '.cif'
            fn = cif_info_dir + struc_id + '_prop.dat'
            # # print('fn: ', fn)
            try:
                cif = readcif(fn)
            except:
                print('Something wrong with: ', fn)
                pass
            output = open(output_filename,'w+')
            output.write(cif)
    print('Done, CIF can now be found in ./cif_info_dir/cif_for_aprdf/')
    return
# getCIFfromcsvfile()


######################################################################
# Takes all the CIF files, runs Obabel 
# and makes pdb files of all files in './cif_info_dir/cif_for_aprdf/'

import os
import fnmatch

def cif_to_pdb():
    dirin = '../cif_info_dir/cif_for_aprdf/'
    dir_pdb_for_aprdf = '../cif_info_dir/pdb_for_aprdf/'
    files = os.listdir(dirin)
    # print(files)
    for file in files:
        cmd = 'obabel ' + dirin + file + ' --fillUC ' + '-O' + dir_pdb_for_aprdf + file.replace(".cif","") + '.pdb'
        print('Running: ' + cmd)
        os.system( cmd )
    return

# cif_to_pdb()

#####################################################################
# Run code:                                                                         #TO DO
# Koden er avhengig av filsystemet på en teit måte. Gjør noe med dette.
# utility missing: gfortran -C -cpp -o ap-rdf.x neighlist_mod.f90 ap-rdf.f90

#Maa kjøres fra mappen med ./ap-rdf.x og ha alle pdb filene i samme mappe. 

def pdb_to_aprdf():
    dirin = '../cif_info_dir/pdb_for_aprdf/'
    dir_aprdf = '../cif_info_dir/aprdf_for_rf/'
    files = os.listdir(dirin)
    print("Calculating AP-RDF values.")
    for file in files:
        #print('This is file: ', file)
        filein = file. replace(".pdb","")+ '.aprdf'
        if fnmatch.fnmatch(file, "m*.pdb"):
            #Fix the parameters!
            cmd = "./ap-rdf.x -i " + file +" -bfac 10.0 -rmin 2.0 -rmax 15.0 -ngrid 53 -of " + filein
            #print("running: " + cmd)
            os.system(cmd)
    return

# getCIFfromcsvfile()
# cif_to_pdb()
# pdb_to_aprdf()







