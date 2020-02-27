#Aprdf_row_approach.py
import fnmatch
import os
import pprint
import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd


#files:
def main():
    Bcsv = '../allFiles.csv'
    dirin = './'
    x = np.linspace(2,15,53)
    files=os.listdir(dirin)
    newframe = pd.read_csv(Bcsv)


            # add empty colomn
    for i in x:
        nameofheader = 'elneg_r' + str(i)
        nameofdisheader = 'diselneg_r' + str(i)
        newframe[nameofheader] = np.nan
        newframe[nameofdisheader] = np.nan
        print(nameofheader)
        print(nameofdisheader)
    exit()
            # print(newframe.iloc[0:355,1:3])

    for i in range(0,355):
        counter_charged = 0
        counter_discharged = 0
        # print("forste loop: ", newframe.iloc[i:i+1,1:3])
        mattid = newframe.iloc[i:i+1,1:3]
        for j in range(93,199):
            print("teller j:", j)
            elneglist_Discharged, elneglist_Charged = get_elneg(mattid,i)
            if is_odd(j) == True:
                print('er odd: ', counter_charged)
                newframe.iloc[i:i+1, j:j+1] = elneglist_Charged[counter_charged]
                counter_charged += 1 
            if is_odd(j) == False:
                print('er ikke odd')
                newframe.iloc[i:i+1, j:j+1] = elneglist_Discharged[counter_discharged]
                counter_discharged += 1



            print(newframe.iloc[i:i+1, j:j+1])

    return newframe

def get_elneg(mattid,i):
    Discharged_ID = mattid['Discharged_ID'][i]
    Charged_ID = mattid['Charged_ID'][i]
    aprdf_file_Charged = pd.read_csv(Charged_ID + ".csv")
    aprdf_file_Discharged = pd.read_csv(Discharged_ID + ".csv")

    elneglist_Charged = aprdf_file_Charged["elneg"]
    elneglist_Discharged = aprdf_file_Discharged["elneg"]
    return elneglist_Discharged, elneglist_Charged

def is_odd(num):
    try:
        if (num % 2) == 0:
           return False
        else:
           return True
    except:
        print("Something went wrong in is_odd!")



df = pd.DataFrame(main())
df = df.loc[:, (df != 0).any(axis=0)]
df.to_csv('../nyfilmedmassetall.csv')

