from pymatgen.ext.matproj import MPRester
from pprint import pprint
from os import path
import numpy as np
import random
import pandas as pd
import json

def isNaN(num):
    return num != num

def download_ALLstructures(allIDs):
    with MPRester("GKDHNwKre8uiowqhPh") as m:
        for id in allIDs:
            try:
                material_prop = m.query(criteria={"task_id": id}, properties = ['cif'])
                print(material_prop)
# ('energy', 'energy_per_atom', 'volume', 'formation_energy_per_atom', 'nsites', 'unit_cell_formula', 'pretty_formula', 'is_hubbard', 'elements', 'nelements', 'e_above_hull', 'hubbards', 'is_compatible', 'spacegroup', 'task_ids', 'band_gap', 'density', 'icsd_id', 'icsd_ids', 'cif', 'total_magnetization', 'material_id', 'oxide_type', 'tags', 'elasticity')
                #print( 'I will downlaod: ', id, ' in dir ', cif_info_dir)
                with open(Cif_jsondictformat + id + '_cif.dat','w+') as f:
                    json.dump(material_prop.as_dict(), f)
            except:
                print("That didn't work, id: ", id)        
                exit()
########################################################

do_download = True
csvfile = 'manual.csv'
cif_info_dir = './cif_info_dir/'
cif_for_poreblazer = './cif_for_poreblazer/'

#heads =  ['Battid', 'Discharged_ID', 'Charged_ID', 'Reduced_Cell_Formula', 'Type', 'Spacegroup', 'Average_Voltage', 'Capacity_Grav', 'Capacity_Vol', 'Specific_E_Wh/kg', 'E Density Wh/l', 'Stability Charge', 'Stability Discharge'
###############################################################

do_download = True
csvfile = 'manual.csv'

#heads =  ['Battid', 'Discharged_ID', 'Charged_ID', 'Reduced_Cell_Formula', 'Type', 'Spacegroup', 'Average_Voltage', 'Capacity_Grav', 'Capacity_Vol', 'Specific_E_Wh/kg', 'E Density Wh/l', 'Stability Charge', 'Stability Discharge'


data = pd.read_csv(csvfile, sep=',')
HEADERS = list(data.head())
#print('heads = ', HEADERS)
#print data['Spacegroup']

if do_download:
   list = []
   for struct_id in data['Charged_ID']:
       if isNaN(struct_id) == False:
           list.append(struct_id)
   download_ALLstructures(list)
   del(list)
   list = []
   for struct_id in data['Discharged_ID']:
       if isNaN(struct_id) == False:
           list.append(struct_id)
   download_ALLstructures(list)
   del(list)
