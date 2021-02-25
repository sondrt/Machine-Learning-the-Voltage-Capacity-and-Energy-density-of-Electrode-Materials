from mendeleev import element

print "#symbol, electronegativity, polarizability, vdw_radius"
for iel in xrange(117):
    el = element(iel+1)
    elecneg=el.en_pauling
    polar=el.dipole_polarizability
    vdw_radius=el.vdw_radius
    if elecneg==None: elecneg=-1
    if polar==None: polar=-1
    if vdw_radius==None: vdw_radius=-1
    print el.symbol, elecneg, polar, vdw_radius
