import numpy as np
import my_lib as ml


nat=4													#number of atoms
#c=0.0
b = [5.0, 5.0, 3.01, 90.0, 90.0, 90.0]					#box dimentions
acoords = np.zeros([3,nat], order='F')					#3xn matrix
acoords[:,:] = np.random.rand(3,nat)
r1 = acoords.ravel()    								# makes coords an 1-d array
anames= np.empty((3,nat), dtype='c')					#atom names
anames = ['H  ', 'O  ', 'Ca ', 'KKK']
print 'names=', anames
print ml.get_rdf.__doc__
c, grid=ml.get_rdf(b, anames, r1, 2., 13., 6, nn=nat)	#grid = desired rdf
print 'c=', c
