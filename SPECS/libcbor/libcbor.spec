Summary:        A CBOR parsing C library
Name:           libcbor
Version:        0.9.0
Release:        4%{?dist}
URL:            http://libcbor.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/PJK/%{name}/archive/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  glibc-devel
BuildRequires:  cmake

Requires:  glibc

%description
%{name} is a C library for parsing and generating CBOR, the general-purpose schema-less binary data format.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description devel
%{name}-devel contains the development libraries and header files for %{name}.

%prep
%autosetup -p1

%build
# A Debug build compiles at -O0 with DEBUG defined and, with libcbor's
# SANITIZE option on by default, links ASan and UBSan into the shipped
# library and into everything that loads it.
%cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DSANITIZE=OFF \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir}

%cmake_build

%install
%cmake_install

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%license LICENSE.md
%doc README.md
%{_libdir}/%{name}.so.0*

%files devel
%defattr(-,root,root)
%{_libdir}/%{name}.so
%{_includedir}/cbor.h
%{_includedir}/cbor/*.h
%{_includedir}/cbor/internal/*.h
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Sat Oct 03 2026 Daniel Casota <dcasota@gmail.com> 0.9.0-4
- Build the release configuration instead of Debug
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 0.9.0-3
- Release bump for SRP compliance
* Tue Jun 14 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.9.0-2
- Fix packaging & fix build with latest cmake
* Fri May 13 2022 Nitesh Kumar <kunitesh@vmware.com> 0.9.0-1
- Initial version
