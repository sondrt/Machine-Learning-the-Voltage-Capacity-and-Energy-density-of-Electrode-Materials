from pymatgen.ext.matproj import MPRester
from pprint import pprint
from os import path
import numpy as np
import random
import pandas as pd
import json
import os.path



def isEmpty(a):
    if not a:
        log = True
    else:
        log = False
    return log

def download_ALLstructures(id):
    with MPRester("GKDHNwKre8uiowqhPh") as m:
        try:
            material_prop = m.query(criteria={"task_id": id}, properties = [ 'energy', 
'energy_per_atom', 'volume', 'formation_energy_per_atom', 'nsites', 'unit_cell_formula', 
'pretty_formula', 'is_hubbard', 'elements', 'nelements', 'e_above_hull', 'hubbards', 'is_compatible',
'spacegroup', 'task_ids', 'band_gap', 'density', 'icsd_id', 'icsd_ids', 'cif', 'total_magnetization', 
'material_id', 'oxide_type', 'tags', 'elasticity'])
            
            print("Empty: ",isEmpty(material_prop))

            print( 'I will download: ', id, ' in dir ', cif_info_dir)
            with open(cif_info_dir + id + '_prop.dat','w+') as f:
                json.dump(material_prop, f)
        except:
          print("That didn't work, id: ", id)            
########################################################
do_download = True
csvfile = 'Li_batteries.csv' # Typical values: 'manualOKT.csv', 'mg_batteries.csv', 'Li_batteries.csv'
cif_info_dir = './cif_info_dir/'
#heads =  ['Battid', 'Discharged_ID', 'Charged_ID', 'Reduced_Cell_Formula', 'Type', 'Spacegroup', 'Average_Voltage', 'Capacity_Grav', 'Capacity_Vol', 'Specific_E_Wh/kg', 'E Density Wh/l', 'Stability Charge', 'Stability Discharge'


data = pd.read_csv(csvfile, sep=',')
HEADERS = list(data.head())
print('heads = ', HEADERS)  #This cant be commented out. 
#print data['Spacegroup']

if do_download:
    for ID in ['Charged_ID','Discharged_ID']:
        for struct_id in data[ID]:
            print(struct_id)
            filename = cif_info_dir + struct_id + '_prop.dat'
            exist = os.path.isfile(filename)
            Empty = False
            if exist:
                isEmpty(filename)
                with open(filename,'r') as f:
                    data2 = json.load(f)

                    try: 
                        print(data['energy'])
                        if data2['energy'] == 0:
                            Empty = True
                    except:
                        pass
            if not exist or Empty:
                print("download is ", exist, Empty)
                download_ALLstructures(struct_id)        
    print("Done!")
    print("Number of charged_IDs: ", len(data["Charged_ID"]))







