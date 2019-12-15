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

    return R,elneg,vdw,polar,lines

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
            read_aprdf(file)
            R,elneg,vdw,polar,a = read_aprdf(file)

            d = {'R':R,'elneg':elneg,'vdw':vdw, 'polar':polar }

            df = pd.DataFrame(data=d)
            print(df)
            newfn = file.replace(".aprdf",".csv")
            print(newfn)
            df.to_csv(newfn)

            if sample is True:
                print("round: ", count)
                count += 1
                if count == maxcount:
                    exit()        

    return

left = pd.DataFrame({'col1' : ['A', 'B', 'C'], 'col2' : [1, 2, 3]})
right = pd.DataFrame({'col1' : ['X', 'Y', 'Z'], 'col2' : [20, 30, 50]})


## Skriv en måte å ta kryssprodukt av csv df og stor CSV fil. 

def cartesian_product_simplified(left, right):
    la, lb = len(left), len(right)
    ia2, ib2 = np.broadcast_arrays(*np.ogrid[:la,:lb])

    return pd.DataFrame(
        np.column_stack([left.values[ia2.ravel()], right.values[ib2.ravel()]]))


#print(cartesian_product_simplified(left, right))

def mergeBandS():
    outcsv=()
    #Big old csv
    Bcsv = '../allfiles.csv'
    #new small csv's
    dirin = './'
    files=os.listdir(dirin)
    for file in files:
        if fnmatch.fnmatch(file,'m*.csv'):
            print(file)
            sdf = pd.read_csv(file)
            headers = list(sdf.head())
            # print(headers)
            # print(sdf)
            sdf.drop(sdf.columns[[0, 1]], axis = 1, inplace = True) 
            # print(sdf)
            # print(df)
            bdf = pd.read_csv(Bcsv)
            headers = list(bdf.head())
            # print(headers)
            newframe = bdf
            nan_value = float("NaN")
            newframe["elneg"] = nan_value
            #newframe = cartesian_product_simplified(bdf,sdf)
            newframe.to_csv('Bcsv.csv')
            exit()
#print("Yes, i'm doing something")
#readandplotaprdf()
#writer()


mergeBandS()

