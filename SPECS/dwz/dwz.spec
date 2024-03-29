Summary:    DWARF optimization and duplicate removal tool
Name:       dwz
Version:    0.15
Release:    3%{?dist}
License:    GPLv2+ and GPLv3+
URL:        https://sourceware.org/dwz
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:     https://sourceware.org/ftp/dwz/releases/%{name}-%{version}.tar.xz
%define sha512 %{name}=43eb4b08c1f529859dc3466697d5ad7e172d6efbf21409530a67a2492ae4acc3734d5134bbd6e07c089ecc358d915871b13e22f6e4f1dd4c3af19ef804f8fcc5

BuildRequires: gcc
BuildRequires: gdb
BuildRequires: dejagnu
BuildRequires: make
BuildRequires: elfutils-libelf-devel
BuildRequires: xxhash-devel

Requires: elfutils-libelf

%description
The dwz package contains a program that attempts to optimize DWARF
debugging information contained in ELF shared libraries and ELF executables
for size, by replacing DWARF information representation with equivalent
smaller representation where possible and by reducing the amount of
duplication using techniques from DWARF standard appendix E - creating
DW_TAG_partial_unit compilation units (CUs) for duplicated information
and using DW_TAG_imported_unit to import it into each CU that needs it.

%prep
%autosetup -p1 -n %{name}

%build
%make_build CFLAGS='%{optflags}' \
  prefix=%{_prefix} mandir=%{_mandir} bindir=%{_bindir}

%install
rm -rf %{buildroot}
%make_install prefix=%{_prefix} mandir=%{_mandir} bindir=%{_bindir}

%check
%if 0%{?with_check}
make check %{?_smp_mflags}
%endif

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%changelog
* Tue Jul 11 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.15-3
- Bump version as a part of elfutils upgrade
* Fri Jan 06 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 0.15-2
- Bump up due to change in elfutils
* Tue Dec 13 2022 Gerrit Photon <photon-checkins@vmware.com> 0.15-1
- Automatic Version Bump. Add xxhash-devel as build requirement.
* Fri Dec 10 2021 Shreenidhi Shedi <sshedi@vmware.com> 0.14-1
- Intial version. Needed for rpm-4.17.0
