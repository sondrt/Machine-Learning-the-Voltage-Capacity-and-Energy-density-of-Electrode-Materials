from pymatgen.ext.matproj import MPRester
from pprint import pprint
from os import path
import numpy as np
import random
import pandas as pd
import json
import sys



foundation_df = pd.read_csv('out_csv_dis.csv',sep=',')
helvol_geomvol_df = pd.read_csv('helvol_geomvol_output.csv',sep=',')

df_new = pd.merge(foundation_df, helvol_geomvol_df, left_on='Charged_ID', right_on='mid')
df_new = pd.merge(df_new, helvol_geomvol_df, left_on='Discharged_ID', right_on='mid',
	suffixes = ('', '_dis'))
df_new = df_new.drop(columns = ['mid','mid_dis'])

df_new.to_csv("allFiles.csv", sep=",", index=False)