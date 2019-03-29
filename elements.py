from pymatgen.ext.matproj import MPRester
from pprint import pprint
from os import path
import numpy as np
import random
import pandas as pd
import json

def isNaN(num):
    return num != num

def readElements(filename):
    #Reads things you want form file 
    with open(filename) as json_file:
        data = json.load(json_file)[0]
        elements = data['elements']
        unit_cell_formula= data['unit_cell_formula']
        volume = data['volume']
    return elements, unit_cell_formula, volume
########################################################
csvfile = 'manual.csv'
cif_info_dir = './cif_info_dir/'
data = pd.read_csv(csvfile, sep=',')
#print(list(data.head()))
#print(data['Charged_ID'])

#makes a list of all elements and 
AllElements = []
for id in data['Charged_ID']:
    if isNaN(id)==False:
        fn = cif_info_dir + id + '_prop.dat'
        try:
            elements0, unit_cell_formula0, volume0 = readElements(fn)
#            print('list0=', elements0)
            for iel, el in enumerate(elements0):
                AllElements.append(elements0[iel])
        except: 
            print("not working ID: ", id)
#            print('File not found', fn)

#print('All elements=',AllElements)

AllE = list(set(AllElements))
#delete(AllElements)


nfiles = len(data['Charged_ID'])
print("AllE   ",AllE)
for el in AllE:
#   data[el + '_vol'] = np.linspace(0, nfiles, nfiles-1)
  data[el + '_vol'] = [0.]*nfiles

print("#################################")
#print("nO= ", data["O_vol"])
for iqid,qid in enumerate(data['Charged_ID']):
    mid = data['Battid'][iqid]
#    print("mid: ", mid)

#    print('mid, qid=', mid, qid)
    if isNaN(qid) == False:
        fn = cif_info_dir + qid + '_prop.dat'
        try:
            elements0, unit_cell_formula0, volume0 = readElements(fn)
            elems  = unit_cell_formula0
            for iel, el in enumerate(elements0):
                nel = elems[el]
                normVol = nel*1000. / volume0  
                data[el+'_vol'][iqid] = normVol
        except: 
            print('File not found', fn)

df = pd.DataFrame(data)
df.to_csv("out_csv_charged.csv",sep=',',index=False)
####################################################



#makes a list of all elements and 
AllElements_dis = []
for id in data['Discharged_ID']:
    if isNaN(id)==False:
        fn_dis = cif_info_dir + id + '_prop.dat'
        try:
            elements0, unit_cell_formula0, volume0 = readElements(fn_dis)
            for iel, el in enumerate(elements0):
                AllElements_dis.append(elements0[iel])
        except: 
            print("not working ID: ", id)


AllE_dis = list(set(AllElements))



nfiles_dis = len(data['Discharged_ID'])
print("AllE   ",AllE_dis)
for el in AllE_dis:
#   data[el + '_vol'] = np.linspace(0, nfiles, nfiles-1)
  data[el + '_vol_dis'] = [0.]*nfiles_dis
#print("nO= ", data["O_vol"])
for iqid,qid in enumerate(data['Discharged_ID']):
    mid = data['Battid'][iqid]

    if isNaN(qid) == False:
        fn_dis = cif_info_dir + qid + '_prop.dat'
        try:
            elements0, unit_cell_formula0, volume0 = readElements(fn_dis)
            elems  = unit_cell_formula0
#            print('=====>', elements0, volume0, '  +    print("elems: ", elems)++  ', elems)
            for iel, el in enumerate(elements0):
                nel = elems[el]
#                print("el= ", el, "   nel=", nel)
                normVol = nel*1000. / volume0  
#                print(normVol)
                data[el+'_vol_dis'][iqid] = normVol
        except: 
            print('File not found', fn_dis)

df_dis = pd.DataFrame(data)
df_dis.to_csv("out_csv_dis.csv",sep=',',index=False)
























