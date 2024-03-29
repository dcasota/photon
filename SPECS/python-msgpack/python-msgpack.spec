Summary:        MessagePack (de)serializer.
Name:           python3-msgpack
Version:        1.0.4
Release:        2%{?dist}
License:        Apache Software License
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            http://msgpack.org/
Source0:        https://pypi.io/packages/source/m/msgpack-python/msgpack-%{version}.tar.gz
%define sha512  msgpack=dcd59bf77408acf7171bdcc46c4d6bf875d36e80b216b7721544855e6c2b20be469415ee768b2195e74fe4650621ee6bfaa7897e709ac0d8d59cdb30772cb90b

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3

%description
MessagePack is a fast, compact binary serialization format, suitable for similar data to JSON. This package provides CPython bindings for reading and writing MessagePack data.

%prep
%autosetup -n msgpack-%{version}

%build
%py3_build

%install
%py3_install

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.0.4-2
- Update release to compile with python 3.11
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 1.0.4-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.0.0-1
- Automatic Version Bump
* Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 0.5.6-2
- Mass removal python2
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.5.6-1
- Update to version 0.5.6
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.4.8-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu May 25 2017 Xiaolin Li <xiaolinl@vmware.com> 0.4.8-1
- Initial version
