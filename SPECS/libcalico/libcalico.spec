Summary:        Library for interacting with Calico data model.
Name:           libcalico
Version:        0.19.0
Release:        7%{?dist}
License:        Apache-2.0
URL:            https://github.com/projectcalico/libcalico
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        %{name}-%{version}.tar.gz
%define sha512 %{name}=f38c850720b635c09fbc32f9be4830531f3cd47f77b1084f3150765d84f7e3ba5d135b7389fd4528c4f78593376907c1e5f7ac7eecfbea3d83bdf3c7d8134edf

BuildRequires:  git
BuildRequires:  libffi-devel
BuildRequires:  openssl-devel
BuildRequires:  procps-ng
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-asn1crypto
BuildRequires:  python3-backports.ssl_match_hostname
BuildRequires:  python3-ConcurrentLogHandler
BuildRequires:  python3-cffi
BuildRequires:  python3-pycryptodome
BuildRequires:  python3-cryptography
BuildRequires:  python3-dnspython
BuildRequires:  python3-docopt
BuildRequires:  python3-etcd
BuildRequires:  python3-idna
BuildRequires:  python3-ipaddress
BuildRequires:  python3-netaddr
BuildRequires:  python3-ndg-httpsclient
BuildRequires:  python3-pyOpenSSL
BuildRequires:  python3-pip
BuildRequires:  python3-prettytable
BuildRequires:  python3-prometheus_client
BuildRequires:  python3-pyasn1
BuildRequires:  python3-pycparser
BuildRequires:  python3-pyinstaller
BuildRequires:  python3-PyYAML
BuildRequires:  python3-requests
BuildRequires:  python3-setuptools
BuildRequires:  python3-simplejson
BuildRequires:  python3-six
BuildRequires:  python3-subprocess32
BuildRequires:  python3-urllib3
BuildRequires:  python3-websocket-client
BuildRequires:  python3-appdirs
BuildRequires:  python3-virtualenv
BuildRequires:  python3

Requires:       python3
Requires:       python3-libs
Requires:       python3-setuptools

%define debug_package %{nil}

%description
Library for interacting with Calico data model.

%prep
%autosetup -p1

%build
%py3_build

%install
%py3_install

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Tue Aug 01 2023 Prashant S Chauhan <psingchauha@vmware.com> 0.19.0-7
- Bump up to compile with latest python3-cryptography
* Mon Jan 03 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.19.0-6
- Replace deprecated pycrypto with pycryptodome
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 0.19.0-5
- Bump up to compile with python 3.10
* Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 0.19.0-4
- Fix build with new rpm
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.19.0-3
- openssl 1.1.1
* Mon Jun 15 2020 Tapas Kundu <tkundu@vmware.com> 0.19.0-2
- Mass removal python2
* Wed Aug 23 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.19.0-1
- libcalico for PhotonOS.
