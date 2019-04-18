from pymatgen.ext.matproj import MPRester
from pprint import pprint
from os import path
import numpy as np
import random
import pandas as pd
import json
import sys



foundation_df 		= pd.read_csv('out_csv_dis.csv',sep=',')
helvol_geomvol_df 	= pd.read_csv('helvol_geomvol_output.csv',sep=',')
add_features_df 	= pd.read_csv('material_properties.csv',sep=',')

#merging manuel and helvol_geomvol
df_new = pd.merge(foundation_df, helvol_geomvol_df, left_on='Charged_ID', right_on='mid')

df_new = pd.merge(df_new, helvol_geomvol_df, left_on='Discharged_ID', right_on='mid',
	suffixes = ('', '_dis'))

df_firstdone = df_new.drop(columns = ['mid','mid_dis'])

#merging features.
list_2_nodups = add_features_df.drop_duplicates()

df_fp2 = pd.merge(df_firstdone, list_2_nodups, left_on = 'Discharged_ID', right_on = 'mid')
df_sp2 = pd.merge(df_fp2, list_2_nodups, left_on = 'Charged_ID', right_on = 'mid',
	suffixes = ('','_dis'))

df_seconddone = df_sp2.drop(columns = ['mid','mid_dis'])
# list_2_nodups = list_2.drop_duplicates()
# pd.merge(list_1 , list_2_nodups , on=['email_address'])

#Is this even my finall form?
df_seconddone.to_csv("allFiles.csv", sep=",", index=False)


################################

#Merge features.


