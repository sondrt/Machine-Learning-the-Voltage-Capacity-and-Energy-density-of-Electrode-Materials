!module neighlist_mod
!implicit none

!type t_box 
!   double precision, dimension(3) :: l, a
!   double precision, dimension(3, 3) :: rprimd, gprimd
!end type t_box 

!double precision, parameter :: PI=3.14159265d0
!type (t_box) :: box
!private
!public :: get_rdf, init_cell

!Contains
   !
   !
   !
   subroutine get_rdf(nn, b, anames, r1, rmin, rmax, ngrid, grid, vol)
   implicit none
   integer, intent(in) :: nn
   double precision, dimension(6), intent( in     ) :: b
   character*3, dimension(nn), intent( in     ) :: anames
   double precision, dimension(3*nn), intent( in    ) :: r1
   double precision, intent( in     ) :: rmin, rmax
   integer, intent(in) :: ngrid
   double precision, dimension(ngrid), intent(   out ) :: grid
   double precision, intent(   out ) :: vol
!   !t2py integer, intent(in) :: nn
   !...
   double precision, dimension(:,:), allocatable :: acoords
   double precision, dimension(3) :: boxl, boxa
   double precision, dimension(3, 3) :: rprimd, gprimd
   integer, dimension(3) :: nxyz
   integer :: i, nat, na


   print*, 'nn=', nn
   Na = size(anames)
   allocate(acoords(3, na))
   acoords = reshape(r1, [3, na])

!   print*,'na=', na
!   print*, 'anames=', anames
   Nat = size(anames)
   print*,'nat = ', nat
   do i=1, nat
      print*,trim(anames(i)), acoords(1:3, i)
   enddo


   boxl(1:3) = b(1:3)
   boxa(1:3) = b(4:6)*3.14159265d0/180.d0
   call init_cell(boxl, boxa, rprimd, gprimd)
   print*, 'boxl=', boxl
   call get_numberofreplicas(rprimd, rmax, nxyz)
   print*,'nxyz= ', nxyz
   deallocate(acoords)
   vol = product(boxl)
   grid=1.1d0
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
    subroutine calcRij(boxl, boxa, rprimd, rij, drsq)
    !... on input rij is at fractional coordinates
    double precision, dimension(3), intent( in    ) :: boxl, boxa
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



!   subroutine replicate_cell()
!
!   end subroutine replicate_cell

!end module neighlist_mod
