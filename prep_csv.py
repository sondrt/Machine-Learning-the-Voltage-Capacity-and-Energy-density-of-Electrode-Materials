#!/usr/bin/env python

#from pymatgen.ext.matproj import MPRester
from pprint import pprint
from os import path
import numpy as np
import random
import pandas as pd
import json
import sys
import pickle
import re 


def main():
    csv = 'allFiles.csv' # Change for discharged or charged ids.
    outcsv = 'for_ML.csv'
    
    l_charged_atoms = True
    l_discharged_atoms= True
    Target = 'Average_Voltage'
    list_of_predictors = ['Battid',
    # 'Reduced_Cell_Formula',
    # 'Spacegroup',

    # 'Average_Voltage',s
    
    'Capacity_Grav',
    'Capacity_Vol',
    
    'Specific_E_Wh/kg',
    
    'E Density Wh/l',
    
    # 'Stability Discharge',                                    # No predictions to talk about.
    # 'Stability Charge',                                       # On stability

    # 'helvol',                                                 # this is not ideal
    # 'geomvol',
    # 'helvol_dis',
    # 'geomvol_dis',

    'energy',
    'energy_dis',                                               #  1

    # 'energy_per_atom',
    # 'energy_per_atom_dis',    

    'volume',
    'volume_dis',                                               #  1
    
    'formation_energy_per_atom',
    'formation_energy_per_atom_dis',                            #  1
    
    # 'band_gap',
    # 'band_gap_dis',
    
    'density',
    'density_dis',                                              #  1
    
    'total_magnetization',
    'total_magnetization_dis',                                  #  1

    # 'nsites',
    # 'nsites_dis',

    # 'elasticity',
    # 'elasticity_dis'    
    ]



    if l_charged_atoms:
    	for ii in [
    	'F_vol','Ni_vol','O_vol','Cr_vol','Mn_vol','As_vol','Mo_vol',
    'Cu_vol','Bi_vol','S_vol','P_vol','V_vol','Fe_vol','Sn_vol','Si_vol',
    'W_vol','Ti_vol','Co_vol','Sb_vol','Ge_vol','Mg_vol'
    #
    # 'La_vol'
    ]:
     	   list_of_predictors.append(ii)
    
    if l_discharged_atoms:
    	for ii in [
    		'Ge_vol_dis', 'W_vol_dis', 'V_vol_dis', 'Sn_vol_dis', 'Ba_vol_dis', 'P_vol_dis', 
    'O_vol_dis', 'Fe_vol_dis', 'Ni_vol_dis', 'Ti_vol_dis', 'Mg_vol_dis', 
    'Co_vol_dis', 'F_vol_dis', 'Cr_vol_dis', 'Cu_vol_dis', 
    'Mo_vol_dis', 'Si_vol_dis', 'Mn_vol_dis', 'Bi_vol_dis', 'As_vol_dis', 'Te_vol_dis', 
    'S_vol_dis', 'Sb_vol_dis'
    #elements with 1 - 3 materials
    # 'Ta_vol_dis', 
    # 'Se_vol_dis',
    # 'Pr_vol_dis',
    # 'La_vol_dis',
    # 'Sr_vol_dis',
    # 'Nb_vol_dis',
    # 'N_vol_dis'
    ]:
    		list_of_predictors.append(ii)
    
    
    list_of_predictors.append(Target)
    
    
    data = pd.read_csv(csv, sep=',')
    headers = list(data.head())

    newframe = pd.DataFrame()
    for fld in list_of_predictors:
       newframe[fld] = data[fld]

    
    newframe.to_csv(outcsv,sep=',',index=False)

    print(Target, list_of_predictors)



if __name__ == '__main__':
    main()







