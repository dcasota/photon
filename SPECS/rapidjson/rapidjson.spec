%global debug_package %{nil}
Summary:	A fast JSON parser/generator for C++ with both SAX/DOM style API
Name:		rapidjson
Version:	1.1.0
Release:	5%{?dist}
License:	BSD, JSON, MIT
URL:		https://github.com/gcc-mirror/gcc/blob/master/gcc/gcov.c
Source0:	https://github.com/miloyip/rapidjson/archive/%{name}-%{version}.tar.gz
%define sha1 rapidjson=a3e0d043ad3c2d7638ffefa3beb30a77c71c869f
Patch0:         rapidjson-fix-Wclass-memaccess-warnings-errors.patch
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildRequires:	cmake

Patch1: 0001-Supress-implicit-fallthrough-in-GCC.patch
Patch2: 0001-Onley-apply-to-GCC-7.patch
%ifarch aarch64
Patch3: Fix-build-warnings-emitted-by-GCC-10-on-Aarch64.patch
%endif

%description
RapidJSON is a JSON parser and generator for C++. It was inspired by RapidXml.

%package devel
Summary:        Fast JSON parser and generator for C++
Group:          Development/Libraries/C and C++
Provides:       %{name} == %{version}

%description devel
RapidJSON is a header-only JSON parser and generator for C++.
This package contains development headers and examples.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%ifarch aarch64
%patch3 -p1
%endif

%build
mkdir build && cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} -DBUILD_SHARED_LIBS=ON ..
make %{?_smp_mflags}

%install
cd build
make DESTDIR=%{buildroot} install

%check
make test


%files devel
%defattr(-,root,root)
%dir %{_libdir}/cmake/RapidJSON
%{_libdir}/cmake/RapidJSON/*
%{_libdir}/pkgconfig/*.pc
%{_includedir}
%{_datadir}
%changelog
*   Tue Feb 09 2021 Alexey Makhalov <amakhalov@vmware.com> 1.1.0-5
-   Fix compilation issue with gcc-10.2.0 for aarch64
*   Fri Apr 03 2020 Alexey Makhalov <amakhalov@vmware.com> 1.1.0-4
-   Fix compilation issue with gcc-8.4.0
*   Mon Nov 19 2018 Vasavi Sirnapalli <vsirnapalli@vmware.com> 1.1.0-3
-   Fix makecheck
*   Wed Aug 08 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.1.0-2
-   Fix build failure with gcc 7.3
*   Fri Jun 09 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.1.0-1
-   Initial build. First version
