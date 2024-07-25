Summary:       Team driver
Name:          libteam
Version:       1.31
Release:       4%{?dist}
License:       GPLv2+
URL:           http://www.libteam.org
Group:         System Environment/Libraries
Vendor:        VMware, Inc.
Distribution:  Photon

Source0: http://libteam.org/files/%{name}-%{version}.tar.gz
%define sha512 %{name}=f18cbe7316f6ac8ddf019d2e4b52e19fbdbc75d637f8cacda15b29d679508919230e1af3eb656febe7aafdf8a94c4334f2ae95ecd60bc89ac379622b99d3b615

BuildRequires: libnl-devel
BuildRequires: libdaemon-devel
BuildRequires: jansson-devel

Requires: libnl

%description
The libteam package contains the user-space components of the Team driver.
It provides a mechanism to team multiple NICs into one logical port at the L2 layer.

%package devel
Summary:    Development libraries and header files for libteam
Requires:   %{name} = %{version}-%{release}

%description devel
The package contains libraries and header files for
developing applications that use libteam

%package -n teamd
Summary:        Team network device control daemon
Requires:       %{name} = %{version}-%{release}
Requires:       libnl
Requires:       libdaemon

%description -n teamd
The teamd package contains the team network device control daemon

%package -n teamd-devel
Summary:        Development files for teamd
Requires:       %{name} = %{version}-%{release}

%description -n teamd-devel
The package contains libraries and header files for
developing applications that use teamd and libteamdctl

%prep
%autosetup -p1

%build
%configure \
    --disable-static

%make_build

%install
%make_install %{?_smp_mflags}

install -D -m 0644 teamd/redhat/systemd/teamd@.service \
            %{buildroot}%{_unitdir}/teamd@.service

install -p -m 755 utils/bond2team %{buildroot}%{_bindir}/bond2team

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig/network-scripts \
         %{buildroot}%{_datadir}/teamd/example_configs/

install -p -m 755 teamd/redhat/initscripts_systemd/network-scripts/ifup-Team \
            %{buildroot}%{_sysconfdir}/sysconfig/network-scripts

install -p -m 755 teamd/redhat/initscripts_systemd/network-scripts/ifdown-Team \
            %{buildroot}%{_sysconfdir}/sysconfig/network-scripts

install -p -m 755 teamd/redhat/initscripts_systemd/network-scripts/ifup-TeamPort \
            %{buildroot}%{_sysconfdir}/sysconfig/network-scripts

install -p -m 755 teamd/redhat/initscripts_systemd/network-scripts/ifdown-TeamPort \
            %{buildroot}%{_sysconfdir}/sysconfig/network-scripts

install -p -m 644 teamd/example_configs/* %{buildroot}%{_datadir}/teamd/example_configs/

%preun -n teamd
%systemd_preun teamd@.service

%postun -n teamd
%systemd_postun teamd@.service

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%{_libdir}/libteam.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/team.h
%{_libdir}/libteam.so
%{_libdir}/pkgconfig/libteam.pc

%files -n teamd
%{_libdir}/libteamdctl.so.*
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_sysconfdir}/*
%{_unitdir}/teamd@.service

%files -n teamd-devel
%{_includedir}/teamdctl.h
%{_libdir}/libteamdctl.so
%{_libdir}/pkgconfig/libteamdctl.pc
%{_datadir}/teamd/*

%changelog
* Sat Sep 30 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.31-4
- Fix spec issues
* Sun Aug 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.31-3
- Remove .la files
* Mon Aug 02 2021 Susant Sahani <ssahani@vmware.com> 1.31-2
- Use autosetup and ldconfig scriptlets
* Tue Dec 08 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.31-1
- Initial build. First version
