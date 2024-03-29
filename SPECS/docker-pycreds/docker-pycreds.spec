Name:           docker-pycreds3
Version:        0.4.0
Release:        2%{?dist}
Summary:        Python API for docker credentials store
License:        ASL2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/shin-/dockerpy-creds

Source0: https://github.com/shin-/dockerpy-creds/archive/refs/tags/docker-pycreds-%{version}.tar.gz
%define sha512 docker-pycreds=ca5f68ef2405cc57c0b54224d4f8199c9a4c9217d78f627bffeb950998b09a69b608d1e365cac6859661346fd078c3d081828bb4ff2e18bf7a9384451ae2225a

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if 0%{?with_check}
BuildRequires:  python3-pytest
%endif

Requires:       python3

BuildArch:      noarch

%description
Python API for docker credentials store

%prep
%autosetup -p1 -n docker-pycreds-%{version}

%build
%py3_build

%install
%py3_install

%clean
rm -rf %{buildroot}

%if 0%{?with_check}
%check
%pytest
%endif

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.4.0-2
- Update release to compile with python 3.11
* Thu Oct 15 2020 Ashwin H <ashwinh@vmware.com> 0.4.0-1
- Upgrade to 0.4.0 release.
* Thu Jun 18 2020 Tapas Kundu <tkundu@vmware.com> 0.3.0-2
- Mass removal python2
* Tue Sep 04 2018 Tapas Kundu <tkundu@vmware.com> 0.3.0-1
- Upgraded to 0.3.0 version
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.2.1-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Sun Jun 04 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.2.1-1
- Initial version of docker-pycreds for PhotonOS.
