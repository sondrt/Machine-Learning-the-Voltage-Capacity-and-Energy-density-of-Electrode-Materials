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

   
def drop_zeros(df):
    #This thing dropes zeros, but it is not great, manually change what u want to use. 
    list_of_indexes =[]
    for index, row in df.iterrows():
        important_rows=abs(row['elneg_charged'] + row['elneg_discharged'] + row['vdw_charged'] + row['vdw_discharged'] + row['polar_charged'] + row['polar_discharged'])
        if (important_rows) == 0:
            # df = df.drop(index)
            list_of_indexes.append(index)
    df = df.drop(df.index[list_of_indexes])
#    df = df.drop(list_of_indexes)

    # for index in list_of_indexes:
    #     df = df.drop(index)
    return df

T = True
F = False
def main():
    csv = "battery_data_after_aprdf_merge.csv"                                        #'battery_data_after_aprdf_merge.csv' , "allFiles.csv"
    outcsv = 'for_ML.csv'
    

    Target              = 'Average_Voltage'
# Possinble Targets: Average_voltage, Capacity_Grav, Capacity_Vol, Specific_E_Wh/kg, 
# E Density Wh/l, Stability Discharge, Stability Charge. 

    l_charged_atoms     = False     #turns on fraction density predictor for charged material
    l_discharged_atoms  = False     #turns on fraction density predictor for discharged material

    list_of_predictors= ['Battid', 
    # 'Reduced_Cell_Formula',   # Not operational.
    # 'Spacegroup',             # Not operational.

    # 'Average_Voltage',
    
    # 'Capacity_Grav',
    # 'Capacity_Vol',
    
    # 'Specific_E_Wh/kg',
    
    # 'E Density Wh/l',
    
    # 'Stability Discharge',                                    # No predictions to talk about.
    # 'Stability Charge',                                       # On stability

    # 'helvol',                                                 # this is not ideal
    # 'geomvol',
    # 'helvol_dis',
    # 'geomvol_dis',

    # 'energy',
    # 'energy_dis',                                               #  1

    #'energy_per_atom',
    #'energy_per_atom_dis',    

    # 'volume',
    # 'volume_dis',                                               #  1
    
    #'formation_energy_per_atom',
    #'formation_energy_per_atom_dis',                            #  1
    
    # 'band_gap',
    # 'band_gap_dis',
    
    # 'density',
    # 'density_dis',                                              #  1
    
    # 'total_magnetization',
    # 'total_magnetization_dis',                                  #  1

    # 'nsites',
    # 'nsites_dis',

    # 'elasticity',
    # 'elasticity_dis'   


    'radius_charged',
    'elneg_charged',
    'elneg_discharged',
    'vdw_charged',
    'vdw_discharged',
    'polar_charged',
    'polar_discharged'
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

    # headers = list(data.head())

    df = pd.DataFrame()
    for fld in list_of_predictors:
       df[fld] = data[fld]
    df.loc[~(df==0).all(axis=1)]

    df = df.round(6)
        # df.fillna(0)

    df = drop_zeros(df)
    df.to_csv(outcsv,sep=',',index=False)

    print(Target, list_of_predictors)



if __name__ == '__main__':
    main()



'''
For df.loc[]
If abs(sum(line[1:-1])) < eps:
                7_kol_er_null_liste.append(line)

'''
