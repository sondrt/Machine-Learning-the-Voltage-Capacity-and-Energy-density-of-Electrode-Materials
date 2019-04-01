#plottetiplot.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



csv = 'allFiles.csv'
data = pd.read_csv(csv, sep=',')
headers = list(data.head())
n = len(data[headers[0]])
x = np.linspace(0,n-1,n)



for ih, header in enumerate(headers):
	if ih>12:
		d = data[header]
		print(header)
		try:
			plt.title(header)
			plt.plot(x,d)
			plt.show()
		except:
			print('failed: ' + header)
	# if ih == 12:
	# 	exit()



