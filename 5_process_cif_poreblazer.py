#/home/fanourg/Packages/poreblazer_v3.0.2_d/poreblazer.exe  ska.inp
#
#UFF_all.atoms
#ska.xyz
#defaults.dat
#6.656392 7.228301 14.915392
#90.000000 90.000000 90.000000

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
                # print(atom['name'])
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
   a = d['a']
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
   return d

def save_poreblazer_input(d, dirout, fpatt):
    from numpy import pi
    f = open(dirout + fpatt + '.xyz', "w+")
    l = d['conf']
    na = len(l)

    f.write("%i\n\n" %(na) )
    for ia in range(na):
        f.write(  "%s %f %f %f\n" %(l[ia]['name'],  l[ia]['x'], l[ia]['y'], l[ia]['z']  )  )
    f.close()
    f = open(dirout + fpatt + '.inp', "w+")
    f.write('%s\n'%(dirout + 'UFF_all.atoms'))
    f.write('%s\n'%(dirout + fpatt + '.xyz'))
    f.write('%s\n'%(dirout + 'defaults.dat'))
    f.write("%f %f %f\n%f %f %f\n"%( d['a'], d['b'], d['c'], d['alpha']*180/pi, d['beta']*180/pi, d['gamma']*180/pi))
    f.close()
    

def get_info_from_poreblazer(fn):
    helvol = []
    geomvol = []
    f = open(fn, "r")
    lines = f.readlines()
    for line in lines:
        if line.find("Helium volume in A^3:")>=0: 
            helvol = line.split()[-1]
            print(helvol)
        if line.find("Geometric (point accessible) volume in A^3:")>=0: 
            geomvol = line.split()[-1]
    f.close()
    exit()
    return helvol, geomvol



#def find_neihbors():
#def get_electronegativity():


dirin = './cif_for_poreblazer/cif_for_Li_PB/'
dirout = './cif_for_poreblazer/xyz_Li_files/'
porexe= '/Users/torp/Dropbox/MetalHydrides/poreblazer-master/src/poreblazer.exe'
helvol_geomvol_output = open('Li_helvol_geomvol_output.csv','w+')
helvol_geomvol_output.write('mid,helvol,geomvol\n')


files = os.listdir(dirin)
for file in files:
    if fnmatch.fnmatch(file, "m*.csv"):
        fpatt = file.replace(".csv","")
        y = read_cif( dirin + file )
        a = frac2cart(y)
        save_poreblazer_input(a, dirout, fpatt)
        logfile = fpatt + '.log'
        cmd = porexe +  '   ' + dirout + fpatt + '.inp > ' + dirout + fpatt + '.log'
        print(cmd)
        os.system( cmd )
        print("DONE=?")
        exit()
        helvol, geomvol = get_info_from_poreblazer(dirout + fpatt + '.log')
        print("This is fpatt:",fpatt, type(fpatt))
        print('helv: ', helvol)
        print('geov: ', geomvol)
        helvol_geomvol_output.write(fpatt.replace("_cif.dat","") + ","+ helvol + ","+ geomvol+ '\n')
        exit()


# Helium volume in A^3:           0.000
# Helium volume in cm^3/g:        0.000
#
# Geometric (point accessible) volume in A^3:          45.287




#y = read_cif( fn )
#print 'yy=', y['a'], y['b']
#a=frac2cart(y)
#save_poreblazer_input(y, 'ska')

#print y['conf']

