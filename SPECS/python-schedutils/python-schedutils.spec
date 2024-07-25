#
# spec file for package python3-schedutils
#

Name:           python3-schedutils
Summary:        Linux scheduler python bindings
Version:        0.6
Release:        3%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
License:        GPLv2
URL:            https://git.kernel.org/pub/scm/libs/python/python-schedutils/python-schedutils.git/
Source:         https://cdn.kernel.org/pub/software/libs/python/python-schedutils/python-schedutils-%{version}.tar.xz
%define sha512  python-schedutils=1373eb0ae7594aeaf0ffa75abeb89424208531049f93d4bd068b0cedc603380c374361c87c09bb01acd6346dfe0de654a2112321f0b9110ec103d51549b8f4d2
BuildRequires:  python3-devel
BuildRequires:  gcc

%description
Python interface for the Linux scheduler sched_{get,set}{affinity,scheduler}\
functions and friends.

%prep
%autosetup -n python-schedutils-%{version}

%build
%py3_build

%install
python3 setup.py install --skip-build --root %{buildroot}

%files
%defattr(0755,root,root,0755)
%license COPYING
%{_bindir}/pchrt
%{_bindir}/ptaskset
%{_mandir}/man1/pchrt.1*
%{_mandir}/man1/ptaskset.1*
%{python3_sitearch}/schedutils*.so
%{python3_sitearch}/*.egg-info

%changelog
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.6-3
- Update release to compile with python 3.11
* Thu May 28 2020 Shreyas B. <shreyasb@vmware.com> 0.6-2
- Remove BuildArch.
* Thu Mar 19 2020 Shreyas B. <shreyasb@vmware.com> 0.6-1
- Initial version.
