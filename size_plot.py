#size_plot.py


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

'''
color = 'red'
titles = ['Mg Batteries','Li Batteries']

targets =[ 'elnegdis_r2.0','elnegdis_r2.25','elnegdis_r2.5','elnegdis_r2.75',
    'elnegdis_r3.0','elnegdis_r3.25','elnegdis_r3.5','elnegdis_r3.75',
    'elnegdis_r4.0']
abbr = ['AV','GC','VC','SE','ED']
files = ['newapproch_aprdf.csv','Li_allFiles.csv',	'aprdf2.csv']
csv = files[2]
df = pd.read_csv(csv, sep=',', low_memory=False)    
header = df.head()
for i in range(6):
	sns.distplot(df[targets[i]], hist=True, kde=False, bins=10, color = color, hist_kws={'edgecolor':'black'})
	plt.title(titles[1], fontsize=18)
	plt.xlabel(targets[i], fontsize=14)
	plt.ylabel('number of appearances', fontsize=14)
	figname = 'Results/figures/columnsplotMg2_' + targets[i].replace(' ','_') +  '.pdf'
	plt.savefig(figname,format = 'pdf',dpi = 100,bbox_inches='tight')
	plt.show()
	plt.close()

color = 'blue'
titles = ['Mg Batteries','Li Batteries']

targets =['Average_Voltage', 'Capacity_Grav', 'Capacity_Vol', 'Specific_E_Wh/kg', 'E Density Wh/l']
abbr = ['AV','GC','VC','SE','ED']
files = ['newapproch_aprdf.csv','Li_allFiles.csv']
csv = files[0]
df = pd.read_csv(csv, sep=',', low_memory=False)    
header = df.head()
for i in range(5):
	sns.distplot(df[targets[i]], hist=True, kde=False, bins=10, color = color, hist_kws={'edgecolor':'black'})
	plt.title(titles[0], fontsize=18)
	plt.xlabel(abbr[i], fontsize=14)
	plt.ylabel('number of appearances', fontsize=14)
	figname = 'Results/figures/columnsplotMg_' + abbr[i] +  '.pdf'
	plt.savefig(figname,format = 'pdf',dpi = 100,bbox_inches='tight')
	# plt.show()
	plt.close()
'''



#Li diff pred

'''
x_predictors = ['msp','msp+stab'			,'co+vnd'		,'co+vf'		,'co+AV'			, 'co+GCVC'		,'co+SEED']
AV 	= [0.5807576174506466	,0.6382352521590721		,0.6889475417554051	,0.7434585478459865,0					, 0.7241229224122133, 0.7390134629839741	]	
GC 	= [0.42486507985539385	,0.40973673978825065 	,0.6287597245517911	,0.6392378928534125,0.6057972768715484	, 0 	 			, 0.8606302267077546	]
VC 	= [0.46523200049569025	,0.47261421608939863	,0.7127950029643826	,0.6889267179947649, 0.7126270639446217	, 0 				, 0.8753624146262561]
SE 	= [0.444673400127916	,0.4334842121982636 	,0.6329753454633711	,0.6437486035928914, 0.6900349150430399	, 0.8458952696501991, 0	 ]
ED 	= [0.43023021580021564	,0.45534173933954647	,0.6466194152371839	,0.6579819998670257, 0.721783961574168	, 0.8870882181162133, 0	]
fig,ax=plt.subplots()
ax.set_title('Combination of predictors and targets')
# ax.label()
# ax.errorbar(x,y,e1, color = 'red',marker = 'o')
ax.plot(x_predictors,AV,'o',label='AV',marker = '*')
ax.plot(x_predictors,GC,'o',label='GC',marker = 'o')
ax.plot(x_predictors,VC,'o',label = 'VC',marker = 'p')
ax.plot(x_predictors,SE,'o',label = 'SE',marker = 'P')
ax.plot(x_predictors,ED,'o',label = 'ED',marker = 'v' )
ax.set_ylim(0.1,1)
ax.legend()
legend = ax.legend(loc='lower right',shadow=True, fontsize='medium')


legend.get_frame()
fig.tight_layout()

plt.grid(False)
plt.show()
fig.savefig('Results/figures/comboofpred.pdf',format = 'pdf',dpi = 100,bbox_inches='tight')
plt.close()





'''
'''
#Mg

x_predictors = ['msp','vnd_chg','vnd_dis','vnd','vf','APRDF1','APRDF2','combo']
AV 	= [0.60989, 0.58126,0.5885,0.6261,0.0621,0.0309,0.2336,0.7072 ]
GC 	= [0.47107, 0.2464,0.6190,0.6622,0.3490,0.11039,0.3956,0.6805 ]
VC 	= [0.4985, 0.3964,0.64017,0.6758,0.3943,0.13321,0.4438,0.7206 ]
SE 	= [0.56822,0.5280,0.6115,0.64942,0.09092,0.04783,0.3611,0.7163 ]
ED 	= [0.5247,0.5174,0.5980,0.6532,0.18253,0.05931,0.32963,0.62737 ]
fig,ax=plt.subplots()
# ax.set_title('Unique predictors')
# ax.label()
# ax.errorbar(x,y,e1, color = 'red',marker = 'o')
ax.plot(x_predictors,AV,'o',label='AV',marker = '*')
ax.plot(x_predictors,GC,'o',label='GC',marker = 'o')
ax.plot(x_predictors,VC,'o',label = 'VC',marker = 'p')
ax.plot(x_predictors,SE,'o',label = 'SE',marker = 'P')
ax.plot(x_predictors,ED,'o',label = 'ED',marker = 'v' )
ax.legend()
ax.set_ylabel('R2',fontsize=14)
ax.set_xlabel('descriptor type',fontsize=14)
legend = ax.legend(loc='lower left',shadow=True, fontsize='medium')

legend.get_frame()
fig.tight_layout()

plt.grid(False)
plt.show()
fig.savefig('Results/figures/Mg_pred_on_targ.pdf',format = 'pdf',dpi = 100,bbox_inches='tight')
plt.close()

#Li

x_predictors = ['msp','vnd_chg','vnd_dis','vnd','vf','APRDF2','combo']
AV 	= [0.5692, 0.5437,0.5319,0.5608,-0.06318,0.3075,0.6979 ]
GC 	= [0.4456, 0.3692,0.3983,0.6191,0.05186,0.3379,0.6444 ]
VC 	= [0.4985, 0.4352,0.4724,0.7186,0.159419,0.4474,0.71029 ]
SE 	= [0.4572, 0.4324,0.4367,0.5619,-0.02663,0.3502,0.6713 ]
ED 	= [0.4815, 0.4690,0.44020,0.6506,0.02518,0.3771,0.6590 ]
fig,ax=plt.subplots()
# ax.set_title('Unique predictors')
# ax.label()
# ax.errorbar(x,y,e1, color = 'red',marker = 'o')
ax.plot(x_predictors,AV,'o',label='AV',marker = '*')
ax.plot(x_predictors,GC,'o',label='GC',marker = 'o')
ax.plot(x_predictors,VC,'o',label = 'VC',marker = 'p')
ax.plot(x_predictors,SE,'o',label = 'SE',marker = 'P')
ax.plot(x_predictors,ED,'o',label = 'ED',marker = 'v' )
ax.legend()
ax.set_ylabel('R2',fontsize=14)
ax.set_xlabel('descriptor type',fontsize=14)
legend = ax.legend(loc='lower left', shadow=True, fontsize='medium')

legend.get_frame()
fig.tight_layout()

plt.grid(False)
plt.show()
fig.savefig('Results/figures/Li_pred_on_targ.pdf',format = 'pdf',dpi = 100,bbox_inches='tight')
plt.close()









'''




"""

x = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
y = [-2.4017124235613707,0.24395045820551758,0.47312341792468127,0.519129391443488,0.5562331686270996,0.60683981223302, 0.6062650739783519,0.614548061354786,0.6470347887381357,0.6788296072575222]
e1 = [2.6416359077132228,0.18050826667655195,0.07522837739521984,0.06159779950763397,0.053596819780455836,0.038445933586554654,0.040814106969404434,0.042844826445907876,0.029624401692294293,0.03147230893335434]

WAPE = [9.474428452475259,8.392210166416898,7.774503406813733,7.838463282273608,7.115551450344077,6.971231989201465,6.771154144402216,6.598847945839905,6.422102740194812,6.0182357636749915]
e2 = [1.9005951379691124,1.0631234437259036,0.7238360623500024,0.5089597322746124,0.5163669813657787,0.505464943378038,0.408460813030898,0.2957348830628311,0.34049798085885963,0.38168205182888915]

fig,ax=plt.subplots()
ax.set_title('Impact of size of database')
ax.errorbar(x,y,e1, color = 'red',marker = 'o')
ax.set_xlabel('% of datbase')
ax.set_ylabel('R2-CVM in %',color='red',fontsize=14)
ax2 = ax.twinx()
ax2.errorbar(x,WAPE,e2,color = 'blue', marker = 'o')
ax2.set_ylabel('WAPE', color='blue',fontsize=14)
ax.set_ylim(0,0.8)
ax.xaxis.set_ticks([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1])
#ax.yaxis.set_ticks([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1])

plt.show()
plt.close()
fig.savefig('Results/figures/size_db.png',format = 'png',dpi = 100,bbox_inches='tight')


"""
################################
'''

x3= [5, 10,25,50,100,250,500,1000]#,2500,5000,10000]
y3 = [0.5823187448011309,0.6284652548313369,0.6489979643980438,0.6688006143786319,
0.6594052261866936,0.6663979907908542,0.6763980018524506,0.6603824476336491]
e3 = [0.044469306663591925,0.03179277308049951,0.037081030325577725,0.04493112876319265,
0.028203819837094676,0.026016038520950375, 0.017682715041168202,0.024492585008256237]

WAPE = []
e4 = []
fig,ax=plt.subplots()
ax.set_title('Impact of Number of estimators')
ax.errorbar(x3,y3,e3 color = 'red',marker = 'o')
ax.set_xlabel('# of estimators')
ax.set_ylabel('R2-CVM in %',color='red',fontsize=14)
ax2 = ax.twinx()
ax2.errorbar(x3,WAPE2,color = 'blue', marker = 'o')
ax2.set_ylabel('WAPE', color='blue',fontsize=14)
start, end = ax.get_xlim()
ax.xaxis.set_ticks(np.arange(0, 1001, 100))
plt.show()
plt.close()
fig.savefig('Results/figures/n_estimators.jpeg',format = 'jpeg',dpi = 100,bbox_inches='tight')
'''
