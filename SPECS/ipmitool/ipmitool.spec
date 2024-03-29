%global debug_package %{nil}
%define ipmi_ver 1_8_19

Summary:        ipmitool - Utility for IPMI control
Name:           ipmitool
Version:        1.8.19
Release:        4%{?dist}
License:        BSD
Group:          System Environment/Utilities
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/ipmitool/ipmitool

Source0: https://github.com/ipmitool/ipmitool/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=2d91706e9feba4b2ce4808eca087b81b842c4292a5840830001919c06ec8babd8f8761b74bb9dcf8fbc7765f028a5b1a192a3c1b643f2adaa157fed6fb0d1ee3

BuildRequires:  autoconf
BuildRequires:  autoconf-archive
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  glib
BuildRequires:  glibc
BuildRequires:  openssl-devel
BuildRequires:  curl-devel

Requires:   openssl
Requires:   curl

%description
This package contains a utility for interfacing with devices that support
the Intelligent Platform Management Interface specification.  IPMI is
an open standard for machine health, inventory, and remote power control.

This utility can communicate with IPMI-enabled devices through either a
kernel driver such as OpenIPMI or over the RMCP LAN protocol defined in
the IPMI specification.  IPMIv2 adds support for encrypted LAN
communications and remote Serial-over-LAN functionality.

It provides commands for reading the Sensor Data Repository (SDR) and
displaying sensor values, displaying the contents of the System Event
Log (SEL), printing Field Replaceable Unit (FRU) information, reading and
setting LAN configuration, and chassis power control.

%prep
%autosetup -p1 -n %{name}-IPMITOOL_%{ipmi_ver}

%build
sh ./bootstrap
%configure \
    --with-kerneldir \
    --with-rpm-distro=

%make_build

%install
%make_install install-strip %{?_smp_mflags}

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(755,root,root)
%{_bindir}/*
%{_sbindir}/*
%{_datadir}/%{name}/*
%{_mandir}/man*/*
%doc %{_docdir}/ipmitool
%{_datadir}/misc/enterprise-numbers

%changelog
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.8.19-4
- Bump version as a part of openssl upgrade
* Thu Dec 22 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.8.19-3
- Bump version as a part of readline upgrade
* Sun Nov 13 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.8.19-2
- Bump version as a part of autoconf-archive upgrade
* Thu Sep 22 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.8.19-1
- Upgrade to v1.8.19
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.8.18-6
- Bump up release for openssl
* Thu Jan 14 2021 Alexey Makhalov <amakhalov@vmware.com> 1.8.18-5
- GCC-10 support.
* Fri Jul 24 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.8.18-4
- Make ipmitool compatible for openssl-1.1.x
* Thu Mar 05 2020 Keerthana K <keerthanak@vmware.com> 1.8.18-3
- Fix %configure.
* Thu Feb 13 2020 Keerthana K <keerthanak@vmware.com> 1.8.18-2
- Fix CVE-2020-5208.
* Fri Aug 25 2017 Xiaolin Li <xiaolinl@vmware.com> 1.8.18-1
- Initial build.  First version
