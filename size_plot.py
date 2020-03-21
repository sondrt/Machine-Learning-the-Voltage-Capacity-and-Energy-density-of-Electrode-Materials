#size_plot.py


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
