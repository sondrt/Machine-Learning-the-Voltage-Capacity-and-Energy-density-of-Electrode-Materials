from pymatgen.ext.matproj import MPRester
from pprint import pprint
from os import path
import numpy as np
import random
import pandas as pd
import json
import os

#####################################################################
#
# Checks if files for PoreBlazer are downloaded, if note - Downloads.
#
#####################################################################
def download_ALLstructures(allIDs):
    with MPRester("GKDHNwKre8uiowqhPh") as m:
        for id in allIDs:
            print(id)
            try:
                material_prop = m.query(criteria={"task_id": id}, properties = ['cif'])
                # print(material_prop)
                df = pd.DataFrame(material_prop)
                save_material_prop = (cif_for_poreblazer + id + ".csv")
                print(save_material_prop)
                # print(type(df),df)
    # ('energy', 'energy_per_atom', 'volume', 'formation_energy_per_atom', 'nsites', 'unit_cell_formula', 'pretty_formula', 'is_hubbard', 'elements', 'nelements', 'e_above_hull', 'hubbards', 'is_compatible', 'spacegroup', 'task_ids', 'band_gap', 'density', 'icsd_id', 'icsd_ids', 'cif', 'total_magnetization', 'material_id', 'oxide_type', 'tags', 'elasticity')
                #print( 'I will downlaod: ', id, ' in dir ', cif_info_dir)
                df.to_csv(save_material_prop)
            except:
                print("That didn't work, id: ", id)        
########################################################

do_download = True
csvfile = 'All_batteries.csv' 
cif_for_poreblazer = './cif_info_dir/'#/cif_for_poreblazer/cif_files/'

data = pd.read_csv(csvfile, sep=',')
HEADERS = list(data.head())
#print('heads = ', HEADERS)
#print data['Spacegroup']
if do_download:
    list = []
    for struct_id in data['Charged_ID']:
        print(struct_id+'_prop.dat')
        path = cif_for_poreblazer + struct_id+'_prop.dat'
        if os.path.exists(path):
            print(struct_id, ' is in ./cif_info_dir/, as', path)
            continue #skips this download        
        else:
            print(struct_id, ' is not in ./cif_info_dir/, downloading.')
            list.append(struct_id)
    download_ALLstructures(list)
    del(list)
    list = []
    for struct_id in data['Discharged_ID']:
        path = cif_for_poreblazer + struct_id+'_prop.dat'
        if os.path.exists(path):
            print(struct_id, ' is in ./cif_info_dir/, as', path)
            continue #skips this download        
        else:        
            print(struct_id, ' is not in ./cif_info_dir/, downloading.')
            list.append(struct_id)
    download_ALLstructures(list)
    del(list)
