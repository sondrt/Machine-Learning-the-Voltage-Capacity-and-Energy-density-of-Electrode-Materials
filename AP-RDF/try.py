#try.py
import pandas as pd
import numpy as np

incsv = "../nyfilmedmassetall.csv" #name&location of csv file with aprdf and more.


df = pd.read_csv(incsv)

df.loc[~(df==0).all(axis=1)] #Not needed. 


df = df.round(6)
df = df.fillna(0)

df.to_csv('../test.csv',sep=',', float_format='%.9f')

