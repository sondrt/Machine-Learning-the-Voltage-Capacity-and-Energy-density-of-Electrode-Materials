EXE=ap-rdf.x
EXEDIR=./

$(shell makedepf90 ${DEFS} -o ${EXEDIR}${EXE} *.f90  > Makefile_deps)
include Makefile_deps

all: ${EXE}
	$(FOBJ): Makefile

#
# ---- Uncomment the following for Intel ifort compiler
#
#FC=gfortran
#FFLAGS=
FC=ifort
FFLAGS=-fpp
FFLAGS=-C -debug -traceback -fpp #-openmp #-warn unused
FFLAGS=-C -check all -debug -traceback -fpp -warn  notruncated_source -warn unused
#FFLAGS=-O2 -ftz -fpp #-openmp
LDFLAGS=${FFLAGS}
#
# ---- Uncomment the following for gfortran compiler
#
FC=gfortran
FFLAGS=-fpp
FFLAGS=-C -cpp #-openmp
#FFLAGS=-O2 -cpp #-openmp
LDFLAGS=${FFLAGS}

DEFS=
INC=
LIBS=

deps:
	        makedepf90 ${DEFS} -o ${EXE} *.f90 > Makefile_deps

%.o:%.f90
	        $(FC) $(FFLAGS) $(DEFS) $(INC) -c $< -o $@

clean: 
	        rm -rf $(FOBJ) *.o *.mod Makefile_deps ${EXE}
