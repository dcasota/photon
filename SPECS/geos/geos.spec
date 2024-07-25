Summary:        A C++11 library for performing operations on two-dimensional vector geometries
Name:           geos
Version:        3.11.1
Release:        1%{?dist}
License:        LGPLv2
URL:            https://trac.osgeo.org/geos
Group:          System Environment/Development
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://download.osgeo.org/geos/%{name}-%{version}.tar.bz2
%define sha512 %{name}=708500aba9b04208ee46a531d55ddf63a213dfaa2922dae937b524300b2b46c95143ed6cd3ff1414e9099f2be95e5df5a2e0b49df43acf93a9478215259f20d3

BuildRequires:  cmake

%description
GEOS (Geometry Engine - Open Source) is a C++ port of the JTS Topology Suite (JTS).
It aims to contain the complete functionality of JTS in C++.

%package    devel
Summary:    Header and development files
Requires:   %{name} = %{version}-%{release}

%description    devel
It contains the libraries and header files

%prep
%autosetup -p1

%build
%cmake \
    -DDEFAULT_BUILD_TYPE=Debug \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir}

%cmake_build

%install
%cmake_install

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%clean
rm -rf %{buildroot}/*

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/geos-config
%{_bindir}/geosop
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/geos
%{_includedir}/geos.h
%{_includedir}/geos_c.h
%{_libdir}/*.so
%{_libdir}/cmake/GEOS
%{_libdir}/pkgconfig/geos.pc

%changelog
* Tue Dec 13 2022 Gerrit Photon <photon-checkins@vmware.com> 3.11.1-1
- Automatic Version Bump
* Thu Sep 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.11.0-1
- Upgrade to v3.11.0
* Fri Jun 17 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.10.2-2
- Fix build with latest cmake
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 3.10.2-1
- Automatic Version Bump
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 3.9.1-1
- Automatic Version Bump
* Wed Jul 22 2020 Gerrit Photon <photon-checkins@vmware.com> 3.8.1-1
- Automatic Version Bump
* Mon Mar 09 2020 Ankit Jain <ankitja@vmware.com> 3.8.0-1
- Initial build.  First version.
