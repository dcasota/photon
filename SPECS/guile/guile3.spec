%define guile_major_ver 3.0

Summary:        GNU Ubiquitous Intelligent Language for Extensions
Name:           guile3
Version:        3.0.8
Release:        3%{?dist}
License:        LGPLv3+
URL:            http://www.gnu.org/software/guile
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://ftp.gnu.org/gnu/guile/guile-%{version}.tar.xz
%define sha512 guile=5d1d93e3e22c524ea3c2fe28cf3c343ab8ba99bf5c7b8750c4ebcaf556ae21485fb99e5ccc50c4b07037cdc678552557753d67ef2c93d8c1b62603e1809418f6

BuildRequires:  libltdl-devel
BuildRequires:  libunistring-devel
BuildRequires:  gc-devel
BuildRequires:  libffi-devel
BuildRequires:  readline-devel

Requires:       readline
Requires:       libltdl
Requires:       libunistring
Requires:       gc
Requires:       libffi
Requires:       gmp
Requires:       glibc-iconv

%description
GUILE (GNU's Ubiquitous Intelligent Language for Extension) is a library
implementation of the Scheme programming language, written in C.  GUILE
provides a machine-independent execution platform that can be linked in
as a library during the building of extensible programs.

%package        devel
Summary:        Development libraries and header files for guile
Requires:       %{name} = %{version}-%{release}
Requires:       libltdl-devel
Requires:       libunistring-devel
Requires:       gc-devel

%description    devel
The package contains libraries and header files for
developing applications that use guile.

%prep
%autosetup -p1 -n guile-%{version}

%build
%configure \
    --disable-static \
    --disable-error-on-warning \
    --program-suffix=%{guile_major_ver}

%make_build

%install
%make_install %{?_smp_mflags}

rm -f %{buildroot}%{_libdir}/*.scm \
      %{buildroot}%{_infodir}/* \
      %{buildroot}%{_libdir}/*.la

%check
%make_build check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/guile/*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_datadir}/aclocal/*.m4
%{_includedir}/guile/%{guile_major_ver}/*.h
%{_includedir}/guile/%{guile_major_ver}/libguile/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/guile/*

%changelog
* Thu Sep 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.0.8-3
- Fix devel package requires
* Thu Dec 22 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.0.8-2
- Bump version as a part of readline upgrade
* Sat Oct 01 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.0.8-1
- First build, guile3.
