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


#python prep_csv.py >> Results/2020-03-10/2020-03-10.txt; python PCA_randomforest_crossvalidation.py >>  Results/2020-03-10/2020-03-10.txt;

T = True
F = False

def main():
    csv = 'allFiles.csv'    
    outcsv = 'for_ML.csv'
    print('File: ', csv)

    Target              = 'Average_Voltage'
# Targets: Average_Voltage, Capacity_Grav, Capacity_Vol, Specific_E_Wh/kg, E Density Wh/l


    l_charged_atoms     = T   #turns on fraction density predictor for charged material
    l_discharged_atoms  = T   #turns on fraction density predictor for discharged material
    APRDF = False

    list_of_predictors= ['Battid', 
    # 'Reduced_Cell_Formula',           # Not operational.
    # 'Spacegroup',                     # Not operational.  
    # 'formation_energy_per_atom',      # Not operational.
    # 'formation_energy_per_atom_dis',  # Not operational.

    
    # 'Average_Voltage',
    # 'Capacity_Grav',
    # 'Capacity_Vol',
    # 'Specific_E_Wh/kg',
    # 'E Density Wh/l',
    
    # 'Stability Discharge',                                    
    # 'Stability Charge',                                       

    # 'energy',
    # 'energy_dis',

    # 'energy_per_atom',
    # 'energy_per_atom_dis',                                          #  1                       

    # 'band_gap',
    # 'band_gap_dis',                                                 #  1
    
    # 'density',
    # 'density_dis',                                                  #  1
    
    # 'total_magnetization',
    # 'total_magnetization_dis',                                  

    # 'nsites',
    # 'nsites_dis',

    # 'elasticity',
    # 'elasticity_dis',

    # 'volume',
    # 'volume_dis', 


    # 'helvol',                                                 
    # 'geomvol',
    # 'helvol_dis',
    # 'geomvol_dis',

    # 'vf_geomvol',
    # 'vf_geomvol_dis',
    # 'vf_helvol',
    # 'vf_helvol_dis',



#operational with right csv
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
    'Sn_vol', 'V_vol', 'Sr_vol', 'Ir_vol', 'Rh_vol', 
    'Co_vol', 'Te_vol', 'Ta_vol', 'Zn_vol', 'Zr_vol', 
    'Tc_vol', 'P_vol', 'As_vol', 'Re_vol', 'Hg_vol', 
    'Mn_vol', 'Gd_vol', 'Ca_vol', 'Au_vol', 'U_vol', 
    'Fe_vol', 'Nb_vol', 'Cu_vol', 'Cs_vol', 'Pr_vol', 
    'F_vol', 'Ce_vol', 'Tl_vol', 'Cl_vol', 'Mo_vol', 
    'Na_vol', 'Ba_vol', 'I_vol', 'Nd_vol', 'Se_vol', 
    'Lu_vol', 'Ga_vol', 'B_vol', 'O_vol', 'Cr_vol', 
    'N_vol', 'S_vol', 'In_vol', 'Br_vol', 'Sb_vol', 
    'Pd_vol', 'H_vol', 'Mg_vol', 'Ti_vol', 'C_vol', 
    'Ru_vol', 'K_vol', 'Bi_vol', 'Rb_vol', 'Si_vol', 
    'Ge_vol', 'W_vol', 'La_vol', 'Sc_vol', 'Al_vol', 
    'Ho_vol', 'Y_vol', 'Li_vol', 'Ni_vol', 'Pt_vol', 'Tb_vol', 
    ]:
     	   list_of_predictors.append(ii)
    
    if l_discharged_atoms:
    	for ii in [
    'Sn_vol_dis','V_vol_dis','Sr_vol_dis','Ir_vol_dis',
    'Rh_vol_dis','Co_vol_dis','Te_vol_dis','Ta_vol_dis',
    'Zn_vol_dis','Zr_vol_dis','Tc_vol_dis','P_vol_dis',
    'As_vol_dis','Re_vol_dis','Hg_vol_dis','Mn_vol_dis',
    'Gd_vol_dis','Ca_vol_dis','Au_vol_dis','U_vol_dis',
    'Fe_vol_dis','Nb_vol_dis','Cu_vol_dis','Cs_vol_dis',
    'Pr_vol_dis','F_vol_dis','Ce_vol_dis','Tl_vol_dis',
    'Cl_vol_dis','Mo_vol_dis','Na_vol_dis','Ba_vol_dis',
    'I_vol_dis','Nd_vol_dis','Se_vol_dis','Lu_vol_dis',
    'Ga_vol_dis','B_vol_dis','O_vol_dis','Cr_vol_dis',
    'N_vol_dis','S_vol_dis','In_vol_dis','Br_vol_dis',
    'Sb_vol_dis','Pd_vol_dis','H_vol_dis','Mg_vol_dis',
    'Ti_vol_dis','C_vol_dis','Ru_vol_dis','K_vol_dis',
    'Bi_vol_dis','Rb_vol_dis','Si_vol_dis','Ge_vol_dis',
    'W_vol_dis','La_vol_dis','Sc_vol_dis','Al_vol_dis',
    'Ho_vol_dis','Y_vol_dis','Li_vol_dis','Ni_vol_dis',
    'Pt_vol_dis','Tb_vol_dis'
    ]:
    		list_of_predictors.append(ii)
    
    if APRDF:
        for ii in [
    'elneg_r2.0','elneg_r2.25','elneg_r2.5','elneg_r2.75',
    'elneg_r3.0','elneg_r3.25','elneg_r3.5','elneg_r3.75',
    'elneg_r4.0','elneg_r4.25','elneg_r4.5','elneg_r4.75',
    'elneg_r5.0','elneg_r5.25','elneg_r5.5','elneg_r5.75',
    'elneg_r6.0','elneg_r6.25','elneg_r6.5','elneg_r6.75',
    'elneg_r7.0','elneg_r7.25','elneg_r7.5','elneg_r7.75',
    'elneg_r8.0','elneg_r8.25','elneg_r8.5','elneg_r8.75',
    'elneg_r9.0','elneg_r9.25','elneg_r9.5','elneg_r9.75',
    'elneg_r10.0','elneg_r10.25','elneg_r10.5','elneg_r10.75',
    'elneg_r11.0','elneg_r11.25','elneg_r11.5','elneg_r11.75',
    'elneg_r12.0','elneg_r12.25','elneg_r12.5','elneg_r12.75',
    'elneg_r13.0','elneg_r13.25','elneg_r13.5','elneg_r13.75',
    'elneg_r14.0','elneg_r14.25','elneg_r14.5','elneg_r14.75',
    'elneg_r15.0',

    'elnegdis_r2.0','elnegdis_r2.25','elnegdis_r2.5','elnegdis_r2.75',
    'elnegdis_r3.0','elnegdis_r3.25','elnegdis_r3.5','elnegdis_r3.75',
    'elnegdis_r4.0','elnegdis_r4.25','elnegdis_r4.5','elnegdis_r4.75',
    'elnegdis_r5.0','elnegdis_r5.25','elnegdis_r5.5','elnegdis_r5.75',
    'elnegdis_r6.0','elnegdis_r6.25','elnegdis_r6.5','elnegdis_r6.75',
    'elnegdis_r7.0','elnegdis_r7.25','elnegdis_r7.5','elnegdis_r7.75',
    'elnegdis_r8.0','elnegdis_r8.25','elnegdis_r8.5','elnegdis_r8.75',
    'elnegdis_r9.0','elnegdis_r9.25','elnegdis_r9.5','elnegdis_r9.75',
    'elnegdis_r10.0','elnegdis_r10.25','elnegdis_r10.5','elnegdis_r10.75',
    'elnegdis_r11.0','elnegdis_r11.25','elnegdis_r11.5','elnegdis_r11.75',
    'elnegdis_r12.0','elnegdis_r12.25','elnegdis_r12.5','elnegdis_r12.75',
    'elnegdis_r13.0','elnegdis_r13.25','elnegdis_r13.5','elnegdis_r13.75',
    'elnegdis_r14.0','elnegdis_r14.25','elnegdis_r14.5','elnegdis_r14.75',
    'elnegdis_r15.0',

        'vdw_r2.0','vdw_r2.25','vdw_r2.5','vdw_r2.75',
    'vdw_r3.0','vdw_r3.25','vdw_r3.5','vdw_r3.75',
    'vdw_r4.0','vdw_r4.25','vdw_r4.5','vdw_r4.75',
    'vdw_r5.0','vdw_r5.25','vdw_r5.5','vdw_r5.75',
    'vdw_r6.0','vdw_r6.25','vdw_r6.5','vdw_r6.75',
    'vdw_r7.0','vdw_r7.25','vdw_r7.5','vdw_r7.75',
    'vdw_r8.0','vdw_r8.25','vdw_r8.5','vdw_r8.75',
    'vdw_r9.0','vdw_r9.25','vdw_r9.5','vdw_r9.75',
    'vdw_r10.0','vdw_r10.25','vdw_r10.5','vdw_r10.75',
    'vdw_r11.0','vdw_r11.25','vdw_r11.5','vdw_r11.75',
    'vdw_r12.0','vdw_r12.25','vdw_r12.5','vdw_r12.75',
    'vdw_r13.0','vdw_r13.25','vdw_r13.5','vdw_r13.75',
    'vdw_r14.0','vdw_r14.25','vdw_r14.5','vdw_r14.75',
    'vdw_r15.0',

'vdwdis_r2.0','vdwdis_r2.25','vdwdis_r2.5','vdwdis_r2.75','vdwdis_r3.0',
'vdwdis_r3.25','vdwdis_r3.5','vdwdis_r3.75','vdwdis_r4.0','vdwdis_r4.25',
'vdwdis_r4.5','vdwdis_r4.75','vdwdis_r5.0','vdwdis_r5.25','vdwdis_r5.5',
'vdwdis_r5.75','vdwdis_r6.0','vdwdis_r6.25','vdwdis_r6.5','vdwdis_r6.75',
'vdwdis_r7.0','vdwdis_r7.25','vdwdis_r7.5','vdwdis_r7.75','vdwdis_r8.0',
'vdwdis_r8.25','vdwdis_r8.5','vdwdis_r8.75','vdwdis_r9.0','vdwdis_r9.25',
'vdwdis_r9.5','vdwdis_r9.75','vdwdis_r10.0','vdwdis_r10.25','vdwdis_r10.5',
'vdwdis_r10.75','vdwdis_r11.0','vdwdis_r11.25','vdwdis_r11.5','vdwdis_r11.75',
'vdwdis_r12.0','vdwdis_r12.25','vdwdis_r12.5','vdwdis_r12.75','vdwdis_r13.0',
'vdwdis_r13.25','vdwdis_r13.5','vdwdis_r13.75','vdwdis_r14.0','vdwdis_r14.25',
'vdwdis_r14.5','vdwdis_r14.75','vdwdis_r15.0',

        'polar_r2.0','polar_r2.25','polar_r2.5','polar_r2.75',
    'polar_r3.0','polar_r3.25','polar_r3.5','polar_r3.75',
    'polar_r4.0','polar_r4.25','polar_r4.5','polar_r4.75',
    'polar_r5.0','polar_r5.25','polar_r5.5','polar_r5.75',
    'polar_r6.0','polar_r6.25','polar_r6.5','polar_r6.75',
    'polar_r7.0','polar_r7.25','polar_r7.5','polar_r7.75',
    'polar_r8.0','polar_r8.25','polar_r8.5','polar_r8.75',
    'polar_r9.0','polar_r9.25','polar_r9.5','polar_r9.75',
    'polar_r10.0','polar_r10.25','polar_r10.5','polar_r10.75',
    'polar_r11.0','polar_r11.25','polar_r11.5','polar_r11.75',
    'polar_r12.0','polar_r12.25','polar_r12.5','polar_r12.75',
    'polar_r13.0','polar_r13.25','polar_r13.5','polar_r13.75',
    'polar_r14.0','polar_r14.25','polar_r14.5','polar_r14.75',
    'polar_r15.0',
'polardis_r2.0','polardis_r2.25','polardis_r2.5','polardis_r2.75',
'polardis_r3.0','polardis_r3.25','polardis_r3.5','polardis_r3.75',
'polardis_r4.0','polardis_r4.25','polardis_r4.5','polardis_r4.75',
'polardis_r5.0','polardis_r5.25','polardis_r5.5','polardis_r5.75',
'polardis_r6.0','polardis_r6.25','polardis_r6.5','polardis_r6.75',
'polardis_r7.0','polardis_r7.25','polardis_r7.5','polardis_r7.75',
'polardis_r8.0','polardis_r8.25','polardis_r8.5','polardis_r8.75',
'polardis_r9.0','polardis_r9.25','polardis_r9.5','polardis_r9.75',
'polardis_r10.0','polardis_r10.25','polardis_r10.5','polardis_r10.75',
'polardis_r11.0','polardis_r11.25','polardis_r11.5','polardis_r11.75',
'polardis_r12.0','polardis_r12.25','polardis_r12.5','polardis_r12.75',
'polardis_r13.0','polardis_r13.25','polardis_r13.5','polardis_r13.75',
'polardis_r14.0','polardis_r14.25','polardis_r14.5','polardis_r14.75',
'polardis_r15.0',


    ]:
            list_of_predictors.append(ii)

    list_of_predictors.append(Target)
    
    
    data = pd.read_csv(csv, sep=',', low_memory=False)    #Swap data and df in to_csv
    data['vf_geomvol']= 0
    data['vf_geomvol_dis']= 0
    data['vf_helvol']= 0
    data['vf_helvol_dis'] = 0

    # headers = list(data.head())

    df = pd.DataFrame()

    for fld in list_of_predictors:
       df[fld] = data[fld]
  

    df.loc[~(df==0).all(axis=1)] #Not needed. 
    df = df.round(6)
    df = df.fillna(0)
    df = df.sample(frac=1)
    # if ('vf_geomvol_dis') in df: 
        
    #     df['vf_geomvol'] = df['geomvol'].div(df['volume'].values,axis=0)
    #     df['vf_geomvol_dis'] = df['geomvol_dis'].div(df['volume_dis'].values,axis=0)
    #     df['vf_helvol'] = df['helvol'].div(df['volume'].values,axis=0)
    #     df['vf_helvol_dis'] = df['helvol_dis'].div(df['volume_dis'].values,axis=0)
    #     # df = df.drop(['helvol','geomvol','helvol_dis','geomvol_dis'],axis=1)


    
    # df = df.insert(loc = 1, column= 'vf_geomvol_dis', value=0)
    # df['vf_geomvol_dis'] = df['geomvol_dis'].div(df['volume_dis'].values,axis=0)
    # df[['vf_geomvol','vf_geomvol_dis']] = df[['geomvol_dis','geomvol']].div(df['volume_dis','volume'].values,axis=0)
    df.to_csv(outcsv,sep=',',index=False)

    print(df.columns)





if __name__ == '__main__':
    main()
    # for cross-APRDF
    # df = df.sample(frac=1)
    # df = df[df['elneg_charged'] >= 0]
    # df = df[(df['elneg_charged'] > 0.7)]

