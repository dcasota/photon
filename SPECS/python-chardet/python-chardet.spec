Summary:        A Universal Character Encoding Detector in Python
Name:           python3-chardet
Version:        5.0.0
Release:        1%{?dist}
Url:            https://pypi.org/project/chardet
License:        LGPL v2.1
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/chardet/chardet/archive/chardet-%{version}.tar.gz
%define sha512 chardet=3853248584d53d977abe0e6ab856e1526fd7360d9b94b4f08d03895da80ba9efac8882dbd3f919f0d52b0699c0d7fd68edb223c37512685976c6f2b212fbe0ff

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

%if 0%{?with_check}
BuildRequires:  python3-pytest
%endif

Requires:       python3
Requires:       python3-setuptools

BuildArch:      noarch

%description
chardet is a universal character encoding detector in Python.

%prep
%autosetup -p1 -n chardet-%{version}

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
%pytest -v
%endif

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*
%{_bindir}/chardetect

%changelog
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 5.0.0-1
- Automatic Version Bump
* Sat Dec 18 2021 Shreenidhi Shedi <sshedi@vmware.com> 4.0.0-1
- Add python3-setuptools to Requires
* Tue Jun 16 2020 Tapas Kundu <tkundu@vmware.com> 3.0.4-2
- Mass removal python2
* Thu Sep 27 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 3.0.4-1
- Initial packaging.
