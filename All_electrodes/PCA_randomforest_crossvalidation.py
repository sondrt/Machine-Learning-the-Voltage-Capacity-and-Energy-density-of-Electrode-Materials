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
from sklearn.preprocessing import MinMaxScaler

from sklearn.metrics import average_precision_score
#Scaling, PCA, Randomforest and crossvalidation.

def plot_number_of_pcs_removed():
    plt.plot(np.cumsum(pca.explained_variance_ratio_))
    plt.xlabel('number of components')
    plt.ylabel('cumulative explained variance');
    # plt.grid(True)
    plt.plot([82,82],[0,1.5], c='red',ls='--')
    plt.plot([-5,130],[1,1], c='red',ls='--')
    plt.show()
    plt.close()
    exit()
    return



print("")
fnt=18
ncv = 50
multi_run = []
WAPE = []
lists = {key:[] for key in ['xlist','ylist','wlist','error1','error2']  }
l1 = [30]#[10,25,50,100,250,500,1000]
l2 = [0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
l2plot = False
l_plot   = False
scatter_pca_plot = False
plot_number_of_pcs_rem = True

warnings.simplefilter(action='ignore', category=FutureWarning)
for j in l1:

    total    = 1     #j% of totalt db 
    train_size = [0.95]
    n_estimators = 10   #j   Number of estimators
    print(n_estimators)
    infile   = 'for_ML.csv'

    for i in range(1):
        # print ('working on file: %s'%(infile))
        data     = pd.read_csv(infile, sep=',')

        HEADERS  = list(data.head()) 
        #print(HEADERS)
        y        = data[HEADERS[-1]]
        X        = data[HEADERS[1:-1]]
        trsize   = 0.9 * total
        tesize   = 0.1 * total
        print(trsize, tesize)
        # exit()
        #trsize=10000
        #nruns=30
        #nshuffles=1
        #ncv=10
        emptyframe = pd.DataFrame()

        sc = StandardScaler()
        regr = RandomForestRegressor(n_estimators=n_estimators, random_state=105)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = tesize,  train_size=trsize )#, stratify=X)

        # print(X['energy'])
        pca = PCA(0.99)#0.99) #pca = PCA(n_components=compontent)
        # pca =  PCA(copy=True, iterated_power ='auto', n_components=pca.n_components, random_state=None, svd_solver='auto', tol=0.0, whiten= False)
        # pca.fit(X)
        sc_X_train = sc.fit_transform(X_train)
        pca_sc_X_train = pca.fit_transform(sc_X_train)
        print("original shape:   ", X_train.shape)
        print("transformed shape:", pca_sc_X_train.shape)

        N = len(pca_sc_X_train) #213 #1657
        print(N)
        # N_test = len(X_test)
        # N_train = len(X_train)
        colors = np.random.rand(N)
        # print(X_train)
        # print(sc_X_train)
        # print(pca_sc_X_train)
        if plot_number_of_pcs_rem:
            plot_number_of_pcs_removed()

        if scatter_pca_plot:

            plt.scatter(sc_X_train[:,0], sc_X_train[:,1], c =colors,edgecolor='none',alpha=0.5,cmap=plt.cm.get_cmap('rainbow',10))# c = colors)
            plt.xlabel('component 1')
            plt.ylabel('component 2')
            plt.colorbar();
            plt.show()
            plt.close()

            plt.scatter(pca_sc_X_train[:,0], pca_sc_X_train[:,1], c =colors,edgecolor='none',alpha=0.5,cmap=plt.cm.get_cmap('rainbow',10))# c = colors)
            plt.xlabel('component 1')
            plt.ylabel('component 2')
            plt.colorbar();
            plt.show()
            plt.close()



    print('Components: ', pca.n_components_)
    regr.fit(X_train,y_train)
    # trained_model=regr.fit(pca_sc_X_train, y_train)
    pred = regr.predict(X_test)
    pred_train = regr.predict(X_train)
    N = 1657 #213 #1657
    N_test = len(X_test)
    N_train = len(X_train)

    colors = np.random.rand(N)
    # pca = PCA().fit(sc_train)
    # pca = PCA().fit(digits.data)

    # plt.title('pca.fit_transform on X_train')
    # plt.scatter(sc_train[:,0], sc_train[:,1],c=colors,edgecolor='none',alpha=0.5,cmap=plt.cm.get_cmap('rainbow',10))# c = colors)

    # print(type(pred))
    # print(pred_train)
    r2score_test = r2_score(y_test, pred,  multioutput='variance_weighted')
    r2score_train= r2_score(y_train, pred_train,  multioutput='variance_weighted')
    print ('r2score = ', r2score_test)
    print ('r2score_train = ', r2score_train)

    Mean_test = np.mean(y_train)
    MSE_test = mean_squared_error(y_test, pred)
    MAE_test = mean_absolute_error(y_test, pred)
    RMSE_test = np.sqrt(MSE_test) 
    WAPE_test = MAE_test/Mean_test * 100

    Mean_train = np.mean(y_test)
    MSE_train = mean_squared_error(y_train, pred_train)
    MAE_train = mean_absolute_error(y_train, pred_train)
    RMSE_train = np.sqrt(MSE_train) 
    WAPE_train = MAE_train/Mean_train * 100
    stdev_train = np.std(y_train-pred_train)

    print("MAE_train:", MAE_train)


    scores = cross_val_score(regr, X_train, y_train, cv=ncv) #only one CPU used
    # print('CROSS_VALIDATION: Accuracy: %0.4f (+/- %0.4f)\n\n' % (scores.mean(), scores.std() * 2))
    # print('scores=', scores)

    ss = sorted(scores)
    SUM = 0

    for i in range(len(scores)-2):
     # print('ss[i+1]',ss[i+1])
     SUM += ss[i+1]
    mean = SUM/(len(scores)-2.)
    # print("mean: ",mean)
    # print(ss)
    # print("---------------------------------- ")







if l_plot:

    # plt.title('pca.fit_transform on X_train')
    # plt.scatter(sc_train[:,0], sc_train[:,1], c = colors)
    # # plt.show()
    # plt.close()

    # plt.title('pca.fit_transform on a standardscaled X_train')
    # plt.scatter(pca_sc_train[:,0],pca_sc_train[:,1],c=colors)
    # plt.colorbar()
    # # plt.show()
    # plt.close() 

    maxp =  1.2*max(max(y_test), max(y_train))
    dx = maxp*0.05

    plt.rcParams["figure.figsize"]=(8,8)

    plt.title(infile)
    plt.xlabel('Exact method')
    plt.ylabel('Machine Learning method')

    plt.xlim (0, maxp)
    plt.ylim (0, maxp)
    plt.plot(y_test, pred,'ro', c='red', alpha=0.5)
    plt.plot(y_train, pred_train,'ro', c='green', alpha=0.5)
    plt.plot([0.,maxp],[0.,maxp])
    #.... text
    plt.text(0.05*maxp, 0.95*maxp, 'N=%i'%(N_train), color='green', fontsize=fnt)
    plt.text(0.05*maxp, 0.95*maxp-dx, 'r2=%.3f'%(r2score_train), color='green', fontsize=fnt)
    plt.text(0.05*maxp, 0.95*maxp-2.*dx, 'RMSE=%.3f'%(RMSE_train), color='green', fontsize=fnt)
    plt.text(0.05*maxp, 0.95*maxp-3.*dx, 'MAE=%.3f'%(MAE_train), color='green', fontsize=fnt)
    plt.text(0.05*maxp, 0.95*maxp-4.*dx, 'WAPE=%.3f'%(WAPE_train), color='green', fontsize=fnt)
    # plt.text(0.05*maxp, 0.95*maxp-7.*dx, 'CROSSVAL[%i]=%f'%(ncv,cross_val), color='black')

    plt.text(0.65*maxp, 0.40*maxp, 'N=%i'%(N_test), color='red', fontsize=fnt)
    plt.text(0.65*maxp, 0.40*maxp-dx, 'r2=%.3f'%(r2score_test), color='red', fontsize=fnt)
    plt.text(0.65*maxp, 0.40*maxp-2.*dx, 'RMSE=%.3f'%(RMSE_test), color='red', fontsize=fnt)
    plt.text(0.65*maxp, 0.40*maxp-3.*dx, 'MAE=%.3f'%(MAE_test), color='red', fontsize=fnt)
    plt.text(0.65*maxp, 0.40*maxp-4.*dx, 'WAPE=%.3f'%(WAPE_test), color='red', fontsize=fnt)

    # plt.show()
    plt.savefig("Results/figures/AV_msp+vnd.pdf", format='pdf', dpi=None, facecolor='w', edgecolor='w',
     orientation='portrait', papertype=None,
     transparent=False, bbox_inches=None, pad_inches=0.1,
     metadata=None)

    multi_run.append(mean)
    WAPE.append(WAPE_test)
   
    print("---------------------------------- ")
    print('\n', 'END DATA','\n')  
    print(multi_run)
    print('multirun: ',np.mean(multi_run),np.std(multi_run))
    print(WAPE)
    print('WAPE: ',np.mean(WAPE),np.std(WAPE))


#   lists['xlist']    = np.mean(multi_run)
    lists['ylist'].append(np.mean(multi_run))
    lists['error1'].append(np.std(multi_run))
    lists['wlist'].append(np.mean(WAPE))
    lists['error2'].append(np.std(WAPE))
if l2plot:
    # ax.set_title('Impact of size of database')
    # print(l1,lists['ylist'], lists['error1'])

    fig,ax=plt.subplots()
    ax.errorbar(l1,lists['ylist'], lists['error1'], color = 'red',marker = 'o')
    ax.set_xlabel('# of estimators')
    ax.set_ylabel('R2-CVM',color='red',fontsize=14)
    # ax.set_ylim(0.5,0.8)
    ax2 = ax.twinx()
    ax2.errorbar(l1,lists['wlist'], lists['error2'], color = 'blue', marker = 'o')
    ax2.set_ylabel('WAPE', color='blue',fontsize=14)
    # ax.set_ylim(0,0.8)
    ax.set_xlim(0,1001)
    # ax.xaxis.set_ticks(np.arange(0, 1001, 100))
    # ax.xaxis.set_ticks([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1])
    plt.show()
    fig.savefig('Results/AV_msp+vnd.pdf',format = 'pdf',dpi = 100,bbox_inches='tight')
    plt.close('all')
exit()