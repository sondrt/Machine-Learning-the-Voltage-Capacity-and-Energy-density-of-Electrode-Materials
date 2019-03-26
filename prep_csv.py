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


def readElements(filename):
  with open(filename) as json_file:
    data = json.load(json_file)[0]
    elements = data['elements']
    unit_cell_formula= data['unit_cell_formula']
    volume = data['volume']
  return elements, unit_cell_formula, volume

####################################################
def main():
    csv = 'out_csv_dis.csv' # Change for discharged or charged ids.
    outcsv = 'for_ML.csv'
    
    l_charged_atoms = True
    l_discharged_atoms= True
    Target = 'Average_Voltage'
    list_of_predictors = ['Battid',
    # 'Reduced_Cell_Formula',
    # 'Spacegroup',
    # 'Average_Voltage',
    'Capacity_Grav',
    'Capacity_Vol',
    'Specific_E_Wh/kg',
    'E Density Wh/l',
    'Stability Discharge',
    'Stability Charge'
    ]
    if l_charged_atoms:
    	for ii in [
    	'F_vol','Ni_vol','O_vol','Cr_vol','La_vol','Mn_vol','As_vol','Mo_vol',
    'Cu_vol','Bi_vol','S_vol','P_vol','V_vol','Fe_vol','Sn_vol','Si_vol',
    'W_vol','Ti_vol','Co_vol','Sb_vol','Ge_vol','Mg_vol']:
     	   list_of_predictors.append(ii)
    
    if l_discharged_atoms:
    	for ii in [
    		'Ge_vol_dis', 'W_vol_dis', 'Ta_vol_dis', 'V_vol_dis', 'Sn_vol_dis', 'Ba_vol_dis', 'P_vol_dis', 
    'O_vol_dis', 'La_vol_dis', 'Fe_vol_dis', 'Ni_vol_dis', 'Ti_vol_dis', 'N_vol_dis', 'Mg_vol_dis', 
    'Co_vol_dis', 'F_vol_dis', 'Cr_vol_dis', 'Pr_vol_dis', 'Nb_vol_dis', 'Se_vol_dis', 'Cu_vol_dis', 
    'Mo_vol_dis', 'Si_vol_dis', 'Mn_vol_dis', 'Bi_vol_dis', 'Sr_vol_dis', 'As_vol_dis', 'Te_vol_dis', 
    'S_vol_dis', 'Sb_vol_dis']:
    		list_of_predictors.append(ii)
    
    
    list_of_predictors.append(Target)
    
    #print(list_of_predictors)
    
    data = pd.read_csv(csv, sep=',')
    headers = list(data.head())
    #print(headers)
    
    
    newframe = pd.DataFrame()
    for fld in list_of_predictors:
       newframe[fld] = data[fld]
    #   print("fld: ", fld)
    #print(newframe)
    
    
    newframe.to_csv(outcsv,sep=',')




if __name__ == '__main__':
    main()







