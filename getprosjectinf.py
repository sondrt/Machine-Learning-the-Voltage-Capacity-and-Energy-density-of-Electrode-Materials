import urllib.request
import pandas as pd
import sys
from urllib.request import Request, urlopen

input_material_ids = pd.read_csv("./mp.csv")
outcsv= "newcsv.csv"
renamed_materials = {}	# renamed ids mapped to new names
missing_material_ids_path = "nfmps.csv"
missing_material_ids_file = open(missing_material_ids_path,'w+')


for material_id in input_material_ids:
	print("fetching real id for: ", material_id)
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
		print("material id: ",material_id, " never existed or has been renamed wrongly.")
		missing_material_ids_file.write(material_id + ",")


li_batteries = pd.read_csv("Li_batteries.csv")
li_batteries = li_batteries.replace(renamed_materials)
li_batteries.to_csv(outcsv,sep=',',index=False)

missing_material_ids.close()
