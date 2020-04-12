# 2. Import libraries and modules
from os import path
import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt 
from sklearn.model_selection import train_test_split, cross_val_score, cross_validate
from sklearn import preprocessing
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.externals import joblib 
import warnings
import scipy.stats as st



warnings.simplefilter(action='ignore', category=FutureWarning)
 
train_size = [0.95]
n_estimators = 250

infile = 'for_ML.csv'
l_plot = True
fnt = 24


print 'working on file: %s'%(infile)
data = pd.read_csv(infile, sep=',')
HEADERS = list(data.head()) 
y = data[HEADERS[-1]]
X = data[HEADERS[2:-1]]
trsize=200
#trsize=10000
#nruns=30
#nshuffles=1
#ncv=10

clf = RandomForestRegressor(n_estimators=n_estimators, random_state=105)
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=trsize )#, stratify=X)
trained_model=clf.fit(X_train, y_train)
print 'train=', X_train
   # 9. Evaluate model pipeline on test data
pred = clf.predict(X_test)
pred_train = clf.predict(X_train)
#print 'mean(pred) = ', np.average(pred_all)
N_test = len(X_test)
r2score_test = r2_score(y_test, pred,  multioutput='variance_weighted')
r2score_train= r2_score(y_train, pred_train,  multioutput='variance_weighted')
print 'r2score = ', r2score_test
print 'r2score_train = ', r2score_train
N_train = np.size(y_train)
N_test = np.size(y_test)

if l_plot:
   maxp =  1.2*max(max(y_test), max(y_train))
   dx = maxp*0.05

   plt.rcParams["figure.figsize"]=(8,8)

   plt.title(infile)
   plt.xlim (0, maxp)
   plt.ylim (0, maxp)
   plt.plot(y_test, pred,'ro', c='red', alpha=0.5)
   plt.plot(y_train, pred_train,'ro', c='green', alpha=0.5)
   plt.plot([0.,maxp],[0.,maxp])
      #.... text
   plt.text(0.05*maxp, 0.95*maxp, 'N=%i'%(N_train), color='green', fontsize=fnt)
   plt.text(0.05*maxp, 0.95*maxp-dx, 'r2=%.3f'%(r2score_train), color='green', fontsize=fnt)
#      plt.text(0.05*maxp, 0.95*maxp-2.*dx, 'RMSE=%.3f'%(rmse_train), color='green', fontsize=fnt)
#      plt.text(0.05*maxp, 0.95*maxp-3.*dx, 'MAE=%.3f'%(mae_train), color='green', fontsize=fnt)
#      #plt.text(0.05*maxp, 0.95*maxp-7.*dx, 'CROSSVAL[%i]=%f'%(ncv,cross_val), color='black')
#
   plt.text(0.65*maxp, 0.40*maxp, 'N=%i'%(N_test), color='red', fontsize=fnt)
   plt.text(0.65*maxp, 0.40*maxp-dx, 'r2=%.3f'%(r2score_test), color='red', fontsize=fnt)
#      plt.text(0.65*maxp, 0.40*maxp-2.*dx, 'RMSE=%.3f'%(rmse_test), color='red', fontsize=fnt)
#      plt.text(0.65*maxp, 0.40*maxp-3.*dx, 'MAE=%.3f'%(mae_test), color='red', fontsize=fnt)
   plt.show()

exit()
