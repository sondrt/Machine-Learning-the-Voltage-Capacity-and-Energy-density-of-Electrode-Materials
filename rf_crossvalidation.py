#!/usr/bin/env python

# 2. Import libraries and modules
from os import path
import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt 
from sklearn.model_selection import train_test_split, cross_val_score, cross_validate
from sklearn import preprocessing
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, accuracy_score
import joblib 
import warnings
import scipy.stats as st


def main():
#Runs crossvalidation on what was produced in randomforest.py, and removes outliers. 
# The date here is not shuffeled, train_test_split already returns a random split. 
    warnings.simplefilter(action='ignore', category=FutureWarning)
     
    train_size = [0.95]
    n_estimators = 250
    
    infile = 'for_ML.csv'
    fnt = 24
    
    
    # print('working on file: %s'%(infile))
    data = pd.read_csv(infile, sep=',')
    HEADERS = list(data.head()) 
    y = data[HEADERS[-1]]
    X = data[HEADERS[2:-1]]
    ncv = 5                                # Number of crossvalidation blocks.
    l_cv = True
    
    if l_cv:
        clf = RandomForestRegressor(n_estimators=n_estimators, random_state=105)
        scores = cross_val_score(clf, X, y, cv=ncv) #only one CPU used
        print('CROSS_VALIDATION: Accuracy: %0.4f (+/- %0.4f)\n\n' % (scores.mean(), scores.std() * 2))
        print('scores=', scores)

        ss = sorted(scores)
        SUM = 0

        for i in range(len(scores)-2):
            # print('ss[i+1]',ss[i+1])
            SUM += ss[i+1]
        mean = SUM/(len(scores)-2.)
        print("mean: ",mean)
        print(ss)
        print("---------------------------------- ")

if __name__ == '__main__':
   main()

