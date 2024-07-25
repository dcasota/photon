Name:           python3-hatch-vcs
Version:        0.2.0
Release:        1%{?dist}
Summary:        Hatch plugin for versioning with your preferred VCS
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/ofek/hatch-vcs
Source0:        https://files.pythonhosted.org/packages/source/h/hatch_vcs/hatch_vcs-%{version}.tar.gz
%define sha512  hatch_vcs=3eb0b04022d4801a982d90a3a0e34e59fcf7dd04c0c2db91c0306b4187ba466ac85ecbb80943a35f4a6a4912bc2ddf2633fab897e8820f5e1ee9d200147b5faf
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-packaging
BuildRequires:  python3-pathspec
BuildRequires:  python3-hatchling
BuildRequires:  python3-pluggy

Requires:       python3

%description
This provides a plugin for Hatch that uses your preferred version control system (like Git) to determine project versions.

%prep
%autosetup -n hatch_vcs-%{version}

%build
%{pyproject_wheel}

%install
%{pyproject_install}

%check
python3 setup.py test

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.2.0-1
- Initial version
