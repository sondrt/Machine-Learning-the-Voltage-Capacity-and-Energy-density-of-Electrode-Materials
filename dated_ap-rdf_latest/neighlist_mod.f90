module neighlist_mod

implicit none
type t_atomic_properties
   character(len=3), dimension(116) :: symbol
   double precision, dimension(116) :: elneg, pol, rvdw
end type t_atomic_properties


Contains
!    subroutine read_atomic_properties( finp, ap)
!    subroutine assign_atomic_properties(ap, anames, elneg, pol, rvdw)
!    subroutine get_rdf(aprop, b, anames, r1, bfac, rmin, rmax, ngrid, grid, vol)
!    subroutine init_cell( boxl, boxa, rprimd, gprimd )
!    subroutine get_numberofreplicas(rprimd, rc, nxyz)
!    subroutine calcRij(rprimd, rij, drsq)
!    subroutine frac2cart(rprimd, r1, r2)
!    subroutine cart2frac(gprimd, r1, r2)
!    subroutine matr3inv(aa,ait)
!    subroutine outprod3(a1,a2,a3)
!    subroutine write_xyz(finp, boxl, boxa, an, R)
!    subroutine read_cif(fn, boxl, boxa, anames, Rf)
!    subroutine read_pdb(fn, boxl, boxa, anames, Rf)

   subroutine read_atomic_properties( finp, ap)
   implicit none
   character(len=*) :: finp
   type(t_atomic_properties) :: ap
   !... local vars
   integer :: i, iloc, iostat
   double precision :: norm_elneg, norm_pol, norm_rvdw

   open(10, file=trim(finp))
   read(10,*)  ! comment line
   do i=1, size(ap% symbol)
       read(10, *, iostat=iostat)ap% symbol(i), ap% elneg(i), ap% pol(i), ap% rvdw(i)
       if (iostat/=0) exit
   enddo
   close(10)

   !.... normalize with respect that of "C"
   do i=1, size(ap% symbol)
      if (trim(ap% symbol(i)) == "C") then
         iloc = i
         exit
      endif
   enddo
   norm_elneg = ap% elneg(iloc)
   norm_pol = ap% pol(iloc)
   norm_rvdw = ap% rvdw(iloc)
   do i=1, size(ap% symbol)
      ap% elneg(i) = ap% elneg(i) / norm_elneg
      ap% pol(i)   = ap% pol(i)   / norm_pol
      ap% rvdw(i)  = ap% rvdw(i)  / norm_rvdw
!      write(*,'(a5,3(3x, f8.4))')trim(ap% symbol(i)), ap% elneg(i), ap% pol(i), ap% rvdw(i) 
   enddo
   end subroutine read_atomic_properties
   !
   !
   !
   subroutine assign_atomic_properties(ap, anames, elneg, pol, rvdw)
   implicit none
   type(t_atomic_properties) :: ap
   character(len=*), dimension(:) :: anames
   double precision, dimension(:), allocatable :: elneg, pol, rvdw
   !...
   integer :: ia, j, na
   logical :: found
   character(len=3) :: symi

   na=size(anames)
   if (allocated(elneg)) deallocate(elneg); allocate(elneg(na))
   if (allocated(pol)) deallocate(pol); allocate(pol(na))
   if (allocated(rvdw)) deallocate(rvdw); allocate(rvdw(na))

   do ia=1, na
      symi=trim(anames(ia))
      found = .false.
      do j=1, size(ap% symbol)
!         print*,'symbol=', trim(ap% symbol(j))
         if (trim(to_lower(symi)) == trim(to_lower(ap% symbol(j)))) then
            elneg(ia) = ap% elneg(j)
            pol(ia) = ap% pol(j)
            rvdw(ia) = ap% rvdw(j)

            found=.true.
            exit
         endif
      enddo

      if (.not. found) then
         print*,'Atomic properties for were not found from atom: ', trim(symi)
         stop
      endif
   enddo

   write(22,*)"============"
   do ia=1, na
      write(22,'(a10,3(2xf12.6))')trim(anames(ia)), elneg(ia), pol(ia), rvdw(ia)
   enddo
   close(22)

   end subroutine assign_atomic_properties
   !
   !
   !
   subroutine get_rdf(aprop, b, anames, r1, bfac, repcell, rmin, rmax, ngrid, grid, vol)
   ! assume that r1 are in fractional coordinates
   implicit none
   double precision, dimension(6), intent( in     ) :: b
   double precision, dimension(:), intent( in    ) :: aprop
   character*3, dimension(:), intent( in     ) :: anames
   double precision, dimension(:,:), intent( in    ) :: r1
   logical, intent( in    ) :: repcell
   double precision, intent( in     ) :: bfac, rmin, rmax
   integer, intent(in) :: ngrid
   double precision, dimension(ngrid), intent(   out ) :: grid
   double precision, intent(   out ) :: vol
   !...
   double precision, dimension(:,:), allocatable :: Rf, Rc, Rc1
   double precision, dimension(3) :: boxl, boxa
   double precision, dimension(3, 3) :: rprimd, gprimd
   integer, dimension(3) :: nxyz
   double precision :: dr, drsq, rmaxsq, dh, sumg, api, apij, rgrid
   double precision, dimension(3) :: ri, rij
   integer :: i, j, ix, iy, iz, ia, ja, na0, na, nscale, nx, ny, nz, idx, ns
   double precision, dimension(:), allocatable :: ap
   character*3, dimension(:), allocatable :: an


   na0 = size(anames)

   boxl(1:3) = b(1:3)
   boxa(1:3) = b(4:6)!   *3.14159265d0/180.d0
   call init_cell(boxl, boxa, rprimd, gprimd)
   if (repcell) then
      call get_numberofreplicas(rprimd, rmax, nxyz)
      print*,'number of replicas : ', nxyz
   else
      nxyz=1
   endif
   !
   !
   !   replicate unit cell so that the three box linear dimensions are larger than 2*Rmax
   !
   ! 
   allocate(Rc1(3, na0))
   do ia=1, na0
      call frac2cart(rprimd, R1(1:3, ia), Rc1(1:3,ia))
   enddo
   call  write_xyz('fff0.xyz', boxl, boxa, anames, Rc1)
   deallocate(Rc1)

   nscale = product( nxyz )
   na = nscale*na0
   boxl=boxl*nxyz
   allocate( an(na) )
   allocate( ap(na) )
   allocate( Rf(3, na))
   nx=nxyz(1)
   ny=nxyz(2)
   nz=nxyz(3)
   do ia=1, na0
      Rf(1:3, ia) = r1(1:3, ia) / [nx, ny, nz]
   enddo
   call init_cell(boxl, boxa, rprimd, gprimd)
   vol = getvolume(rprimd)
   ja=0
   do iz=1, nxyz(3)
      do iy=1, nxyz(2)
         do ix=1, nxyz(1)
            do ia=1, na0
               ja = ja+1
               Rf(1:3, ja) = Rf(1:3, ia) + [dble(ix-1)/nx, dble(iy-1)/ny, dble(iz-1)/nz]
               an(ja) = anames(ia)
               ap(ja) = aprop(ia)
            enddo   ! do ia=1, na0
         enddo
      enddo
   enddo
   !
   !   save the (replicated) configuration in xyz format
   !
   allocate(Rc(3, na))
   do ia=1, na
      call frac2cart(rprimd, Rf(1:3, ia), Rc(1:3,ia))
   enddo
   call  write_xyz('fff.xyz', boxl, boxa, an, Rc)
   dh = (rmax - rmin) / dble(ngrid-1)
   rmaxsq = rmax*rmax
   grid = 0

   ns = 0
   do ia=1, na-1
      ri = rf(1:3, ia)
      api = ap(ia)
      do ja=ia+1, na
         rij = ri - rf(1:3, ja)
         call calcRij(rprimd, rij, drsq)
         
         dr = sqrt(drsq)

         idx = (dr - rmin) / dh + 1

         if (idx<1 .or. idx>ngrid) then
!            print*,'out of grid boundaries', idx
            cycle
         endif

         ns = ns+1
         apij = api*ap(ja)
         do j=1, ngrid
            rgrid = rmin+(j-1)*dh
            grid(j) = grid(j) + apij*exp(-Bfac*(   (rgrid-dr)**2)   )! / rgrid**2
         enddo
      enddo
   enddo
   !... normalize grig
   sumg = sum(grid)
!   print*,'sum=', sumg, dh
!   print*,'ns=', ns
   grid = grid/(sumg*dh)
   !SOS
!   do j=1, ngrid
!      rgrid = rmin+(j-1)*dh
!      grid(j) = grid(j) / rgrid**2
!   enddo

   end subroutine get_rdf
   !
   !
   !
   subroutine init_cell( boxl, boxa, rprimd, gprimd )
   implicit none
   double precision, dimension(3) :: boxl, boxa
   double precision, dimension(3,3), intent(   out ) :: rprimd, gprimd
   double precision ::  ca, cb, cc, sc, t1, t2, t3
   ca = cos(boxa(1))
   cb = cos(boxa(2))
   cc = cos(boxa(3))
   sc = sin(boxa(3))
   rprimd(1, 1:3) = [boxl(1), 0.d0, 0.d0 ]
   rprimd(2, 1:3) = [boxl(2)*cc, boxl(2)*sc, 0.d0]
   t1 = cb
   t2 = (ca -cc*cb) / sc
   t3 = sqrt(1.d0 - ca**2 - cb**2 - cc**2 + 2.d0*ca*cb*cc) / sc
   rprimd(3, 1:3) = boxl(3)*[t1, t2, t3]
   rprimd = transpose( rprimd )

   call matr3inv(rprimd,  gprimd)
   gprimd=transpose(gprimd)
   end subroutine init_cell

   subroutine get_numberofreplicas(rprimd, rc, nxyz)
   !
   !   given the initial frame (frame) and the cutoff (rc)
   !   returns the number in the 3-directions that it has to be replicated
   !   in order each dimension to be > 2*Rc
   !   (IDEA for the implementation taken from RASPA2)
   !
   implicit none
   double precision, dimension(3,3), intent( in    ) :: rprimd
   double precision,           intent( in    ) :: rc
   integer, dimension(3),      intent(   out ) :: nxyz
   !..
   double precision, dimension(3) :: v1, v2, v3, v1x2, v2x3, v3x1
   double precision :: dv1x2, dv2x3, dv3x1, vol, lxx, lyy, lzz
 
   v1 = rprimd(:,1)
   v2 = rprimd(:,2)
   v3 = rprimd(:,3)
   call outprod3(v1, v2, v1x2); dv1x2=sqrt(dot_product(v1x2, v1x2))
   call outprod3(v2, v3, v2x3); dv2x3=sqrt(dot_product(v2x3, v2x3))
   call outprod3(v3, v1, v3x1); dv3x1=sqrt(dot_product(v3x1, v3x1))
   vol = dot_product(v1, v2x3)
   lxx = vol/dv2x3
   lyy = vol/dv3x1
   lzz = vol/dv1x2
   nxyz(1) = 2.d0*rc/lxx + 1
   nxyz(2) = 2.d0*rc/lyy + 1
   nxyz(3) = 2.d0*rc/lzz + 1
   print*,'replicate Cell as ', nxyz(1:3)
 
   end subroutine get_numberofreplicas
   !
   !
   !
   subroutine calcRij(rprimd, rij, drsq)
!   subroutine calcRij(boxl, boxa, rprimd, rij, drsq)
   !... on input rij is at fractional coordinates
!   double precision, dimension(3), intent( in    ) :: boxl, boxa
   double precision, dimension(3, 3), intent( in    ) :: rprimd     
   double precision, dimension(3), intent( inout ) :: rij
   double precision, optional,     intent(   out ) :: drsq
   !... local variables
   integer :: ii
   double precision, dimension(3) :: r1
 
      do ii=1, 3
         r1(ii) = Rij(ii) + 1.d0
         do while (r1(ii) .gt. 0.5d0)
            r1(ii) = r1(ii) - 1.d0
         end do
         do while (r1(ii) .lt. -0.5d0)
            r1(ii) = r1(ii) + 1.d0
         end do
      enddo
      call frac2cart(rprimd, r1, rij)
 
   if (present(drsq)) drsq=rij(1)*rij(1) + rij(2)*rij(2) + rij(3)*rij(3)
   end subroutine calcRij
   !--------------------------------------------------------------------------
   !>  @author  GSF
   !!  @brief if (pbc) transforms the fractional (r1) to cartesian (r2) coordinates
   !!  @param[in] r1
   !!  @param[out] r2
   !--------------------------------------------------------------------------
   subroutine frac2cart(rprimd, r1, r2)
   implicit none
   double precision, dimension(3,3), intent( in    ) :: rprimd
   double precision, dimension(3),   intent( in    ) :: r1
   double precision, dimension(3),   intent(   out ) :: r2
 
   r2 = matmul(rprimd, r1)
   end subroutine frac2cart

   !--------------------------------------------------------------------------
   !>  @author  GSF
   !!  @brief if (pbc) transforms the fractional (r1) to cartesian (r2) coordinates
   !!  @param[in] r1
   !!  @param[out] r2
   !--------------------------------------------------------------------------
   subroutine cart2frac(gprimd, r1, r2)
   implicit none
   double precision, dimension(3,3), intent( in    ) :: gprimd
   double precision, dimension(3),   intent( in    ) :: r1
   double precision, dimension(3),   intent(   out ) :: r2
 
   r2 = matmul(gprimd, r1)
   end subroutine cart2frac

   !.........................................................
   subroutine matr3inv(aa,ait)
   !.........................................................
   implicit none
   double precision :: aa(3,3),ait(3,3)
   double precision :: dd,t1,t2,t3
     
   
   t1 = aa(2,2) * aa(3,3) - aa(3,2) * aa(2,3)
   t2 = aa(3,2) * aa(1,3) - aa(1,2) * aa(3,3)
   t3 = aa(1,2) * aa(2,3) - aa(2,2) * aa(1,3)
   dd  = 1.d0/ (aa(1,1) * t1 + aa(2,1) * t2 + aa(3,1) * t3)
   ait(1,1) = t1 * dd
   ait(2,1) = t2 * dd
   ait(3,1) = t3 * dd
   ait(1,2) = (aa(3,1)*aa(2,3)-aa(2,1)*aa(3,3)) * dd
   ait(2,2) = (aa(1,1)*aa(3,3)-aa(3,1)*aa(1,3)) * dd
   ait(3,2) = (aa(2,1)*aa(1,3)-aa(1,1)*aa(2,3)) * dd
   ait(1,3) = (aa(2,1)*aa(3,2)-aa(3,1)*aa(2,2)) * dd
   ait(2,3) = (aa(3,1)*aa(1,2)-aa(1,1)*aa(3,2)) * dd
   ait(3,3) = (aa(1,1)*aa(2,2)-aa(2,1)*aa(1,2)) * dd
   
   end subroutine matr3inv
   !.........................................................
   subroutine outprod3(a1,a2,a3)
   !.........................................................
   implicit none
   double precision, dimension(3), intent(in) :: a1, a2
   double precision, dimension(3), intent(out) :: a3
   
   a3(1) =  a1(2)*a2(3) - a1(3)*a2(2)
   a3(2) = -a1(1)*a2(3) + a1(3)*a2(1)
   a3(3) =  a1(1)*a2(2) - a1(2)*a2(1)
   
   end  subroutine outprod3

   !.........................................................
   function getvolume(rprimd) result (vol)
   !.........................................................
   implicit none
   double precision, dimension(3,3) :: rprimd
   double precision                                :: vol

   vol = rprimd(1,1) * rprimd(2,2) * rprimd(3,3)
   end function getvolume

   !
   subroutine write_xyz(finp, boxl, boxa, an, R)
   !  assume R in cartesian coordinates
   implicit none
   character(len=*) :: finp
   double precision, dimension(3) :: boxl, boxa
   character(len=*), dimension(:) :: an
   double precision, dimension(:,:) :: R
   !.... local variables
   integer :: ia, na

   na = size(an, dim=1)
   open(unit=111, file=trim(finp))
   write(111,*)na
   write(111,'(6(f12.5,1x))')boxl, boxa*180.d0/3.14159265d0
   do ia=1, na
      write(111,'(a3,2x, 3(f12.6,1x))')trim(an(ia)), R(1:3, ia)
   enddo
   close(111)
   end subroutine write_xyz
   !
   !
   !
   subroutine read_cif(fn, boxl, boxa, anames, Rf)
   implicit none
   character(len=*) :: fn
   double precision, dimension(3) :: boxl, boxa
   character(len=*), dimension(:), allocatable :: anames
   double precision, dimension(:,:), allocatable :: Rf
   !....
   character(len=3), dimension(:), allocatable :: anames0
   double precision, dimension(:,:), allocatable :: Rf0
   integer :: na, iostat, itmp
   character(len=1000) :: line, tstr

   allocate(Rf0(3, 10000))
   allocate(anames0(10000))

   na = 0
   open(11, file=trim(fn))
   do
      read(11,'(a)', iostat=iostat)line
      if (iostat/=0) exit
      if (index(line,'_cell_length_a')>0) read(line,*)tstr, boxl(1)
      if (index(line,'_cell_length_b')>0) read(line,*)tstr, boxl(2)
      if (index(line,'_cell_length_c')>0) read(line,*)tstr, boxl(3)
      if (index(line,'_cell_angle_alpha')>0) read(line,*)tstr, boxa(1)
      if (index(line,'_cell_angle_beta')>0) read(line,*)tstr, boxa(2)
      if (index(line,'_cell_angle_gamma')>0) read(line,*)tstr, boxa(3)
      if (index(line,'_atom_site_occupancy')>0) then
         do
            read(11,'(a)', iostat=iostat)line
            if (iostat/=0 .or. line(1:1)=='"') exit
            na = na+1
            read(line,*)anames0(na), tstr, Rf0(1:3, na)
         enddo
      endif
   enddo
   close(11)
   allocate(Rf(3, na)); Rf(1:3, 1:na)=Rf0(1:3, 1:na)
   allocate(anames(na)); anames(1:na)=anames0(1:na)
   deallocate(Rf0, anames0)
   end subroutine read_cif
   !
   !
   !
   subroutine read_pdb(fn, boxl, boxa, anames, Rf)
   implicit none
   character(len=*) :: fn
   double precision, dimension(3) :: boxl, boxa
   character(len=*), dimension(:), allocatable :: anames
   double precision, dimension(:,:), allocatable :: Rf
   !....
   character(len=3), dimension(:), allocatable :: anames0
   double precision, dimension(:,:), allocatable :: Rf0
   integer :: ia, na, iostat, itmp
   double precision, dimension(3, 3) :: rprimd, gprimd
   character(len=1000) :: line, tstr, tstr1, nm1

   allocate(Rf0(3, 10000))
   allocate(anames0(10000))

   na = 0
   open(11, file=trim(fn))
   do
      read(11,'(a)', iostat=iostat)line
      if (iostat/=0) exit

      if (index(line,'CRYST1')==1) then
         read(line,*)tstr, boxl(1:3), boxa(1:3)
         boxa = boxa*3.14159265d0/180.d0
      endif

      if (index(line,'HETATM')==1) then
         na = na+1
         read(line,*)tstr, tstr1, nm1, tstr, tstr, Rf0(1:3, na)
         anames0(na) = trim(nm1)
      endif
   enddo
   close(11)

   !
   call init_cell( boxl, boxa, rprimd, gprimd )

   allocate(Rf(3, na)); 
   allocate(anames(na));

   do ia=1, na
      anames(ia) = trim(anames0(ia))
      call cart2frac(gprimd, Rf0(1:3, ia), Rf(1:3, ia))  !fractional coordinates
   enddo

!   print*,'rprimd=', rprimd
!   print*,'gprimd=', gprimd
   deallocate(Rf0, anames0)
   end subroutine read_pdb
   !
   !
   !
   function to_lower(strIn) result(strOut)
   ! Adapted from http://www.star.le.ac.uk/~cgp/fortran.html (25 May 2012)
   ! Original author: Clive Page

   implicit none

   character(len=*), intent(in) :: strIn
   character(len=len(strIn)) :: strOut
   integer :: i,j

   do i = 1, len(strIn)
        j = iachar(strIn(i:i))
        if (j>= iachar("A") .and. j<=iachar("Z") ) then
             strOut(i:i) = achar(iachar(strIn(i:i))+32)
        else
             strOut(i:i) = strIn(i:i)
        end if
   end do

   end function to_lower


end module neighlist_mod
