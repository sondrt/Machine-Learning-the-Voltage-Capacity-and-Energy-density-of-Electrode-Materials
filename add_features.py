from pprint import pprint
from os import path
import numpy as np
import random
import pandas as pd
import json
import fnmatch

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
  return(str(energy),str(energy_per_atom),str(volume),str(formation_energy_per_atom),str(nsites),str(band_gap),str(density),str(total_magnetization),str(elasticity))

def json_csv(filename):
    with open(filename) as data_file:
        data = json.load(data_file)
    return pd.DataFrame(data['profile_set'])


csvfile = 'manual.csv'
outcsv = 'material_properties.csv'
cif_info_dir = './cif_info_dir/'
data = pd.read_csv(csvfile, sep=',')

output = open(outcsv,'w+')
output.write('mid,energy,energy_per_atom,volume,formation_energy_per_atom,nsites,band_gap,density,total_magnetization,elasticity\n')

aa=[]
try:
    for ID in ['Discharged_ID','Charged_ID']:
        for struct_id in data[ID]:
            fn = cif_info_dir + struct_id + '_prop.dat'
            fpatt = fn.replace(".csv","")
            fpatt = fn.replace("./cif_info_dir/","")
            energy0,energy_per_atom0,volume0,formation_energy_per_atom0,nsites0,band_gap0,density0,total_magnetization0,elasticity0  = readElements(fn,ID)
            output.write(fpatt.replace("_prop.dat","") + ","+ energy0 + "," + energy_per_atom0+ ","+volume0+ ","+formation_energy_per_atom0+ ","+nsites0+ ","+band_gap0+ ","+density0+ ","+total_magnetization0+ ","+elasticity0+ '\n')

except:
    print('That did not work')








	 