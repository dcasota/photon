Summary:        Python cryptography library
Name:           python3-cryptography
Version:        41.0.3
Release:        1%{?dist}
Url:            https://pypi.python.org/pypi/cryptography
License:        ASL 2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://pypi.io/packages/source/c/cryptography/cryptography-%{version}.tar.gz
%define sha512  cryptography=84f79f72be3646c1e9a932ba8aba514471f6c0e50462a0bb3a927622ce67c7932e71d44e187db8928b05f04b803b958284f785c0dc297a0c9453846af1ac1aca

BuildRequires:  openssl-devel
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-cffi
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools-rust
BuildRequires:  python3-xml
BuildRequires:  rust
BuildRequires:  ca-certificates

%if 0%{?with_check}
BuildRequires:  python3-pip
BuildRequires:  curl-devel
BuildRequires:  python3-pytest
%endif

Requires:       openssl
Requires:       python3
Requires:       python3-libs
Requires:       python3-cffi
Requires:       python3-idna
Requires:       python3-pyasn1
Requires:       python3-six
Requires:       python3-packaging
Requires:       python3-asn1crypto

%description
Cryptography is a Python library which exposes cryptographic recipes and primitives.

%prep
%autosetup -p1 -n cryptography-%{version}

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
openssl req \
    -new \
    -newkey rsa:4096 \
    -days 365 \
    -nodes \
    -x509 \
    -subj "/C=US/ST=Denial/L=Springfield/O=Dis/CN=photon.com" \
    -keyout photon.key \
    -out photon.cert

openssl rsa -in photon.key -out photon.pem

mv photon.pem %{_sysconfdir}/ssl/certs

pip3 install pretend hypothesis iso8601 cryptography_vectors pytz

export PYTHONPATH="${PWD}"/docs/development/custom-vectors/:%{buildroot}%{python3_sitelib}
python3 -m pytest
%endif

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Tue Aug 01 2023 Prashant S Chauhan <psinghchauha@vmware.com> 41.0.3-1
- Update to v41.0.3
* Tue May 23 2023 Prashant S Chauhan <psinghchauha@vmware.com> 3.3.2-5
- Fix CVE-2023-23931
* Thu Jun 30 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.3.2-4
- FIPS 3.0.0 support
- Fix %check to make it run tests
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 3.3.2-3
- Bump up to compile with python 3.10
* Thu Jul 22 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.3.2-2
- openssl 3.0.0 support
* Tue May 18 2021 Piyush Gupta <gpiyush@vmware.com> 3.3.2-1
- Upgrade to 3.3.2, Fixes CVE-2020-36242.
* Fri Nov 06 2020 Gerrit Photon <photon-checkins@vmware.com> 3.2.1-1
- Automatic Version Bump
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.1.1-2
- openssl 1.1.1
* Tue Sep 22 2020 Gerrit Photon <photon-checkins@vmware.com> 3.1.1-1
- Automatic Version Bump
* Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 3.1-1
- Automatic Version Bump
* Wed Aug 26 2020 Gerrit Photon <photon-checkins@vmware.com> 3.0-1
- Automatic Version Bump
* Mon Jun 15 2020 Tapas Kundu <tkundu@vmware.com> 2.8-2
- Mass removal python2
* Tue Mar 03 2020 Tapas Kundu <tkundu@vmware.com> 2.8-1
- Update to version 2.8
- Fix make check
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 2.3.1-1
- Update to version 2.3.1
* Mon Aug 14 2017 Xiaolin Li <xiaolinl@vmware.com> 2.0.3-1
- Updated to version 2.0.3.
* Tue Jul 25 2017 Divya Thaluru <dthaluru@vmware.com> 1.8.1-4
- Added missing requires python-six and python-enum34
- Removed python-enum from requires
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.8.1-3
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Fri May 05 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.1-2
- Added missing requires python-enum
* Tue Apr 04 2017 Xiaolin Li <xiaolinl@vmware.com> 1.8.1-1
- Updated to version 1.8.1.
* Thu Feb 02 2017 Xiaolin Li <xiaolinl@vmware.com> 1.7.2-1
- Updated to version 1.7.2 and added python3 package.
* Mon Oct 03 2016 ChangLee <changLee@vmware.com> 1.2.3-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.3-2
- GA - Bump release of all rpms
* Mon Mar 07 2016 Anish Swaminathan <anishs@vmware.com> 1.2.3-1
- Upgrade to 1.2.3
* Fri Feb 26 2016 Anish Swaminathan <anishs@vmware.com> 1.2.2-1
- Upgrade version to 1.2.2
* Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 1.2.1-1
- Upgrade version
* Wed Nov 18 2015 Divya Thaluru <dthaluru@vmware.com> 1.1-1
- Initial packaging for Photon
