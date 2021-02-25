import urllib.request
import pandas as pd
import sys
from urllib.request import Request, urlopen
import os
import json

#
# Search through the mp's making sure they 
# match with the API, by fetching html title. 
#
# Output files: <ion>_batteries.csv
#


input_material_ids = pd.read_csv("./notworking.csv")
renamed_materials = {}  # renamed ids mapped to new names
missing_material_ids_path = "nfmps.csv" #Not functioning materials
missing_material_ids_file = open(missing_material_ids_path,'w+')

def getprojectinf():
    for material_id in input_material_ids:
        print("fetching real id for: ", material_id)
        url = 'https://materialsproject.org/materials/' + material_id
        # print(url) #!!! Might need too check URL !!!
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

    renamed_batteries_path = "newcsv.csv"
    All_batteries = pd.read_csv("All_batteries.csv")
    All_batteries = All_batteries.replace(renamed_materials)
    All_batteries.to_csv(renamed_batteries_path, sep=',', index=False)

    missing_material_ids_file.close()
    return

# def changemaincsv():
#   df = pd.read_csv('newcsv.csv')
#   for material_id in lst_nfmps:
#       print(material_id)

#   return

def remove_empty_files():
    #Removes files in given directory if size = 2 bytes
    directory = './cif_info_dir/'
    for file in os.listdir(directory):
        # print(os.path.getsize(directory+file))
        if os.path.getsize(directory+file) == 2:
            print('file of size 2 bytes: ', file)
            cmd = 'rm ' + directory+file
            print('File ', file,' of size ',os.path.getsize(directory+file), ' was removed.')
            os.system(cmd)

    return()





# remove_empty_files()
# changemaincsv()
getprojectinf()




