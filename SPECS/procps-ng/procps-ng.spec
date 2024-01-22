Summary:        Programs for monitoring processes
Name:           procps-ng
Version:        3.3.17
Release:        2%{?dist}
License:        GPLv2
URL:            https://sourceforge.net/projects/procps-ng
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://sourceforge.net/projects/procps-ng/files/Production/%{name}-%{version}.tar.xz
%define sha512  %{name}=59e9a5013430fd9da508c4655d58375dc32e025bb502bb28fb9a92a48e4f2838b3355e92b4648f7384b2050064d17079bf4595d889822ebb5030006bc154a1a7

Patch0:         CVE-2023-4016.patch

BuildRequires:  ncurses-devel

Requires:       ncurses

Conflicts:      toybox < 0.8.2-2

%description
The Procps package contains programs for monitoring processes.

%package    devel
Summary:    Header and development files for procps-ng
Requires:   %{name} = %{version}

%description    devel
It contains the libraries and header files to create applications

%package lang
Summary:    Additional language files for procps-ng
Group:      Applications/Databases
Requires:   %{name} = %{version}-%{release}

%description lang
These are the additional language files of procps-ng

%prep
%autosetup -p1 -n procps-%{version}

%build
if [ %{_host} != %{_build} ]; then
  export ac_cv_func_malloc_0_nonnull=yes
  export ac_cv_func_realloc_0_nonnull=yes
fi

%configure --docdir=%{_defaultdocdir}/%{name}-%{version} \
           --disable-static \
           --disable-kill \
           --disable-silent-rules

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
install -vdm 755 %{buildroot}%{_bindir}
install -vdm 755 %{buildroot}%{_lib}
ln -sfv ../..%{_lib}/$(readlink %{buildroot}%{_libdir}/libprocps.so) %{buildroot}%{_libdir}/libprocps.so
install -vdm 755 %{buildroot}%{_sbindir}
ln -sfv %{_bindir}/pidof %{buildroot}%{_sbindir}/pidof
find %{buildroot} -name '*.la' -delete
%find_lang %{name}

%check
make %{?_smp_mflags} check

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%{_bindir}/ps
%{_bindir}/pidof
%{_bindir}/free
%{_bindir}/w
%{_bindir}/pgrep
%{_bindir}/uptime
%{_bindir}/vmstat
%{_bindir}/pmap
%{_bindir}/tload
%{_bindir}/pwdx
%{_bindir}/top
%{_bindir}/slabtop
%{_bindir}/watch
%{_bindir}/pkill
%{_bindir}/pwait
%{_sbindir}/sysctl
%{_sbindir}/pidof
%_datadir/locale/*
%{_docdir}/procps-ng-*/*
%{_mandir}/man8/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_libdir}/libprocps.so.*

%files devel
%{_includedir}/proc/sig.h
%{_includedir}/proc/wchan.h
%{_includedir}/proc/version.h
%{_includedir}/proc/pwcache.h
%{_includedir}/proc/procps.h
%{_includedir}/proc/devname.h
%{_includedir}/proc/sysinfo.h
%{_includedir}/proc/readproc.h
%{_includedir}/proc/escape.h
%{_includedir}/proc/slab.h
%{_includedir}/proc/alloc.h
%{_includedir}/proc/whattime.h
%{_includedir}/proc/numa.h
%{_libdir}/pkgconfig/libprocps.pc
%{_libdir}/libprocps.so
%{_mandir}/man3/*

%exclude %{_mandir}/pl/*
%exclude %{_mandir}/pt_BR/*
%exclude %{_mandir}/sv/*
%exclude %{_mandir}/uk/*
%exclude %{_mandir}/de/*
%exclude %{_mandir}/fr/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
* Tue Jan 16 2024 Srish Srinivasan <srish.srinivasan@broadcom.com> 3.3.17-2
- Patched CVE-2023-4016
* Mon Dec 06 2021 Shreenidhi Shedi <sshedi@vmware.com> 3.3.17-1
- Fix file packaging paths
* Tue Jun 30 2020 Gerrit Photon <photon-checkins@vmware.com> 3.3.16-1
- Automatic Version Bump
* Thu Apr 16 2020 Alexey Makhalov <amakhalov@vmware.com> 3.3.15-3
- Do not conflict with toybox >= 0.8.2-2
* Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 3.3.15-2
- Cross compilation support
* Fri Aug 10 2018 Tapas Kundu <tkundu@vmware.com> 3.3.15-1
- Upgrade version to 3.3.15.
- Fix for CVE-2018-1122 CVE-2018-1123 CVE-2018-1124 CVE-2018-1125
- Fix for CVE-2018-1126
* Mon Oct 02 2017 Alexey Makhalov <amakhalov@vmware.com> 3.3.12-3
- Added conflicts toybox
* Tue May 02 2017 Anish Swaminathan <anishs@vmware.com> 3.3.12-2
- Add lang package.
* Mon Apr 03 2017 Rongrong Qiu <rqiu@vmware.com> 3.3.12-1
- Upgrade to 3.3.12
* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 3.3.11-5
- Moved man3 to devel subpackage.
* Mon Oct 03 2016 ChangLee <changLee@vmware.com> 3.3.11-4
- Modified %check
* Tue Jun 21 2016 Divya Thaluru <dthaluru@vmware.com> 3.3.11-3
- Added patch to interpret ASCII sequence correctly
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.3.11-2
- GA - Bump release of all rpms
* Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 3.3.11-1
- Upgrade version
* Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 3.3.9-2
- Update according to UsrMove.
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.3.9-1
- Initial build. First version
