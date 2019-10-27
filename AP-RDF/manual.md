# ap-rdf

## requirements
Originally, it was planned to provide as input **cif** structures. However, cif format is complicated and for that the `obabel` package should be used instead to transforn the cif file to a **pdb** file.

> `obabel  LiFePO4.cif   --fillUC  -OLiFePO4.pdb`

or

> `obabel -icif LiFePO4.cif   --fillUC -opdb -OLiFePO4.pdb`

## ap-rdf usage

`
./ap-rdf.x -i filename.pdb
`



On the output the code provides the distribution of electronegativity, polarizability and vdw volume. See the JPCC paper below for details.

<u>The following optional/required arguments can be provided:</u>

**-i**      string [required] filename of the pdb input file


**-rmax**   float [optional] default: 20

**-rmin**   float [optional] default: 2.d0

**-repcell** char: F/T [optional] default T. if T (true) then it replicates the unit cell so each one of its linear dimensions is larger that 2*rmax

**-bfac**   float [optional] default: 1.  It is the **B** exponent in  the exponential.

**-ngrid**   integer [optional] default: 100.

**-of** filename [optional] default: out_grid.dat 


### Example :

Convert first the cif file to pdb. Use:


> `obabel  MIL-47.cif   --fillUC  -OMIL-47.pdb`


After run the code and save the results in the mil-47.aprdf.

  
> `./ap-rdf.x -i MIL-47.pdb -bfac 1.0 -rmin 3.0 -rmax 50.0 -ngrid 50 -of mil-47.aprdf`


## to be clarified
* I am not sure that the code works correctly. I **can not** reproduce exactly the results for the *IRMOF-1* and *MIL-47* which can be found in <u>dx.doi.org/10.1021/jp404287t | J. Phys. Chem. C 2013, 117, 14095−14105</u>.

* I dont know if **repcell** should be True or False. In my opinion should be True, but I see that the results are closer to the published ones, if repcell is False.
