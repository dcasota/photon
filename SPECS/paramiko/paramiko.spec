Summary:        Python SSH module
Name:           paramiko
Version:        2.7.2
Release:        3%{?dist}
License:        LGPL
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            http://www.paramiko.org/

Source0: https://github.com/paramiko/paramiko/archive/paramiko-%{version}.tar.gz
%define sha512 %{name}=c9bc569428a0a61814cb73941356de5bae7fea7891ba4fd3f5c00ff1ee5083454bfde7e969fb4aaf5254b909f7f0132f590d67803eda8a67503e5c02ec2bf01a

Patch0:         CVE-2022-24302.patch

BuildArch:      noarch

BuildRequires:  python-setuptools
BuildRequires:  python2-devel
BuildRequires:  ecdsa > 0.11
BuildRequires:  pycrypto > 2.1
BuildRequires:  python-cryptography
BuildRequires:  python3-devel
BuildRequires:  python3-ecdsa > 0.11
BuildRequires:  python3-pycrypto > 2.1
BuildRequires:  python3-cryptography
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

%if 0%{?with_check}
BuildRequires:  python3-pip
BuildRequires:  python3-bcrypt
BuildRequires:  python3-PyNaCl
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
%endif

Requires:       python2
Requires:       pycrypto > 2.1
Requires:       ecdsa > 0.11
Requires:       python-cryptography
Requires:       python-PyNaCl
Requires:       python-bcrypt

%description
"Paramiko" is a combination of the esperanto words for "paranoid" and "friend". It's a module for Python 2.6+ that implements the SSH2 protocol for secure (encrypted and authenticated) connections to remote machines. Unlike SSL (aka TLS), SSH2 protocol does not require hierarchical certificates signed by a powerful central authority.

%package -n     python3-paramiko
Summary:        python3-paramiko
Requires:       python3
Requires:       python3-pycrypto > 2.1
Requires:       python3-ecdsa > 0.11
Requires:       python3-cryptography
Requires:       python3-PyNaCl
Requires:       python3-bcrypt

%description -n python3-paramiko

Python 3 version.

%prep
%autosetup -p1

%build
python2 setup.py build
python3 setup.py build

%install
python2 setup.py install -O1 --skip-build \
    --root "%{buildroot}" \
    --single-version-externally-managed

python3 setup.py install -O1 --skip-build \
    --root "%{buildroot}" \
    --single-version-externally-managed

%check
pip3 install -r dev-requirements.txt
pytest

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%{python_sitelib}/*

%files -n python3-paramiko
%defattr(-, root, root)
%{python3_sitelib}/*

%changelog
* Tue Oct 03 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.7.2-3
- Bump version as a part of cryptography upgrade
* Wed Oct 12 2022 Shivani Agarwal <shivania2@vmware.com> 2.7.2-2
- Fix for CVE-2022-24302
* Mon Dec 14 2020 Gerrit Photon <photon-checkins@vmware.com> 2.7.2-1
- Automatic Version Bump
* Mon May 11 2020 Tapas Kundu <tkundu@vmware.com> 2.7.1-1
- Update to 2.7.1
- txt files have been moved in sitelib path.
* Thu Oct 17 2019 Tapas Kundu <tkundu@vmware.com> 2.4.3-1
- Updated to 2.4.3
* Fri Aug 23 2019 Anisha Kumari <kanisha@vmware.com> 2.4.2-3
- Added patch to update pytest version.
* Wed Mar 06 2019 Tapas Kundu <tkundu@vmware.com> 2.4.2-2
- Added bcrypt and PyNaCl to requires.
* Thu Jan 10 2019 Siju Maliakkal <smaliakkal@vmware.com> 2.4.2-1
- Upgraded to 2.4.2 to mitigate CVE-2018-1000805
* Tue Sep 11 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.4.1-1
- Update version to 2.4.1
* Mon Apr 16 2018 Xiaolin Li <xiaolinl@vmware.com> 2.1.5-1
- Update version to 2.1.5 for CVE-2018-1000132
* Tue Jul 25 2017 Divya Thaluru <dthaluru@vmware.com> 2.1.2-5
- Fixed test command
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 2.1.2-4
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.1.2-3
- Use python2 explicitly while building
* Fri May 05 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.2-2
- Added missing requires python-cryptography
* Sat Apr 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.2-1
- Update to 2.1.2
* Mon Feb 27 2017 Xiaolin Li <xiaolinl@vmware.com> 1.16.0-4
- Added python3 site-packages.
* Fri Oct 07 2016 ChangLee <changlee@vmware.com> 1.16.0-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.16.0-2
- GA - Bump release of all rpms
* Tue Jan 5 2016 Xiaolin Li <xiaolinl@vmware.com> 1.16.0-1
- Initial build.  First version
