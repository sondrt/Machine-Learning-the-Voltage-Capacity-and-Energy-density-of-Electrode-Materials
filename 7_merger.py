from pymatgen.ext.matproj import MPRester
from pprint import pprint
from os import path
import numpy as np
import random
import pandas as pd
import json
import sys

foundation_df 		= pd.read_csv('Li_out_csv_dis.csv',sep=',')	
helvol_geomvol_df 	= pd.read_csv('Li_helvol_geomvol_output.csv',sep=',') #specify Mg or Li 
add_features_df 	= pd.read_csv('Li_material_properties.csv',sep=',')
# print(foundation_df)
# print(helvol_geomvol_df)
# print(add_features_df)
def totalmerge():
	#merging manuel and helvol_geomvol
	# df_new = pd.merge(foundation_df, helvol_geomvol_df, left_on='Charged_ID', right_on='mid')
	df_new = pd.merge(foundation_df, helvol_geomvol_df, how='inner', left_on='Charged_ID',right_on='mid')
	df_new = pd.merge(df_new, helvol_geomvol_df, left_on='Discharged_ID', right_on='mid', suffixes = ('', '_dis'))
	df_firstdone = df_new.drop(columns = ['mid','mid_dis'])
	#merging features.
	list_2_nodups = add_features_df.drop_duplicates()
	df_fp2 = pd.merge(df_firstdone, list_2_nodups, left_on = 'Discharged_ID', right_on = 'mid')
	df_sp2 = pd.merge(df_fp2, list_2_nodups, left_on = 'Charged_ID', right_on = 'mid',
		suffixes = ('','_dis'))

	df_seconddone = df_sp2.drop(columns = ['mid','mid_dis'])
	#write to file
	df_seconddone.to_csv("Li_allFiles.csv", sep=",", index=False)
	return

def mergefeaturesandfoundation():
	#excluding the voidfraction
	df_foundationandfeatures = pd.merge(foundation_df, add_features_df, left_on='Charged_ID', right_on='mid')
	df_foundationandfeatures = pd.merge(df_foundationandfeatures, add_features_df, left_on='Discharged_ID', right_on='mid',
		suffixes = ('', '_dis'))
	df_done = df_foundationandfeatures.drop(columns = ['mid','mid_dis'])
	df_list = df_done.drop_duplicates()
	df_list.to_csv("allFiles.csv", sep=",", index=False)
	return

#Select mergertype: 
var = int(input("press 1 to merge Manual and material properties, press 2 to include the voidfraction: "))
try:
	if var == 1:
		mergefeaturesandfoundation()
		print("Volumetric numberdensity merged with other material properties.")
	elif var == 2: 
		totalmerge()
		print("Everything merged!(maybe)")
except: 
	"valueerror"



#mergefeaturesandfoundation()



################################

#Merge features.


