from pprint import pprint
from os import path
import numpy as np
import random
import pandas as pd
import json

def isNaN(num):
    return num != num

def isEmpty(a):
    if not a:
        log = True
    else:
        log = False
    return log

def readElements(filename,id):
    #Reads things you want from file 
  with open(filename) as json_file:
    try:
        data = json.load(json_file)[0]
        energy = data['energy']
        energy_per_atom = data['energy_per_atom']
        volume = data['volume']
        formation_energy_per_atom = data['formation_energy_per_atom']
        nsites = data['nsites']
        unit_cell_formula= data['unit_cell_formula']
        pretty_formula = data['pretty_formula']
        elements = data['elements']    
        nelements = data['nelements']
        e_above_hull = data['e_above_hull']
        band_gap = data['band_gap']
        density = data['density']
        cif = data['cif']
        total_magnetization = data['total_magnetization']
        oxide_type = data['oxide_type']
        elasticity = data['density']
    except:
        print("no data found: ", id)
  return formation_energy_per_atom

def json_csv(filename):
    with open(filename) as data_file:
        data = json.load(data_file)
    return pd.DataFrame(data['profile_set'])

csvfile = 'manual.csv'
cif_info_dir = './cif_info_dir/'
data = pd.read_csv(csvfile, sep=',')

for id in data['Discharged_ID']:
    fn_dis = cif_info_dir + id + '_prop.dat'
    print("Empty: ",isEmpty(fn_dis))
    try:
        formation_energy_per_atom0 = readElements(fn_dis,id)
#            print(formation_energy_per_atom0)
    except:
        print('did not work for some reason',id)




# try:
#     print(readElements(fn, energy))
# except:
#     print('did not work')
	