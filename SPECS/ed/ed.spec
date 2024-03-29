Summary:        Ed - A line-oriented text editor
Name:           ed
Version:        1.19
Release:        1%{?dist}
URL:            https://www.gnu.org/software/ed/
License:        GPLv3
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://fossies.org/linux/privat/%{name}-%{version}.tar.gz
%define sha512  ed=5d515db9710ec485e5f4b727052a5237bdf7efcfd2efaee0ce8ff4f0b970dbfa444820d39fb86b3393cc342fab64f0ecc9c2e5572f63dc84adf17dca33a8fa1b
%description
Ed - A line-oriented text editor

%prep
%autosetup -p1

%build
sh configure --prefix=/usr CC=%{_host}-gcc
make V=1 %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
install -vdm 755 %{buildroot}%{_lib}

%check
make  %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/ed
%{_bindir}/red
%{_infodir}/*
%exclude %{_datadir}/info/dir
%{_mandir}/man1/*

%changelog
*   Tue May 23 2023 Siju Maliakal <smaliakkal@vmware.com> 1.19-1
-   Upgrading to latest version for CVE-2017-5357
*   Fri Jun 18 2021 Nitesh Kumar <kunitesh@vmware.com> 1.4-2
-   Removed devel Package
*   Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 1.4-1
-   Automatic Version Bump
*   Wed Jul 15 2020 Gerrit Photon <photon-checkins@vmware.com> 1.16-1
-   Automatic Version Bump
*   Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 1.14.2-2
-   Cross compilation support
*   Thu Sep 27 2018 Sujay G <gsujay@vmware.com> 1.14.2-1
-   Initial build.
