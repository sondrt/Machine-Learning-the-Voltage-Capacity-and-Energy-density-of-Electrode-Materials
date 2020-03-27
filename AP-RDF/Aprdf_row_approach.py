#Aprdf_row_approach.py
import fnmatch
import os
import pprint
import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd


def main():

    Bcsv = '../Li_allFiles.csv'
    x = np.linspace(2,15,53)
    df = pd.read_csv(Bcsv)
    # print(df.shape[0])

            # add empty colomn
    for i in x:
        nameofheader = 'elneg_r' + str(i)
        nameofdisheader = 'elnegdis_r' + str(i)
        df[nameofheader] = np.nan
        df[nameofdisheader] = np.nan
    for i in x:
        nameofheader2 = 'vdw_r' + str(i)
        nameofdisheader2 = 'vdwdis_r' + str(i)
        df[nameofheader2] = np.nan
        df[nameofdisheader2] = np.nan
    for i in x:
        nameofheader3 = 'polar_r' + str(i)
        nameofdisheader3 = 'polardis_r' + str(i)
        df[nameofheader3] = np.nan
        df[nameofdisheader3] = np.nan
        # print(nameofheader)
        # print(nameofdisheader)
            # print(df.iloc[0:355,1:3])

    df = values(df)

    df.to_csv('../test.csv')
        # print(df)
        # exit()
    return df

def values(df):

    for i in range(0,df.shape[0]):
        counter_charged = 0
        counter_discharged = 0
        # print("forste loop: ", df.iloc[i:i+1,1:3])
        mattid = df.iloc[i:i+1,1:3]
        for j in range(141,247):
            print("teller j:", j)
            # print('j thing, ',df.iloc[i:i+1, j:j+1])
            elneglist_Discharged, elneglist_Charged = get_elneg(mattid,i)
            if is_odd(j) == True:
                print('cn Charged: ', counter_charged)
                df.iloc[i:i+1, j:j+1] = elneglist_Charged[counter_charged]
                counter_charged += 1 
            if is_odd(j) == False:
                print('cn Discharged: ', counter_discharged )
                df.iloc[i:i+1, j:j+1] = elneglist_Discharged[counter_discharged]
                counter_discharged += 1
            print(df.iloc[i:i+1, j:j+1])
            # exit()
        #reset counters
        counter_charged = 0
        counter_discharged = 0
        print('step 2')

        for h in range(247,353):
            print("teller h:", h)
            # print('j thing, ',df.iloc[i:i+1, j:j+1])
            vdwlist_Discharged, vdwlist_Charged = get_vdw(mattid,i)
            # print('charged: ',vdwlist_Charged, 'discharged', vdwlist_Discharged)
            if is_odd(h) == True:
                print('er odd: ', counter_charged)
                df.iloc[i:i+1, h:h+1] = vdwlist_Charged[counter_charged]
                counter_charged += 1 
            if is_odd(h) == False:
                print('er ikke odd', counter_discharged)
                df.iloc[i:i+1, h:h+1] = vdwlist_Discharged[counter_discharged]
                counter_discharged += 1
            print(df.iloc[i:i+1, h:h+1])
        #reset counters
        counter_charged = 0
        counter_discharged = 0
        print('step 3')
        for h in range(353,459):
            print("teller h:", h)
            polarlist_Discharged, polarlist_Charged = get_polar(mattid,i)
            # print('charged: ',polarlist_Charged, 'discharged', polarlist_Discharged)
            if is_odd(h) == True:
                print('er odd: ', h)
                df.iloc[i:i+1, h:h+1] = polarlist_Charged[counter_charged]
                # print('polarlist: ',df.iloc[i:i+1, h:h+1])
                counter_charged += 1 
            if is_odd(h) == False:
                print('er ikke odd', h)
                df.iloc[i:i+1, h:h+1] = polarlist_Discharged[counter_discharged]
                counter_discharged += 1
            print(df.iloc[i:i+1, h:h+1])
    return df


def get_elneg(mattid,i):
    #Get elneg values from csv files meant for cross-prod files created by Reader_aprdf
    Discharged_ID = mattid['Discharged_ID'][i]
    Charged_ID = mattid['Charged_ID'][i]
    print(Charged_ID,Discharged_ID)
    aprdf_file_Charged = pd.read_csv(Charged_ID + ".csv")
    aprdf_file_Discharged = pd.read_csv(Discharged_ID + ".csv")

    elneglist_Charged = aprdf_file_Charged["elneg"]
    elneglist_Discharged = aprdf_file_Discharged["elneg"]
    return elneglist_Discharged, elneglist_Charged

def get_vdw(mattid,i):
    #thefiles are mixed up so vdw are polar and visa versa
    #Get elneg values from csv files meant for cross-prod files created by Reader_aprdf
    Discharged_ID = mattid['Discharged_ID'][i]
    Charged_ID = mattid['Charged_ID'][i]
    print(Charged_ID,Discharged_ID)
    aprdf_file_Charged = pd.read_csv(Charged_ID + ".csv")
    aprdf_file_Discharged = pd.read_csv(Discharged_ID + ".csv")
    vdwlist_Charged = aprdf_file_Charged["vdw"]
    vdwlist_Discharged = aprdf_file_Discharged["vdw"]
    return vdwlist_Charged, vdwlist_Discharged
def get_polar(mattid,i):
    #Get elneg values from csv files meant for cross-prod files created by Reader_aprdf
    Discharged_ID = mattid['Discharged_ID'][i]
    Charged_ID = mattid['Charged_ID'][i]
    print(Charged_ID,Discharged_ID)

    aprdf_file_Charged = pd.read_csv(Charged_ID + ".csv")
    aprdf_file_Discharged = pd.read_csv(Discharged_ID + ".csv")

    polarlist_Charged = aprdf_file_Charged["polar"]
    polarlist_Discharged = aprdf_file_Discharged["polar"]
    return polarlist_Charged, polarlist_Discharged

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

