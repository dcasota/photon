Summary:        The GnuTLS Transport Layer Security Library
Name:           gnutls
Version:        3.6.16
Release:        7%{?dist}
License:        GPLv3+ and LGPLv2+
URL:            http://www.gnutls.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://www.gnupg.org/ftp/gcrypt/gnutls/v3.6/%{name}-%{version}.tar.xz
%define sha512 %{name}=72c78d7fcb024393c1d15f2a1856608ae4460ba43cc5bbbb4c29b80508cae6cb822df4638029de2363437d110187e0a3cc19a7288c3b2f44b2f648399a028438

Patch0: default-priority.patch
Patch1: CVE-2021-4209.patch
Patch2: CVE-2022-2509.patch
Patch3: CVE-2023-0361-1.patch
Patch4: CVE-2023-0361-2.patch
Patch5: CVE-2023-5981.patch
Patch6: CVE-2024-0553.patch
Patch7: CVE-2024-0567.patch
Patch8: CVE-2024-28834.patch

BuildRequires:  nettle-devel
BuildRequires:  autogen-libopts-devel
BuildRequires:  libtasn1-devel
BuildRequires:  ca-certificates
BuildRequires:  openssl-devel
BuildRequires:  guile-devel
BuildRequires:  gc-devel

Requires:       nettle >= 3.4.1
Requires:       autogen-libopts
Requires:       libtasn1
Requires:       openssl
Requires:       ca-certificates
Requires:       gmp
Requires:       guile
Requires:       gc

%description
GnuTLS is a secure communications library implementing the SSL, TLS and DTLS protocols and technologies around them. It provides a simple C language application programming interface (API) to access the secure communications protocols as well as APIs to parse and write X.509, PKCS #12, OpenPGP and other required structures. It is aimed to be portable and efficient with focus on security and interoperability.

%package devel
Summary:    Development libraries and header files for gnutls
Requires:   %{name} = %{version}-%{release}
Requires:   libtasn1-devel
Requires:   nettle-devel >= 3.4.1

%description devel
The package contains libraries and header files for
developing applications that use gnutls.

%prep
%autosetup -p1

%build
# check for trust store file presence
[ -f %{_sysconfdir}/pki/tls/certs/ca-bundle.crt ] || exit 1

%configure \
    --without-p11-kit \
    --disable-openssl-compatibility \
    --with-included-unistring \
    --with-system-priority-file=%{_sysconfdir}/gnutls/default-priorities \
    --with-default-trust-store-file=%{_sysconfdir}/pki/tls/certs/ca-bundle.crt

%make_build

%install
%make_install %{?_smp_mflags}
rm %{buildroot}%{_infodir}/*
find %{buildroot}%{_libdir} -name '*.la' -delete
mkdir -p %{buildroot}/etc/%{name}
chmod 755 %{buildroot}/etc/%{name}

cat > %{buildroot}/etc/%{name}/default-priorities << "EOF"
SYSTEM=NONE:!VERS-SSL3.0:!VERS-TLS1.0:+VERS-TLS1.1:+VERS-TLS1.2:+AES-128-CBC:+RSA:+SHA1:+COMP-NULL
EOF

%check
%make_build check

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/locale/*
%{_docdir}/gnutls/*.png
%{_libdir}/guile/2.0/extensions/*.so*
%{_libdir}/guile/2.0/site-ccache/gnutls*
%{_datadir}/guile/site/2.0/gnutls*
%config(noreplace) %{_sysconfdir}/gnutls/default-priorities

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*

%changelog
* Wed Apr 03 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 3.6.16-7
- Fix CVE-2024-28834
* Mon Jan 22 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 3.6.16-6
- Fix CVE-2024-0553 and CVE-2024-0567
* Fri Dec 01 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.6.16-5
- Fix CVE-2023-5981
* Fri Feb 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.6.16-4
- Fix CVE-2023-0361
* Tue Aug 30 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.6.16-3
- Fix CVE-2021-4209 & CVE-2022-2509
* Wed Apr 27 2022 Susant Sahani <ssahani@vmware.com> 3.6.16-2
- Disabled fips-140 mode.
* Tue Apr 05 2022 Susant Sahani <ssahani@vmware.com> 3.6.16-1
- Version bump
* Thu May 20 2021 Prashant S Chauhan <psinghchauha@vmware.com> 3.6.15-3
- Fix CVE-2021-20232
* Sat Apr 17 2021 Shreenidhi Shedi <sshedi@vmware.com> 3.6.15-2
- Bump version as a part of nettle upgrade
* Thu Sep 24 2020 Shreenidhi Shedi <sshedi@vmware.com> 3.6.15-1
- Upgrade to version 3.6.15, fixes CVE-2020-24659
* Tue Jun 09 2020 Tapas Kundu <tkundu@vmware.com> 3.6.14-1
- Update to 3.6.14
- Fix CVE-2020-13777
* Fri Apr 10 2020 Tapas Kundu <tkundu@vmware.com> 3.6.13-1
- Update to 3.6.13
- Fix CVE-2020-11501
* Thu Oct 24 2019 Shreenidhi Shedi <sshedi@vmware.com> 3.6.9-2
- Added default priority patch.
* Thu Oct 17 2019 Shreenidhi Shedi <sshedi@vmware.com> 3.6.9-1
- Upgrade to version 3.6.9
* Mon Apr 15 2019 Keerthana K <keerthanak@vmware.com> 3.6.3-3
- Fix CVE-2019-3829, CVE-2019-3836
* Wed Oct 03 2018 Tapas Kundu <tkundu@vmware.com> 3.6.3-2
- Including default-priority in the RPM packaging.
* Thu Sep 06 2018 Anish Swaminathan <anishs@vmware.com> 3.6.3-1
- Update version to 3.6.3
* Fri Feb 09 2018 Xiaolin Li <xiaolinl@vmware.com> 3.5.15-2
- Add default_priority.patch.
* Tue Oct 10 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.5.15-1
- Update to 3.5.15. Fixes CVE-2017-7507
* Thu Apr 13 2017 Danut Moraru <dmoraru@vmware.com> 3.5.10-1
- Update to version 3.5.10
* Sun Dec 18 2016 Alexey Makhalov <amakhalov@vmware.com> 3.4.11-4
- configure to use default trust store file
* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 3.4.11-3
- Moved man3 to devel subpackage.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.4.11-2
- GA - Bump release of all rpms
* Wed Apr 27 2016 Xiaolin Li <xiaolinl@vmware.com> 3.4.11-1
- Updated to version 3.4.11
* Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 3.4.9-1
- Updated to version 3.4.9
* Thu Jan 14 2016 Xiaolin Li <xiaolinl@vmware.com> 3.4.8-1
- Updated to version 3.4.8
* Wed Dec 09 2015 Anish Swaminathan <anishs@vmware.com> 3.4.2-3
- Edit post script.
* Fri Oct 9 2015 Xiaolin Li <xiaolinl@vmware.com> 3.4.2-2
- Removing la files from packages.
* Thu Jun 18 2015 Divya Thaluru <dthaluru@vmware.com> 3.4.2-1
- Initial build. First version
