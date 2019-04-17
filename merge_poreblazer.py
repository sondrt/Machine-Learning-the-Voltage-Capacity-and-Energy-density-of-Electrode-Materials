
import os
import pandas as pd


struc_info = "./struc_info.csv"
id_list_csv = 'manual.csv'
outcsv = 'out_csv_dis.csv'

struc_df = pd.read_csv(struc_info, sep=',')
# HEADERS = list(struc_data.head())
#print('heads = ', HEADERS)
id_df = pd.read_csv(id_list_csv, sep=',')
print (struc_df)
print (id_df[])

for x in id_df['Discharged_ID']:
    for y in struc_df['Battid']:
        if x == y:
            print('These are the same: ',x,y)
            print(struc_df[x])


exit()
# print(type(struc_df["helvol"]))
# for ID in ['Battid','helvol', 'geomvol']:
#     for struc_id in struc_df[ID]:
#        print(struc_id)

    # print(helvol)
    # print(geomvol)

# for ID in ['Charged_ID','Discharged_ID']:
#     for struc_id in id_df[ID]:
#         struc_df[struc_id]
#         print(struc_df)
#         exit()






