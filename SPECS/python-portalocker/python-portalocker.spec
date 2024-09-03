Summary:        Library to provide an easy API to file locking.
Name:           python3-portalocker
Version:        2.8.2
Release:        1%{?dist}
Url:            https://pypi.org/project/portalocker
License:        BSD-3-Clause
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://files.pythonhosted.org/packages/35/00/0f230921ba852226275762ea3974b87eeca36e941a13cd691ed296d279e5/portalocker-%{version}.tar.gz
%define sha512 portalocker=9ebd6fdbc597615c5f76bf5741556d84bc95c925e931ee708b4fccbf0908e4dc4e758be659928340675675f5ca09764f5d2621fdef9195e21c1359f7764ae1dc

BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
%if 0%{?with_check}
BuildRequires:  python3-pytest
%endif

Requires:       python3

BuildArch:      noarch

Provides: python%{python3_version}dist(portalocker)

%description
Portalocker is a library to provide an easy API to file locking.
On Linux and Unix systems the locks are advisory by default.
By specifying the -o mand option to the mount command it is possible to enable mandatory file locking on Linux

%prep
%autosetup -n portalocker-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%if 0%{?with_check}
%check
rm pytest.ini
pip3 install redis tomli
%pytest portalocker_tests
%endif

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Tue Jun 18 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.8.2-1
- Initial packaging for Photon
