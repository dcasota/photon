Name:          htop
Version:       3.2.1
Release:       2%{?dist}
Summary:       Interactive process viewer
License:       GPLv2+
Group:         Applications/System
Vendor:        VMware, Inc.
Distribution:  Photon
URL:           http://hisham.hm/htop/
Source0:       https://github.com/htop-dev/htop/archive/%{name}-%{version}.tar.gz
%define sha512 htop=d7b76e28ee870ac572ba1d9606dec6f9475346a00e599ca15838017c97683f1fc1be40417b9c1e76128cacc8a60ff9ba88c6b237be1835d309f98329b25644fc
BuildRequires: ncurses-devel
Requires:      ncurses-libs

%description
htop is an interactive text-mode process viewer for Linux, similar to top.

%prep
%autosetup

%build
autoreconf -vfi

%configure \
        --enable-openvz \
        --enable-vserver \
        --enable-taskstats \
        --enable-unicode \
        --enable-native-affinity \
        --enable-oom \
        --with-sensors \
        --enable-cgroup
%make_build

%install
%make_install

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README
%{_bindir}/htop
%{_datadir}/pixmaps/htop.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/applications/%{name}.desktop
%{_mandir}/man1/htop.1*

%changelog
* Fri Jun 09 2023 Nitesh Kumar <kunitesh@vmware.com> 3.2.1-2
- Bump version as a part of ncurses upgrade to v6.4
* Tue Sep 27 2022 Gerrit Photon <photon-checkins@vmware.com> 3.2.1-1
- Automatic Version Bump
* Sun May 29 2022 Gerrit Photon <photon-checkins@vmware.com> 3.2.0-1
- Automatic Version Bump
* Mon Apr 11 2022 Shivani Agarwal <shivania2@vmware.com> 3.1.2-1
- htop initial build
