module neighlist_mod

implicit none
type t_atomic_properties
   character(len=3), dimension(116) :: symbol
   double precision, dimension(116) :: elneg, pol, rvdw
end type t_atomic_properties
!double precision, parameter :: PI=3.14159265d0
!type (t_box) :: box
!private
!public :: get_rdf, init_cell


Contains
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
   print*, 'pos C=',  iloc
   norm_elneg = ap% elneg(iloc)
   norm_pol = ap% pol(iloc)
   norm_rvdw = ap% rvdw(iloc)
   do i=1, size(ap% symbol)
      ap% elneg(i) = ap% elneg(i) / norm_elneg
      ap% pol(i)   = ap% pol(i)   / norm_pol
      ap% rvdw(i)  = ap% rvdw(i)  / norm_rvdw
      write(*,'(a5,3(3x, f8.4))')trim(ap% symbol(i)), ap% elneg(i), ap% pol(i), ap% rvdw(i) 
   enddo
!   stop
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
!      print*,'symi=', trim(symi)
      found = .false.
      do j=1, size(ap% symbol)
!         print*,'symbol=', trim(ap% symbol(j))
         if (trim(symi) == trim(ap% symbol(j))) then
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

   end subroutine assign_atomic_properties
   !
   !
   !
   subroutine get_rdf(aprop, b, anames, r1, bfac, rmin, rmax, ngrid, grid, vol)
   ! assume that r1 are in fractional coordinates
   implicit none
   double precision, dimension(6), intent( in     ) :: b
   double precision, dimension(:), intent( in    ) :: aprop
   character*3, dimension(:), intent( in     ) :: anames
   double precision, dimension(:,:), intent( in    ) :: r1
   double precision, intent( in     ) :: bfac, rmin, rmax
   integer, intent(in) :: ngrid
   double precision, dimension(ngrid), intent(   out ) :: grid
   double precision, intent(   out ) :: vol
   !...
   double precision, dimension(:,:), allocatable :: Rf, Rc
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
   boxa(1:3) = b(4:6)*3.14159265d0/180.d0
   call init_cell(boxl, boxa, rprimd, gprimd)
   call get_numberofreplicas(rprimd, rmax, nxyz)
!   print*,'nxyz=', nxyz
   nxyz=1
   !
   !
   !   replicate unit cell so that the three box linear dimensions are larger than 2*Rmax
   !
   ! 
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
   print*,'na0=', na0,  '  na=', na
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
         
!         if (drsq>rmaxsq) cycle

         dr = sqrt(drsq)

         idx = (dr - rmin) / dh + 1

         if (idx<1 .or. idx>ngrid) then
            print*,'out of grid boundaries', idx
            cycle
         endif

         ns = ns+1
         apij = api*ap(ja)
         do j=1, ngrid
            rgrid = rmin+(j-1)*dh
            grid(j) = grid(j) + apij*exp(-Bfac*(rgrid-dr)**2)
         enddo
      enddo
   enddo
   !... normalize grig
   sumg = sum(grid)
   print*,'sum=', sumg, dh
   print*,'ns=', ns
!   grid = grid/(sumg*dh)
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
   !
   !
   !

!   subroutine replicateCell( nxyz, boxl0, boxa0, R0, anames0, boxl1, )
!   use box_mod
!   use t_frame_mod, only: t_framework
!   implicit none
!   integer, dimension(3), intent( in    ) :: nxyz
!   type(t_framework), target,  intent( inout ) :: frame
!   !... local variables
!   integer :: ix, iy, iz, ia, idx0, idx, na, nna
!   double precision, dimension(3) :: shft, R0
!   double precision, dimension(:,:), allocatable :: R2, Rfrac
!   type(t_box), pointer :: box
!   character(len=10), dimension(:), allocatable :: at_names2, at_types2
!   double precision, dimension(:), allocatable :: lj_e2, lj_s2, qarr
!   double precision :: vol0, vol1!, drsq
!   type (t_box) :: box1
!
!   na = size(frame% R, dim=2)
!   nna = na*nxyz(1)*nxyz(2)*nxyz(3)
!   box => frame% box
!
!   allocate(Rfrac(3, na))
!   do ia=1, na
!      R0 = frame% R(1:3, ia)
!      call cart2frac( box, R0, Rfrac(1:3, ia) )
!   enddo
!
!   vol0 = getvolume ( box )
!   box1 = box
!   box1% l(1:3) = box% l(1:3)*nxyz
!   call init_box ( box1 )
!   do ia=1, na
!      R0 = frame% R(1:3, ia)
!      call cart2frac( box1, R0, Rfrac(1:3, ia) )
!   enddo
!   vol1 = getvolume ( box1 )
!   allocate(R2(3, nna))
!   allocate(at_names2(nna))
!   allocate(at_types2(nna))
!   allocate(lj_e2(nna))
!   allocate(lj_s2(nna))
!   allocate(qarr(nna))
!   idx0 = 0
!   do iz=1, nxyz(3)
!      do iy=1, nxyz(2)
!         do ix=1, nxyz(1)
!            shft = [  dble(ix-1) / nxyz(1),  dble(iy-1) / nxyz(2),  dble(iz-1) / nxyz(3)]
!
!            do ia=1, na
!               idx  = ia + idx0
!               R2(1:3, idx) = Rfrac(1:3, ia) + shft
!               call frac2cart( box1, R2(1:3, idx), R2(1:3, idx) )
!               at_names2(idx) = frame% at_names(ia)
!               lj_e2(idx) = frame% lj_e(ia)
!               lj_s2(idx) = frame% lj_s(ia)
!               qarr(idx) = frame% q(ia)
!            enddo
!            idx0 = idx0 + na
!         enddo
!      enddo
!   enddo
!
!   box = box1
!   call init_box (  box  )
!
!   deallocate(frame% R, frame% q, frame% at_names, frame% lj_e, frame% lj_s)
!   allocate(frame% R(3, nna)); frame% R=r2
!   allocate(frame% at_names(nna)); frame% at_names = at_names2
!   allocate(frame% lj_e(nna)); frame% lj_e = lj_e2
!   allocate(frame% lj_s(nna)); frame% lj_s = lj_s2
!   allocate(frame% q(nna)); frame% q = qarr
!   frame% totmass = frame% totmass * nxyz(1)*nxyz(2)*nxyz(3)
!   deallocate( R2, Rfrac, at_names2, at_types2, lj_e2, lj_s2, qarr )
!   end subroutine replicateCell


    !
    !
    !
    subroutine calcRij(rprimd, rij, drsq)
!    subroutine calcRij(boxl, boxa, rprimd, rij, drsq)
    !... on input rij is at fractional coordinates
!    double precision, dimension(3), intent( in    ) :: boxl, boxa
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
             print*,'l=', trim(line)
             na = na+1
             read(line,*)anames0(na), tstr, itmp, Rf0(1:3, na)
          enddo
       endif
    enddo
    close(11)
    allocate(Rf(3, na)); Rf(1:3, 1:na)=Rf0(1:3, 1:na)
    allocate(anames(na)); anames(1:na)=anames0(1:na)
    deallocate(Rf0, anames0)
    end subroutine read_cif

!   subroutine replicate_cell()
!
!   end subroutine replicate_cell

end module neighlist_mod
