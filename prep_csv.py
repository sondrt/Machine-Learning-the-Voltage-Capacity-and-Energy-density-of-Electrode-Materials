#!/usr/bin/env python

#from pymatgen.ext.matproj import MPRester
from os import path
import numpy as np
import random
import pandas as pd
import json
import sys
import pickle
import re 

   
# def drop_zeros(df):
#     #This thing dropes zeros, but it is not great, manually change what u want to use. 
#     list_of_indexes =[]
#     for index, row in df.iterrows():
#         important_rows=abs(row['elneg_charged'] + row['elneg_discharged'] + row['vdw_charged'] + row['vdw_discharged'] + row['polar_charged'] + row['polar_discharged'])
#         if (important_rows) == 0:
#             # df = df.drop(index)
#             list_of_indexes.append(index)
#     df = df.drop(df.index[list_of_indexes])
# #    df = df.drop(list_of_indexes)

#     # for index in list_of_indexes:
#     #     df = df.drop(index)
#     return df


T = True
F = False

def main():
    csv = 'Li_allFiles.csv' #'newapproch_aprdf.csv'          #'battery_data_after_aprdf_merge.csv' , "allFiles.csv"
    outcsv = 'for_ML.csv'
    

    Target              = 'Capacity_Grav'
# Possinble Targets: Average_Voltage, Capacity_Grav, Capacity_Vol, Specific_E_Wh/kg, 
# E Density Wh/l, Stability Discharge, Stability Charge. 

    l_charged_atoms     = F     #turns on fraction density predictor for charged material
    l_discharged_atoms  = F    #turns on fraction density predictor for discharged material
    APRDF = False

    l_charged_atoms_Li     = True
    l_discharged_atoms_Li  = True 

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

    # 'energy_per_atom',
    # 'energy_per_atom_dis',                                          #  1 

    # 'volume',
    # 'volume_dis',                                               
    
    # 'formation_energy_per_atom',
    # 'formation_energy_per_atom_dis',                            #  This does not work
    
    # 'band_gap',
    # 'band_gap_dis',                                                 #  1
    
    # 'density',
    # 'density_dis',                                                  #  1
    
    # 'total_magnetization',
    # 'total_magnetization_dis',                                  

    # 'nsites',
    # 'nsites_dis',

    # 'elasticity',
    # 'elasticity_dis'   


    # 'radius_charged',
    # 'elneg_charged',
    # 'elneg_discharged',
    # 'vdw_charged',
    # 'vdw_discharged',
    # 'polar_charged',
    # 'polar_discharged'
    ]



    if l_charged_atoms:
    	for ii in [
    	'F_vol','Ni_vol','O_vol','Cr_vol','Mn_vol','As_vol','Mo_vol',
    'Cu_vol','Bi_vol','S_vol','P_vol','V_vol','Fe_vol','Sn_vol','Si_vol',
    'W_vol','Ti_vol','Co_vol','Sb_vol','Ge_vol','Mg_vol'
    #
    # ,'La_vol'
    ]:
     	   list_of_predictors.append(ii)
    
    if l_discharged_atoms:
    	for ii in [
    		'Ge_vol_dis', 'W_vol_dis', 'V_vol_dis', 'Sn_vol_dis', 'Ba_vol_dis', 'P_vol_dis', 
    'O_vol_dis', 'Fe_vol_dis', 'Ni_vol_dis', 'Ti_vol_dis', 'Mg_vol_dis', 
    'Co_vol_dis', 'F_vol_dis', 'Cr_vol_dis', 'Cu_vol_dis', 
    'Mo_vol_dis', 'Si_vol_dis', 'Mn_vol_dis', 'Bi_vol_dis', 'As_vol_dis', 'Te_vol_dis', 
    'S_vol_dis', 'Sb_vol_dis',
    #elements with 1 - 3 materials
    'Ta_vol_dis', 
    'Se_vol_dis',
    'Pr_vol_dis',
    # 'La_vol_dis',
    'Sr_vol_dis',
    'Nb_vol_dis',
    'N_vol_dis'
    ]:
    		list_of_predictors.append(ii)
    
    if APRDF:
        for ii in [
    'elneg_r2.0','diselneg_r2.0','elneg_r2.25','diselneg_r2.25','elneg_r2.5','diselneg_r2.5','elneg_r2.75','diselneg_r2.75',
    'elneg_r3.0','diselneg_r3.0','elneg_r3.25','diselneg_r3.25','elneg_r3.5','diselneg_r3.5','elneg_r3.75','diselneg_r3.75',
    'elneg_r4.0','diselneg_r4.0','elneg_r4.25','diselneg_r4.25','elneg_r4.5','diselneg_r4.5','elneg_r4.75','diselneg_r4.75',
    # 'elneg_r5.0','diselneg_r5.0','elneg_r5.25','diselneg_r5.25','elneg_r5.5','diselneg_r5.5','elneg_r5.75','diselneg_r5.75',
    # 'elneg_r6.0','diselneg_r6.0','elneg_r6.25','diselneg_r6.25','elneg_r6.5','diselneg_r6.5','elneg_r6.75','diselneg_r6.75',
    # 'elneg_r7.0','diselneg_r7.0','elneg_r7.25','diselneg_r7.25','elneg_r7.5','diselneg_r7.5','elneg_r7.75','diselneg_r7.75',
    # 'elneg_r8.0','diselneg_r8.0','elneg_r8.25','diselneg_r8.25','elneg_r8.5','diselneg_r8.5','elneg_r8.75','diselneg_r8.75',
    # 'elneg_r9.0','diselneg_r9.0','elneg_r9.25','diselneg_r9.25','elneg_r9.5','diselneg_r9.5','elneg_r9.75','diselneg_r9.75',
    # 'elneg_r10.0','diselneg_r10.0','elneg_r10.25','diselneg_r10.25','elneg_r10.5','diselneg_r10.5','elneg_r10.75','diselneg_r10.75',
    # 'elneg_r11.0','diselneg_r11.0','elneg_r11.25','diselneg_r11.25','elneg_r11.5','diselneg_r11.5','elneg_r11.75','diselneg_r11.75',
    # 'elneg_r12.0','diselneg_r12.0','elneg_r12.25','diselneg_r12.25','elneg_r12.5','diselneg_r12.5','elneg_r12.75','diselneg_r12.75',
    # 'elneg_r13.0','diselneg_r13.0','elneg_r13.25','diselneg_r13.25','elneg_r13.5','diselneg_r13.5','elneg_r13.75','diselneg_r13.75',
    # 'elneg_r14.0','diselneg_r14.0','elneg_r14.25','diselneg_r14.25','elneg_r14.5','diselneg_r14.5','elneg_r14.75','diselneg_r14.75',
    # 'elneg_r15.0','diselneg_r15.0'
    ]:
            list_of_predictors.append(ii)

    if l_charged_atoms_Li:
        for ii in [
    'Co_vol','H_vol','V_vol','Bi_vol','Sb_vol',
    'Nb_vol','C_vol','P_vol','As_vol','Mn_vol',
    'O_vol','La_vol','Na_vol','Fe_vol','W_vol',
    'Ti_vol','K_vol','Ni_vol','Mg_vol','Mo_vol',
    'Te_vol','Sn_vol','F_vol','Ba_vol','Cr_vol',
    'S_vol','Cu_vol','B_vol','Li_vol','Si_vol',

    #Elements with to few data points
'Cl_vol','Zr_vol','U_vol','Pr_vol','Cs_vol','Ta_vol','Ga_vol','Re_vol','Y_vol','Ca_vol','Rb_vol','Sc_vol','Pt_vol','Au_vol','Al_vol','In_vol','Pd_vol','Tl_vol','Nd_vol','Rb_vol','Sr_vol','Se_vol','Ge_vol','Zn_vol'
]:
           list_of_predictors.append(ii)
    if l_discharged_atoms_Li:
        for ii in [
'Co_vol_dis','H_vol_dis','V_vol_dis','Bi_vol_dis','Nb_vol_dis',
'C_vol_dis','P_vol_dis','As_vol_dis','Mn_vol_dis','Fe_vol_dis',
'O_vol_dis','La_vol_dis','Sb_vol_dis','Ti_vol_dis','K_vol_dis',
'Ni_vol_dis','Mg_vol_dis','Mo_vol_dis','Na_vol_dis','Te_vol_dis',
'Sn_vol_dis','F_vol_dis','Ba_vol_dis','Cr_vol_dis','S_vol_dis',
'Cu_vol_dis','B_vol_dis','Li_vol_dis','Si_vol_dis','W_vol_dis',

'Ge_vol_dis','Sr_vol_dis','Nd_vol_dis','Tl_vol_dis','Pd_vol_dis','In_vol_dis','Al_vol_dis','Au_vol_dis','Pt_vol_dis','Sc_vol_dis','Zn_vol_dis','Rb_vol_dis','Ca_vol_dis','Y_vol_dis','Re_vol_dis','Ga_vol_dis','Ta_vol_dis','Cs_vol_dis','Pr_vol_dis','U_vol_dis','Zr_vol_dis','Cl_vol_dis','Se_vol_dis' 

    ]:
            list_of_predictors.append(ii)


    
    list_of_predictors.append(Target)
    
    
    data = pd.read_csv(csv, sep=',')    #Swap data and df in to_csv

    # headers = list(data.head())

    df = pd.DataFrame()


    for fld in list_of_predictors:
       df[fld] = data[fld]
    # df.loc[~(df==0).all(axis=1)] #Not needed. 


    # df = df.round(6)
    # df = df.fillna(0)

    # df = drop_zeros(df)

    df.to_csv(outcsv,sep=',',index=False)

    print(Target, list_of_predictors)



if __name__ == '__main__':
    main()



