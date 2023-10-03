Summary:        An asynchronous networking framework written in Python
Name:           python-Twisted
Version:        19.10.0
Release:        5%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://twistedmatrix.com

Source0: https://pypi.python.org/packages/source/T/Twisted/Twisted-%{version}.tar.bz2
%define sha512 Twisted=de8d7fd0b2081cebeff68b060c8469377011648bc563a94a993d3530fb007ed42c3a54925c9a10c465ee7a3065cc9108ace12d10d358223fab13494becb9ac4b

Patch0:         extra_dependency.patch
Patch1:         no_packet.patch
Patch2:         CVE-2020-10108_10109.patch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-incremental
BuildRequires:  python-zope.interface
BuildRequires:  python-cryptography
BuildRequires:  python-pyOpenSSL
BuildRequires:  python-six
BuildRequires:  python-xml

BuildRequires:  python3-devel
BuildRequires:  python3-incremental
BuildRequires:  python3-zope.interface
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

%if 0%{?with_check}
BuildRequires:  net-tools
BuildRequires:  sudo
BuildRequires:  shadow
BuildRequires:  curl-devel
BuildRequires:  python3-pip
%endif

Requires:       python2
Requires:       python-zope.interface
Requires:       python-netaddr
Requires:       python-incremental
Requires:       python-constantly
Requires:       python-hyperlink
Requires:       python-attrs
Requires:       python-PyHamcrest
Requires:       python-service_identity >= 18.1.0

%description
Twisted is an event-driven networking engine written in Python and licensed under the open source ​MIT license. Twisted runs on Python 2 and an ever growing subset also works with Python 3.

Twisted also supports many common network protocols, including SMTP, POP3, IMAP, SSHv2, and DNS.

%package -n     python3-Twisted
Summary:        python-Twisted
Requires:       python3
Requires:       python3-zope.interface
Requires:       python3-netaddr
Requires:       python3-incremental
Requires:       python3-constantly
Requires:       python3-hyperlink
Requires:       python3-attrs
Requires:       python3-PyHamcrest
Requires:       python3-service_identity >= 18.1.0

%description -n python3-Twisted
Python 3 version.

%prep
%autosetup -p1 -n Twisted-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
mv %{buildroot}%{_bindir}/twistd %{buildroot}%{_bindir}/twistd3
mv %{buildroot}%{_bindir}/trial %{buildroot}%{_bindir}/trial3
mv %{buildroot}%{_bindir}/tkconch %{buildroot}%{_bindir}/tkconch3
mv %{buildroot}%{_bindir}/pyhtmlizer %{buildroot}%{_bindir}/pyhtmlizer3
mv %{buildroot}%{_bindir}/twist %{buildroot}%{_bindir}/twist3
mv %{buildroot}%{_bindir}/conch %{buildroot}%{_bindir}/conch3
mv %{buildroot}%{_bindir}/ckeygen %{buildroot}%{_bindir}/ckeygen3
mv %{buildroot}%{_bindir}/cftp %{buildroot}%{_bindir}/cftp3
popd
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
route add -net 224.0.0.0 netmask 240.0.0.0 dev lo
useradd test -G root -m
pushd ../p3dir
pip3 install --upgrade tox
chmod g+w . -R
LANG=en_US.UTF-8 tox -e py36-alldeps-nocov
popd

%files
%defattr(-,root,root)
%{python_sitelib}/*
%{_bindir}/twistd
%{_bindir}/trial
%{_bindir}/tkconch
%{_bindir}/pyhtmlizer
%{_bindir}/twist
%{_bindir}/mailmail
%{_bindir}/conch
%{_bindir}/ckeygen
%{_bindir}/cftp

%files -n python3-Twisted
%defattr(-,root,root)
%{python3_sitelib}/*
%{_bindir}/twistd3
%{_bindir}/trial3
%{_bindir}/tkconch3
%{_bindir}/pyhtmlizer3
%{_bindir}/twist3
%{_bindir}/conch3
%{_bindir}/ckeygen3
%{_bindir}/cftp3

%changelog
* Tue Oct 03 2023 Shreenidhi Shedi <sshedi@vmware.com> 19.10.0-5
- Bump version as a part of cryptography upgrade
* Sat Jun 27 2020 Tapas Kundu <tkundu@vmware.com> 19.10.0-4
- Address CVE-2020-10108 and CVE-2020-10109
* Mon Jun 01 2020 Tapas Kundu <tkundu@vmware.com> 19.10.0-3
- Requires service_identity
* Wed Mar 04 2020 Tapas Kundu <tkundu@vmware.com> 19.10.0-2
- Fix make check
* Mon Nov 18 2019 Tapas Kundu <tkundu@vmware.com> 19.10.0-1
- Updated to 19.10.0 release
* Fri Aug 30 2019 Tapas Kundu <tkundu@vmware.com> 18.7.0-3
- Added requires as PyHamcrest
* Tue Oct 30 2018 Tapas Kundu <tkundu@vmware.com> 18.7.0-2
- Moved build requires from subpackage
- Added attrs package in requires.
* Thu Sep 13 2018 Tapas Kundu <tkundu@vmware.com> 18.7.0-1
- Upgraded to release 18.7.0
* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 17.5.0-3
- Remove BuildArch
* Mon Sep 11 2017 Dheeraj Shetty <dheerajs@vmware.com> 17.5.0-2
- Added python-automat, python-hyperlink and its python3 version to the
- requires.
* Tue Aug 29 2017 Dheeraj Shetty <dheerajs@vmware.com> 17.5.0-1
- Upgrade version
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 17.1.0-6
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 17.1.0-5
- Adding python3 scripts to bin directory
* Tue May 09 2017 Rongrong Qiu <rqiu@vmware.com> 17.1.0-4
- Added python-constantly to the requires.
* Mon Mar 27 2017 Xiaolin Li <xiaolinl@vmware.com> 17.1.0-3
- Added python-netaddr and python-incremental to the requires.
* Thu Mar 23 2017 Xiaolin Li <xiaolinl@vmware.com> 17.1.0-2
- Change requires
* Wed Mar 01 2017 Xiaolin Li <xiaolinl@vmware.com> 17.1.0-1
- Added python3 package and updated to version 17.1.0.
* Mon Oct 10 2016 ChangLee <changlee@vmware.com> 15.5.0-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 15.5.0-2
- GA - Bump release of all rpms
* Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 15.5.0-1
- Upgrade version
* Tue Oct 27 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial packaging for Photon
