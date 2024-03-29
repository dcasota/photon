Summary:    Utilities for writing cds.
Name:       cdrkit
Version:    1.1.11
Release:    5%{?dist}
License:    GPLv2+
Group:      System Environment/Base
Vendor:     VMware, Inc.
Distribution:   Photon
URL:        http://gd.tuwien.ac.at/utils/schilling/cdrtools/

Source0:    %{name}-%{version}.tar.gz
%define sha512 %{name}=e5afcd2cb68d39aeff680a0d5b0a7877f94cf6de111b3cb7388261c665fbd3209ce98a20a01911875af7d6b832a156801b1fa46a4481f7c8ba60b22eac0a5b05

Patch0:     cdrkit-1.1.9-efi-boot.patch
Patch1:     cdrkit-1.1.11-gcc10.patch

Requires:   bash
Requires:   libcap

BuildRequires:  cmake
BuildRequires:  libcap-devel
BuildRequires:  bzip2-devel

%description
The Cdrtools package contains CD recording utilities. These are useful for reading, creating or writing (burning) Compact Discs.

%prep
%autosetup -p1

%build
%make_build

%install
export PREFIX=%{_prefix}
%make_install %{?_smp_mflags}
ln -sfv genisoimage %{buildroot}%{_bindir}/mkisofs

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_sbindir}/*
%{_datadir}/man/*

%changelog
* Thu Jan 14 2021 Alexey Makhalov <amakhalov@vmware.com> 1.1.11-5
- GCC-10 support.
* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 1.1.11-4
- Remove BuildArch
* Mon Mar 6 2017 Alexey Makhalov <amakhalov@vmware.com> 1.1.11-3
- Support for efi boot (.patch)
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.1.11-2
- GA - Bump release of all rpms
* Sat Feb 14 2015 Sharath George <sharathg@vmware.com>
- first packaging
