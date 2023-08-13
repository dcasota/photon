%define sourcever 3350500
Summary:        A portable, high level programming interface to various calling conventions
Name:           sqlite
Version:        3.35.5
Release:        2%{?dist}
License:        Public Domain
URL:            http://www.sqlite.org
Group:          System Environment/GeneralLibraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://sqlite.org/2020/%{name}-autoconf-%{sourcever}.tar.gz
%define sha512  sqlite=039af796f79fc4517be0bd5ba37886264d49da309e234ae6fccdb488ef0109ed2b917fc3e6c1fc7224dff4f736824c653aaf8f0a37550c5ebc14d035cb8ac737
Patch0:         CVE-2021-31239.patch
Obsoletes:      sqlite-autoconf
Obsoletes:      sqlite-devel <= 3.27.2-5
Requires:       sqlite-libs = %{version}-%{release}
Provides:       sqlite3

%description
This package contains most of the static files that comprise the
www.sqlite.org website including all of the SQL Syntax and the
C/C++ interface specs and other miscellaneous documentation.

%package devel
Summary:        sqlite3 link library & header files
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
%description    devel
The sqlite devel package include the needed library link and
header files for development.

%package libs
Summary:        sqlite3 library
Group:          Libraries
Provides:       pkgconfig(sqlite3)
Obsoletes:      libsqlite
Obsoletes:      sqlite-autoconf
%description libs
The sqlite3 library.

%prep
%autosetup -p1 -n %{name}-autoconf-%{sourcever}

%build
%configure \
    CFLAGS="%{optflags}               \
    -DSQLITE_ENABLE_FTS3=1            \
    -DSQLITE_ENABLE_COLUMN_METADATA=1 \
    -DSQLITE_ENABLE_UNLOCK_NOTIFY=1   \
    -DSQLITE_SECURE_DELETE=1"         \
    CXXFLAGS="%{optflags}"            \
    --disable-static
make %{?_smp_mflags}

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install %{?_smp_mflags}
install -D -m644 sqlite3.1 %{buildroot}/%{_mandir}/man1/sqlite3.1
find %{buildroot}/%{_libdir} -name '*.la' -delete
rm -rf %{buildroot}/%{_infodir}
%{_fixperms} %{buildroot}/*

%check
make %{?_smp_mflags} check

%post libs
/sbin/ldconfig

%postun libs
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/*
%{_libdir}/libsqlite3.so
%{_includedir}/*

%files libs
%defattr(-,root,root)
%{_libdir}/libsqlite3.so.0.8.6
%{_libdir}/libsqlite3.so.0

%changelog
* Thu Aug 10 2023 Siju Maliakkal <smaliakkal@vmware.com> 3.35.5-2
- Apply patch to fix CVE-2021-31239
* Mon Apr 19 2021 Siju Maliakkal <smaliakkal@vmware.com> 3.35.5-1
- Upgrade to latest to mitigate CVE-2021-20227
* Fri Jul 03 2020 Shreyas B <shreyasb@vmware.com> 3.32.1-2
- Fix for CVE-2020-15358
* Thu May 28 2020 Siju Maliakkal <smaliakkal@vmware.com> 3.32.1-1
- Upgrade to 3.32.1 for following CVEs
- CVE-2020-13630 CVE-2020-13434 CVE-2020-13435 CVE-2020-13631 CVE-2020-13632
* Thu May 14 2020 Ankit Jain <ankitja@vmware.com> 3.31.1-4
- Macros defined need to be inside CFLAGS, else it was unused
- Certain symbols were undefined
* Wed Apr 15 2020 Siju Maliakkal <smaliakkal@vmware.com> 3.31.1-3
- Fix for CVE-2020-9327
* Mon Apr 13 2020 Ankit Jain <ankitja@vmware.com> 3.31.1-2
- Fix for CVE-2020-11656
* Mon Feb 3 2020 Siju Maliakkal <smaliakkal@vmware.com> 3.31.1-1
- Upgrade to 3.31.1 for following CVEs
- CVE-2019-19959 CVE-2019-19926 CVE-2019-19925 CVE-2019-19923 CVE-2019-19244
* Mon Jan 06 2020 Ankit Jain <ankitja@vmware.com> 3.30.1-1
- Upgrade to version 3.30.1
* Wed Oct 23 2019 Michelle Wang <michellew@vmware.com> 3.27.2-6
- Move libsqlite3.so* from devel to libs
* Fri Oct 18 2019 Michelle Wang <michellew@vmware.com> 3.27.2-5
- Fix patch CVE-2019-16168.patch
* Mon Sep 16 2019 Michelle Wang <michellew@vmware.com> 3.27.2-4
- Add patch CVE-2019-16168.patch
* Wed Jun 5 2019 Michelle Wang <michellew@vmware.com> 3.27.2-3
- Add patch CVE-2019-8457.
* Thu Apr 25 2019 Michelle Wang <michellew@vmware.com> 3.27.2-2
- Add patch CVE-2019-9937.
* Mon Apr 15 2019 Michelle Wang <michellew@vmware.com> 3.27.2-1
- Upgrade to 3.27.2 and add patch CVE-2019-9936.
* Sun Feb 3 2019 Michelle Wang <michellew@vmware.com> 3.26.0-1
- Upgrade to 3.26.0 for a critical Vulnerability named 'Magallan'.
* Fri Sep 21 2018 Srinidhi Rao <srinidhir@vmware.com> 3.25.1-1
- Upgrade to version 3.25.1
* Tue Feb 20 2018 Xiaolin Li <xiaolinl@vmware.com> 3.22.0-1
- Upgrade to version 3.22.0
* Fri Nov 10 2017 Xiaolin Li <xiaolinl@vmware.com> 3.21.0-1
- Upgrade to version 3.21.0
* Fri Jul 14 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.19.3-1
- Upgrading to version 3.19.0 and adding patch for CVE-2017-10989
* Thu Jun 29 2017 Divya Thaluru <dthaluru@vmware.com> 3.18.0-2
- Added obseletes for deprecated sqlite-autoconf package
* Fri Apr 7 2017 Alexey Makhalov <amakhalov@vmware.com> 3.18.0-1
- Version update
- Package rename: sqlite-autoconf -> sqlite
* Wed Nov 16 2016 Alexey Makhalov <amakhalov@vmware.com> 3.11.0-4
- Added -devel and -libs subpackages
* Tue Oct 04 2016 ChangLee <changlee@vmware.com> 3.11.0-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.11.0-2
- GA - Bump release of all rpms
* Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 3.11.0-1
- Updated to version 3.11.0
* Wed Feb 03 2016 Anish Swaminathan <anishs@vmware.com> - 3.8.3.1-2
- Fix versioning
* Tue Oct 7 2014 Divya Thaluru <dthaluru@vmware.com> 3080301-1
- Initial build. First version
