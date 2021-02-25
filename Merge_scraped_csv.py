# A program for concating existing electrode files. 

import pandas as pd


file_types = ['Li','Ca','Cs','Rb','K','Y','Na','Al','Zn','Mg'] 
All_battery_types  = pd.DataFrame()
lst = []
for i in file_types:
	filename = str(i)+'_batteries.csv'
	df = pd.read_csv(filename, sep=',')
	lst.append(df)
result = pd.concat(lst,axis=0,sort = False)
result.to_csv("All_batteries.csv", sep=",", index=False)





