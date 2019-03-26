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
            material_prop = m.query(criteria={"task_id": id}, properties = ["nsites","unit_cell_formula", 
 "pretty_formula", "elements", "nelements","material_id"])

            print( 'I will downlaod: ', id, ' in dir ', cif_info_dir)

            with open(cif_info_dir + id + '_prop.dat','w+') as f:
                json.dump(material_prop, f)
########################################################
do_download = True
csvfile = 'manual.csv'
cif_info_dir = './cif_info_dir/'

#heads =  ['Battid', 'Discharged_ID', 'Charged_ID', 'Reduced_Cell_Formula', 'Type', 'Spacegroup', 'Average_Voltage', 'Capacity_Grav', 'Capacity_Vol', 'Specific_E_Wh/kg', 'E Density Wh/l', 'Stability Charge', 'Stability Discharge'


data = pd.read_csv(csvfile, sep=',')
HEADERS = list(data.head())
print('heads = ', HEADERS)
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
