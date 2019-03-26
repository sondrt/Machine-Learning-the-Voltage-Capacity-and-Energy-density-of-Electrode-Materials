from pymatgen.ext.matproj import MPRester
from pprint import pprint
from os import path
import numpy as np
import random
import pandas as pd
import json
import sys


#Files = ['manual.csv', 'out_csv']

#df1 = pd.read_csv('manual.csv',sep=",")
df2 = pd.read_csv("out_csv",sep=",")

#df_new = pd.merge(df1, df2, on='Battid')

df_new.to_csv("allFiles.csv")


# for ifl, fl in enumerate(Files):
#     if ifl>0:
#     	dfi = pd.DataFrame(Files[ifl])
#     	headersI = 

print(sys.argv)


#pprint(list(df2.head()))

#open("","r") 




















