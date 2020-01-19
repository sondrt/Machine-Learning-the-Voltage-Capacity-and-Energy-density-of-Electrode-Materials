import urllib.request
import pandas as pd
import sys
from urllib.request import Request, urlopen

df = pd.read_csv("./mp.csv")
outcsv= "newcsv.csv"
counter = 0
renamed_materials = {}	# renamed ids mapped to new names
mp_that_does_not_work = "nfmps.csv"
f = open(mp_that_does_not_work,'w+')


for i in df:
	material_id = i
	print("fetching real id for: ", i)
	url = 'https://materialsproject.org/materials/' + material_id
	try:
		req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
		webpage = urlopen(req).read()	
		x = str(webpage)
		y = (x[49:58]).replace(":","")
		print("real id is: ", y)
		y = y.replace(" ","")
		renamed_materials[material_id] = y
	except:
		print("material id: ",i, "did not function.")
		f.write(i+",")


li_df = pd.read_csv("Li_batteries.csv")
li_df.replace(renamed_materials)
li_df.to_csv(outcsv,sep=',',index=False)
f.close()
