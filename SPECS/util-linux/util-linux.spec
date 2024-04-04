Summary:        Utilities for file systems, consoles, partitions, and messages
Name:           util-linux
Version:        2.32.1
Release:        6%{?dist}
URL:            http://www.kernel.org/pub/linux/utils/util-linux
License:        GPLv2+
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: %{name}-%{version}.tar.xz
%define sha512 %{name}=267fedae24a874ee4dc558081f6b8d07b33b955b0635f3348f021c111c17f2e95c01b2cbf909fe13c6ca448cbcf23c658c75f72f25749aa65e99f68fabb94698

Patch0: CVE-2021-37600.patch
Patch1: 0001-chfn-Make-readline-prompt-for-each-field-on-a-separa.patch
Patch2: 0002-chsh-chfn-remove-readline-support-CVE-2022-0563.patch
Patch3: CVE-2024-28085-pre1.patch
Patch4: CVE-2024-28085-pre2.patch
Patch5: CVE-2024-28085-pre3.patch
Patch6: CVE-2024-28085.patch

BuildRequires: ncurses-devel

%if 0%{?with_check}
BuildRequires: ncurses-terminfo
%endif

Requires: %{name}-libs = %{version}-%{release}

Conflicts: toybox < 0.8.2-2

%description
Utilities for handling file systems, consoles, partitions,
and messages.

%package lang
Summary: Additional language files for util-linux
Group: Applications/System
Requires: %{name} = %{version}-%{release}

%description lang
These are the additional language files of util-linux.

%package devel
Summary: Header and library files for util-linux
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
These are the header and library files of util-linux.

%package libs
Summary: library files for util-linux
Group: Development/Libraries

%description libs
These are library files of util-linux.

%prep
%autosetup -p1
sed -i -e 's@etc/adjtime@var/lib/hwclock/adjtime@g' $(grep -rl '/etc/adjtime' .)

%build
%configure \
    --disable-nologin \
    --disable-silent-rules \
    --disable-static \
    --disable-use-tty-group \
    --without-python

%make_build

%install
install -vdm 755 %{buildroot}%{_sharedstatedir}/hwclock
%make_install %{?_smp_mflags}
chmod 644 %{buildroot}/usr/share/doc/util-linux/getopt/getopt*.tcsh
find %{buildroot} -name '*.la' -delete
%find_lang %{name}

%check
chown -Rv nobody .
sudo -u nobody -s /bin/bash -c "PATH=$PATH make -k check"
rm -rf %{buildroot}/lib/systemd/system

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%dir %{_sharedstatedir}/hwclock
%{_libdir}/libfdisk.so.*
%{_libdir}/libsmartcols.so.*
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_datadir}/bash-completion/completions/*
%{_datadir}/doc/util-linux/getopt/*

%files libs
%defattr(-,root,root)
%{_libdir}/libblkid.so.*
%{_libdir}/libmount.so.*
%{_libdir}/libuuid.so.*

%files lang -f %{name}.lang
%defattr(-,root,root)

%files devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_includedir}/*
%{_mandir}/man3/*

%changelog
* Fri Mar 22 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.32.1-6
- Fix CVE-2024-28085
* Mon Mar 21 2022 Ankit Jain <ankitja@vmware.com> 2.32.1-5
- Fixes CVE-2022-0563
* Wed Aug 11 2021 Ankit Jain <ankitja@vmware.com> 2.32.1-4
- Fixes CVE-2021-37600
* Fri Jul 03 2020 Prashant S Chauhan <psinghchauha@vmware.com> 2.32.1-3
- Do not conflict with toybox >= 0.8.2-2
* Mon May 04 2020 Sujay G <gsujay@vmware.com> 2.32.1-2
- Replaced ./configure with %configure to fix builder issue
* Tue Apr 14 2020 Ashwin H <ashwinh@vmware.com> 2.32.1-1
- Update to version 2.32.1, fix CVE-2017-2616
* Mon Apr 09 2018 Xiaolin Li <xiaolinl@vmware.com> 2.32-1
- Update to version 2.32, fix CVE-2018-7738
* Wed Dec 27 2017 Anish Swaminathan <anishs@vmware.com> 2.31.1-1
- Upgrade to version 2.31.1.
* Mon Oct 02 2017 Alexey Makhalov <amakhalov@vmware.com> 2.29.2-5
- Added conflicts toybox
* Fri Sep 15 2017 Bo Gan <ganb@vmware.com> 2.29.2-4
- Cleanup check
* Mon Jul 31 2017 Xiaolin Li <xiaolinl@vmware.com> 2.29.2-3
- Fixed rpm check errors.
* Thu Apr 20 2017 Alexey Makhalov <amakhalov@vmware.com> 2.29.2-2
- Added -libs subpackage to strip docker image.
* Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 2.29.2-1
- Updated to version 2.29.2.
* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 2.27.1-5
- Moved man3 to devel subpackage.
* Thu Nov 17 2016 Alexey Makhalov <amakhalov@vmware.com> 2.27.1-4
- Disable use tty droup
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 2.27.1-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.27.1-2
- GA - Bump release of all rpms
* Fri Dec 11 2015 Anish Swaminathan <anishs@vmware.com> 2.27.1-1
- Upgrade version.
* Tue Oct 6 2015 Xiaolin Li <xiaolinl@vmware.com> 2.24.1-3
- Disable static, move header files, .so and config files to devel package.
* Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 2.24.1-2
- Update according to UsrMove.
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.24.1-1
- Initial build. First version
