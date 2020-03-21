program main
use neighlist_mod
implicit none
double precision, dimension(:), allocatable :: r1
double precision, dimension(:,:), allocatable :: rf
character(len=3), dimension(:), allocatable :: anames
character(len=100) :: fcif, atmp, atmp2, fpatt
integer :: i, nn, ngrid, na, ia, narg
double precision, dimension(:), allocatable :: grid_elneg, grid_pol, grid_rvdw
double precision :: rmin, rmax, vol, dh, bfac
double precision, dimension(6) :: b
type(t_atomic_properties) :: ap
logical :: repcell
double precision, dimension(:), allocatable :: elneg, pol, rvdw

rmin=2.d0
rmax=20.d0
ngrid=100
bfac=1
fcif=''
repcell = .false.
fpatt='out_grid.dat'



narg=iargc()
if (narg>=1) then
   do ia=1, narg
      call getarg(ia, atmp)
      if (trim(atmp)=='-i') then
         call getarg(ia+1, fcif)
      endif
      if (trim(atmp)=='-rmin') then
         call getarg(ia+1, atmp2)
         read(atmp2,*)rmin
      endif
      if (trim(atmp)=='-rmax') then
         call getarg(ia+1, atmp2)
         read(atmp2,*)rmax
      endif
      if (ANY((/'-ngrid', '-ng   '/)==trim(atmp))) then
         call getarg(ia+1, atmp2)
         read(atmp2,*)ngrid
      endif
      if (ANY(['-bfac']==trim(atmp))) then
         call getarg(ia+1, atmp2)
         read(atmp2,*)bfac
      endif
      if (ANY(['-repcell', '-rcell  ']==trim(atmp))) then
         call getarg(ia+1, atmp2)

         if (ANY(['f', 'F'] == trim(atmp2) )) then
            repcell = .false.
         else if (ANY(['t', 'T'] == trim(atmp2) )) then
            repcell = .true.
         else
            stop 'Wrong -repcell in namelist' // trim(atmp2)
         endif
      endif
      if (ANY(['-of   ', '-fpatt']==trim(atmp))) then
         call getarg(ia+1, atmp2)
         read(atmp2,*)fpatt
      endif
   enddo
endif

if (fcif=='') then
   print*,'ERROR! no input cif file was provided'
   stop
endif
!print*,' rmin= ',rmin, ' rmax= ', rmax,' ngrid= ', ngrid,' bfac= ', bfac

call read_atomic_properties('atomic_properties.dat', ap)

!call read_cif(trim(fcif), b(1:3), b(4:6), anames, rf)
call read_pdb(trim(fcif), b(1:3), b(4:6), anames, rf)
!print*,'box=', b

allocate(grid_elneg( ngrid ))
allocate(grid_pol( ngrid ))
allocate(grid_rvdw( ngrid ))


call assign_atomic_properties(ap, anames, elneg, pol, rvdw)


call get_rdf(elneg, b, anames, rf, bfac, repcell, rmin, rmax, ngrid, grid_elneg, vol)
call get_rdf(pol, b, anames, rf, bfac, repcell, rmin, rmax, ngrid, grid_pol, vol)
call get_rdf(rvdw, b, anames, rf, bfac, repcell, rmin, rmax, ngrid, grid_rvdw, vol)

dh = (rmax-rmin)/dble(ngrid-1)
open(20, file = trim(fpatt) )
write(20,'("#"a7,4(2x,a12))')"R","Electrpneg.", "polarizability", "vdWaals"
do i=1, ngrid
   write(20,'(f8.2,4(2x,f12.6))')rmin + (i-1)*dh, grid_elneg(i), grid_pol(i), grid_rvdw(i)
enddo
close(20)


end program main
