# Reades aprdf
import fnmatch
import os
import pprint
import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd
import pprint

#time
from datetime import date
today = date.today()
# dd/mm/YY
d1 = today.strftime("%Y-%m-%d-")
#print("d1 =", d1)

outcsv = "../battery_data_after_aprdf_merge.csv" #name&location of csv file with aprdf and more.


def read_aprdf(fn):
# Reads aprdf files and sorts them into 4 list, Radius, electronegativity, 
# von der wals volume, polarizability. 
    R     = []
    elneg = []
    vdw   = []
    polar = []

    f = open(fn,'r')
    print(fn)
    lines = f.readlines()
    for line in lines[1:]:
        a = (line.split())
        # print(a)
        R.append(float(a[0]))
        elneg.append(float(a[1]))
        vdw.append(float(a[2]))
        polar.append(float(a[3]))

        d = {'materialid':fn.strip('.aprdf'),'radius':R,'elneg':elneg,'vdw':vdw, 'polar':polar }
        df = pd.DataFrame(data=d)
    return df

def readandplotaprdf():
    dirin = './'
    files = os.listdir(dirin)
    
    plot = True
    show = False
    sample = True #only change a few samples: set maxcount.
    maxcount = 2

    count = 0
    for file in files:

        if fnmatch.fnmatch(file,'m*.aprdf'):
            R,elneg,vdw,polar = read_aprdf(file)

            if plot is True:
                plt.title(file)
                plt.plot(elneg)
                plt.plot(vdw)
                plt.plot(polar)
                plt.xlim(2,15)
                plt.ylim(0,2)
                plt.yticks([])

                if show is True:
                    plt.show()

                date_nameoffig= d1 + file.replace('.aprdf','.jpg')
                location_date_nameoffig = 'aprdf_result_plots/' + date_nameoffig
        #        print('Name of fig: ', nameoffig)
                plt.savefig(location_date_nameoffig, dpi=None, facecolor='w', edgecolor='w',
                    orientation='portrait', papertype=None, format=None,
                    transparent=False, bbox_inches=None, pad_inches=0.1,
                    frameon=None, metadata=None)
                plt.clf()
            if sample is True:
                print("round: ", count)
                count += 1
                if count == maxcount:
                    exit()

#csvout = ''

def writer():
    #Writing a csv file that can be .crossproduct with the csv for RF. 
    #
    dirin = "./"
    files = os.listdir(dirin)
    sample = False #only change a few samples: set maxcount.
    maxcount = 3
    count = 0
    for file in files:
        if fnmatch.fnmatch(file,'m*.aprdf'):
            print(file)

            df = read_aprdf(file)
            # print(df)
            newfn = file.replace(".aprdf",".csv")
            # print(newfn)
            df.to_csv(newfn, index=False)
            # print(df)
            if sample is True:
                print("round: ", count)
                count += 1
                if count == maxcount:
                    exit()        

    return

left = pd.DataFrame({'col1' : ['A', 'B', 'C'], 'col2' : [1, 2, 3]})
right = pd.DataFrame({'col1' : ['X', 'Y', 'Z'], 'col2' : [20, 30, 50]})



def mergeBandS():
    #Big old csv
    Bcsv = '../allFiles.csv'
    dirin = './'

    files=os.listdir(dirin)
    for file in files:
        if fnmatch.fnmatch(file,'m*.csv'):
            sdf = pd.read_csv(file)

            headers = list(sdf.head())
            # print(headers)
            # print(sdf)
            sdf.drop(sdf.columns[0], axis = 1, inplace = True) 
            # print("this thing: ", sdf)
            # print(df)
            newframe = pd.read_csv(Bcsv)
            headers = list(newframe.head())
            newframe.to_csv('Bcsv.csv')
            
            aprdf_data = merge_aprdf_for_RF(newframe)
            merged_aprdf_data = newframe.merge(aprdf_data, on='Battid')

            merged_aprdf_data.to_csv('../battery_data_after_aprdf_merge.csv')
            exit()

def merge_charged_discharged_aprdf(discharged: str, charged: str):
    charged_df = pd.read_csv(charged + ".csv").add_suffix('_charged')
    discharged_df = pd.read_csv(discharged + ".csv").add_suffix('_discharged')
    return pd.concat([charged_df, discharged_df], axis=1)

def merge_aprdf_for_RF(RF_data):
    merged_aprdf_list = RF_data.apply(axis=1, func=aprdf_df_merger)
    return pd.concat(merged_aprdf_list.to_list())

def aprdf_df_merger(battery_row):
    merged_df = merge_charged_discharged_aprdf(battery_row[1],battery_row[2])
    merged_df.insert(0, 'Battid', battery_row[0])
    merged_df.drop("")
    #print(merged_df)
    return merged_df





#writer()
#print(merge_charged_discharged_aprdf('mp-540570','mvc-12771'))
#print("Yes, i'm doing something")
# readandplotaprdf()



#mergeBandS()

