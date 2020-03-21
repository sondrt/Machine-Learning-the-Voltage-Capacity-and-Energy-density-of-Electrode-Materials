#run_aprdf.py
import os
import fnmatch

dirin = './../cif_info_dir/cif_for_aprdf/'
dir_aprdf = './../cif_info_dir/pdb_for_aprdf/'

files = os.listdir(dir_aprdf)
i = 0
for file in files:
	if fnmatch.fnmatch(file, 'm*.pdb'):
		print(file)
		cmd = './ap-rdf.x -i ' + file + ' -bfac 1.0 -rmin 3.0 -rmax 10.0 -ngrid 50 -repcell T -of ' + file.replace('.pdb','') + '.aprdf'
		print(cmd)
		os.system(cmd)
