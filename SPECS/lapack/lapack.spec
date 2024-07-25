Summary:        linear algebra package
Name:           lapack
Version:        3.11.0
Release:        1%{?dist}
URL:            http://www.netlib.org/lapack
License:        BSD
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://www.netlib.org/%{name}/%{name}-%{version}.tar.gz
%define sha512 %{name}=fc3258b9d91a833149a68a89c5589b5113e90a8f9f41c3a73fbfccb1ecddd92d9462802c0f870f1c3dab392623452de4ef512727f5874ffdcba6a4845f78fc9a

BuildRequires:  cmake
BuildRequires:  gfortran

%description
LAPACK is written in Fortran 90 and provides routines for solving systems of simultaneous linear equations, least-squares solutions of linear systems of equations, eigenvalue problems, and singular value problems. The associated matrix factorizations (LU, Cholesky, QR, SVD, Schur, generalized Schur) are also provided, as are related computations such as reordering of the Schur factorizations and estimating condition numbers. Dense and banded matrices are handled, but not general sparse matrices. In all areas, similar functionality is provided for real and complex matrices, in both single and double precision.

%package        devel
Summary:        Development files for lapack
Group:          Development/Libraries
Requires:       lapack = %{version}-%{release}

%description    devel
The lapack-devel package contains libraries and header files for
developing applications that use lapack.

%prep
%autosetup

%build
%cmake \
      -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
      -DCMAKE_BUILD_TYPE=Debug \
      -DBUILD_SHARED_LIBS=ON \
      -DLAPACKE=ON

%cmake_build

%install
%cmake_install
mkdir %{buildroot}%{_includedir}/lapacke
mv %{buildroot}%{_includedir}/*.h %{buildroot}/%{_includedir}/lapacke/.

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%{_libdir}/libblas.so.*
%{_libdir}/liblapack.so.*
%{_libdir}/liblapacke.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/libblas.so
%{_libdir}/liblapack.so
%{_libdir}/liblapacke.so
%{_includedir}/*
%{_libdir}/pkgconfig

%exclude %{_libdir}/cmake/*

%changelog
* Tue Dec 13 2022 Gerrit Photon <photon-checkins@vmware.com> 3.11.0-1
- Automatic Version Bump
* Mon Jun 20 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.10.1-2
- Use cmake macros for build
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 3.10.1-1
- Automatic Version Bump
* Wed Dec 15 2021 Nitesh Kumar <kunitesh@vmware.com> 3.9.1-2
- Fix for CVE-2021-4048.
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 3.9.1-1
- Automatic Version Bump
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 3.9.0-1
- Automatic Version Bump
* Thu Sep 20 2018 Ankit Jain <ankitja@vmware.com> 3.8.0-1
- Updated to version 3.8.0
* Fri Mar 03 2017 Xiaolin Li <xiaolinl@vmware.com> 3.7.0-1
- Initial packaging for Photon
