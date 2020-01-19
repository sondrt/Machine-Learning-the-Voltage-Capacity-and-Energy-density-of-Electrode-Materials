import urllib.request
import pandas as pd
import sys
from urllib.request import Request, urlopen

df = pd.read_csv("./mp.csv")
outcsv= "newcsv.csv"
counter = 0
renamed_materials = []	#all old ids
mp_that_does_not_work = "nfmps.csv"
f = open(mp_that_does_not_work,'w+')


for i in df:
	material_id = i
	renamed_materials.append(material_id)
	print("fetching real id for: ", i)
	url = 'https://materialsproject.org/materials/' + material_id
	try:
		req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
		webpage = urlopen(req).read()	
		x = str(webpage)
		y = (x[49:58]).replace(":","")
		print("real id is: ", y)
		y = y.replace(" ","")
		renamed_materials.append((material_id, y))
	except:
		print("material id: ",i, "did not function.")
		f.write(i+",")


li_df = pd.read_csv("Li_batteries.csv")

for i in li_df["Discharged_ID"]:
	for j in invalid_materials:
		if i == j:
			#print("old: ", i, "new: ", all_ids.index(j))
			print(i)
			li_df = li_df.replace({i,j})

for i in li_df["Charged_ID"]:
	for j in invalid_materials:
		if i == j:
			#print("old: ", i, "new: ", all_ids.index(j))
			li_df = li_df.replace({i,j})

li_df.to_csv(outcsv,sep=',',index=False)
f.close()
