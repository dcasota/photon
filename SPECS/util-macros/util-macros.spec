Summary:        m4 macros used by all of the Xorg packages.
Name:           util-macros
Version:        1.19.3
Release:        1%{?dist}
License:        MIT
URL:            http://www.x.org
Group:          Development/System
BuildArch:      noarch
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.x.org/pub/individual/util/%{name}-%{version}.tar.bz2
%define sha512 %{name}=b9c7398a912c688a782eab5b1e0f6da2df11a430775c5c98fc3269f73a665de6eeb60d300a849e38d345714a6e51f74e9334cb6039767304cca4b93d823a53a2

%description
The util-macros package contains the m4 macros used by all of the Xorg packages.

%prep
%autosetup -p1

%build
%configure

%install
%make_install %{?_smp_mflags}

%ldconfig_scriptlets

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_datadir}/aclocal/xorg-macros.m4
%{_datadir}/pkgconfig/xorg-macros.pc
%{_datadir}/util-macros

%changelog
* Wed Dec 14 2022 Gerrit Photon <photon-checkins@vmware.com> 1.19.3-1
- Automatic Version Bump
* Fri May 15 2015 Alexey Makhalov <amakhalov@vmware.com> 1.19.0-1
- initial version
