#returns Arrays; atom names, and box[6], position of all atoms[n x 3], 4: electronegativity

import os
import fnmatch

def read_cif(fn):
    print("Reading CIFs:")
    from numpy import pi
    f = open(fn, "r")
    lines = f.readlines()
    l_readatoms = False
    l = []
    for line in lines:
        if not l_readatoms:
            if line.find('_cell_length_a')>=0: 
                a = float(line.split()[1])
            if line.find('_cell_length_b')>=0: 
                b = float(line.split()[1])
            if line.find('_cell_length_c')>=0: 
                c = float(line.split()[1])
            if line.find('_cell_angle_alpha')>=0: 
                alpha = float(line.split()[1])*pi/180.
            if line.find('_cell_angle_beta')>=0: 
                beta = float(line.split()[1])*pi/180.
            if line.find('_cell_angle_gamma')>=0: 
                gamma = float(line.split()[1])*pi/180.
            if line.find('_atom_site_occupancy')>=0: 
                l_readatoms=True
        else:
            try:
                aname,tmp1,tmp2,fx,fy, fz,tmp3 = line.split()
                atom = {'name': aname, 'fx': float(fx), 'fy': float(fy), 'fz': float(fz), 'x':0., 'y':0., 'z':0}
                l.append(atom)
            except:
                pass
                #print('is it last line?? Good.', line)
    d = {'a':a, 'b':b, 'c':c, 'alpha':alpha, 'beta':beta, 'gamma': gamma, 'conf':l} 
    print('Done reading CIFS', fn)
    return d

def frac2cart(d):
   from numpy import sin, cos, sqrt, array, matmul
   cos_a = cos(d['alpha'])
   cos_b = cos(d['beta'])
   cos_c = cos(d['gamma'])
   sin_c = sin(d['gamma'])
   a  = d['a']
   b = d['b']
   c = d['c']
   tmp = c * sqrt(1.0 - cos_a**2 - cos_b**2 - cos_c**2 + 2.0*cos_a*cos_b*cos_c) / sin_c
   arr = [ [a, 0., 0.], [b*cos_c, b*sin_c, 0.], [c*cos_b, c*(cos_a - cos_c*cos_b) / sin_c, tmp] ]
   l = d['conf']
   lxyz =[]
   na = len(l)
   for ia in range(na):
       vec = [l[ia]['fx'], l[ia]['fy'], l[ia]['fz'] ]
       x, y, z = matmul(array(arr), array(vec))
       d['conf'][ia]['x'] = x
       d['conf'][ia]['y'] = y
       d['conf'][ia]['z'] = z
   return na

aa = read_cif('./cif_for_poreblazer/cif_files/mp-38816_cif.dat.csv')
print(aa['conf'])