# 2. Import libraries and modules
from os import path
import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt 
from sklearn.model_selection import train_test_split, cross_val_score, cross_validate
from sklearn import preprocessing
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
import pprint
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.decomposition import PCA
import joblib
import warnings
import scipy.stats as st
from sklearn.preprocessing import StandardScaler

print("")
fnt=18
ncv = 5

warnings.simplefilter(action='ignore', category=FutureWarning)
 
train_size = [0.95]
n_estimators = 250

infile = 'for_ML.csv'
l_plot = False


# print ('working on file: %s'%(infile))
data = pd.read_csv(infile, sep=',')

HEADERS = list(data.head()) 
#print(HEADERS)
y = data[HEADERS[-1]]
X = data[HEADERS[1:-1]]
trsize=0.6
#trsize=10000
#nruns=30
#nshuffles=1
#ncv=10
sc = StandardScaler()

clf = RandomForestRegressor(n_estimators=n_estimators, random_state=105)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2,  train_size=trsize )#, stratify=X)


pca = PCA(0.99) #pca = PCA(n_components=compontent)

sc_train = sc.fit_transform(X_train)
sc_test = sc.transform(X_test)
print(sc_test)
print(sc_train)
# sc_y_train = sc.fit_transform(y_train)  #remove
# sc_y_test = sc.transform(t_test)        #remove
pca_sc_train = pca.fit_transform(sc_train)
pca_sc_test = pca.fit(sc_test)
print(pca_sc_train,"---------------------------------")
print(pca_sc_test)

PCA(copy=True, iterated_power ='auto', n_components=pca.n_components, random_state=None, svd_solver='auto', tol=0.0, whiten= False)
print('pca explained_variance_ratio_: ')
print(pca.explained_variance_ratio_)
print('singular_values_: ')
print(pca.singular_values_)
print('Components: ', pca.n_components_)

trained_model=clf.fit(sc_train, y_train)
pred = clf.predict(sc_test)
pred_train = clf.predict(sc_train)


r2score_test = r2_score(y_test, pred,  multioutput='variance_weighted')
r2score_train= r2_score(y_train, pred_train,  multioutput='variance_weighted')
print ('r2score = ', r2score_test)
print ('r2score_train = ', r2score_train)

MSE = mean_squared_error(y_test, pred)
RMSE = np.sqrt(MSE) 
print('MSE: ', MSE)
print('RMSE: ', RMSE)
# print("pred and pred_train: ", pred, pred_train)

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

N= 1248
# print(pca.components_)
# print(str(pca.components_.shape))
# plt.scatter(trained_model2[:,0],trained_model2[:,1],c=colors)
# plt.show()
   #213
colors = np.random.rand(N)

plt.scatter(pca_sc_train[:,0],pca_sc_train[:,1],c=colors)
plt.colorbar()
plt.show()


'''


pred = clf.predict(X_test)
pred_train = clf.predict(X_train)
#print 'mean(pred) = ', np.average(pred_all)
N_test = len(X_test)
N_train = len(X_train)

r2score_test = r2_score(y_test, pred,  multioutput='variance_weighted')
r2score_train= r2_score(y_train, pred_train,  multioutput='variance_weighted')
print ('r2score = ', r2score_test)
print ('r2score_train = ', r2score_train)

MSE = mean_squared_error(y_test, pred)
RMSE = np.sqrt(MSE) 
print('MSE: ', MSE)
print('RMSE: ', RMSE)

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
#   plt.show()
#   plt.savefig("Results/2019-06-11/mg_2AV-t=AV_p=msp_n.jpg", dpi=None, facecolor='w', edgecolor='w',
#        orientation='portrait', papertype=None, format=None,
#        transparent=False, bbox_inches=None, pad_inches=0.1,
#        frameon=None, metadata=None)


'''
exit()
