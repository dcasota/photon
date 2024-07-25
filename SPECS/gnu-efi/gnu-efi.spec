Name:           gnu-efi
Version:        3.0.15
Release:        2%{?dist}
Summary:        Development Libraries and headers for EFI
License:        BSD
URL:            https://sourceforge.net/projects/gnu-efi
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://download.sourceforge.net/gnu-efi/%{name}-%{version}.tar.bz2
%define sha512 %{name}=64d408b6d115bdc6eebae12fbd6cd907ed5f847f54e506c1e8f8ea5de38a95cf6fac66ab1009bd1d0bd2d54ad45ad598d29bcc303926a5899bf5cc25448cbb2f

Patch0: aarch64-Fix-ld-RWX-warning.patch

BuildRequires: binutils
BuildRequires: gcc
BuildRequires: make

%define debug_package %{nil}

%description
This package contains development headers and libraries for developing
applications that run under EFI (Extensible Firmware Interface).

%prep
%autosetup -p1 -n %{name}-%{version}

%build
export CFLAGS="${CFLAGS} -ffat-lto-objects"
%make_build
%make_build -C lib
%make_build -C gnuefi
%make_build -C inc

export LDFLAGS=""
%make_build -C apps

%install
%make_install %{?_smp_mflags} PREFIX=%{_prefix} LIBDIR=%{_libdir} INSTALLROOT=%{buildroot}

%files
%defattr(-,root,root)
%{_includedir}/efi
%{_libdir}/elf_%{_arch}_efi.lds
%{_libdir}/crt0-efi-%{_arch}.o
%{_libdir}/libefi.a
%{_libdir}/libgnuefi.a

%changelog
* Mon Oct 10 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 3.0.15-2
- Fix build for aarch64
* Thu Sep 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.0.15-1
- Upgrade to v3.0.15
* Tue Jan 11 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.0.14-1
- Intial version needed for systemd-250.x
