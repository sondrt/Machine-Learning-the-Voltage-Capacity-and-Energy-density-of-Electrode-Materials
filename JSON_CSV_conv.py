import json
import numpy
import pandas as pd
import os
import csv

from pprint import pprint

cif_for_poreblazer = './cif_for_poreblazer/'
outcsv = './cif_for_poreblazer/cif_files/'


for filename in os.listdir(cif_for_poreblazer):
    try:
        with open('./cif_for_poreblazer/' + filename) as json_data:
            data = json.load(json_data)
            json_data.close()
      
        datadict = data[0]


        with open(outcsv + filename + '.csv','w+') as f:
            w = csv.DictWriter(f, datadict.keys())
            w.writeheader()
            w.writerow(datadict)

    except:
        print('This did not work: ', filename)
