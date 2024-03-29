Name:           python3-babel
Version:        2.10.3
Release:        3%{?dist}
Summary:        An integrated collection of utilities that assist in internationalizing and localizing Python applications
License:        BSD3
Group:          Development/Languages/Python
Url:            http://babel.pocoo.org
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://files.pythonhosted.org/packages/17/e6/ec9aa6ac3d00c383a5731cc97ed7c619d3996232c977bb8326bcbb6c687e/Babel-%{version}.tar.gz
%define sha512 Babel=72a5759d2cfa239df56f3d2809b23367b9691e21de92535b30f9b3455d253682f6c18ca919f3fb039deed2663db9276307f6343cbbab56fca96ff1ac9c214fa7

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-pytz
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

%if 0%{?with_check}
BuildRequires:  curl-devel
BuildRequires:  python3-pytest
BuildRequires:  openssl-devel
BuildRequires:  python3-six
BuildRequires:  python3-attrs
%endif

Requires:       python3
Requires:       python3-pytz

BuildArch:      noarch

%description
Babel is an integrated collection of utilities that assist in internationalizing and localizing Python applications,
with an emphasis on web-based applications.

The functionality Babel provides for internationalization (I18n) and localization (L10N) can be separated into two different aspects:
1.Tools to build and work with gettext message catalogs.
2.A Python interface to the CLDR (Common Locale Data Repository), providing access to various locale display names, localized number and date formatting, etc.

%prep
%autosetup -n Babel-%{version} -p1

%build
%py3_build

%install
%py3_install
mv %{buildroot}/%{_bindir}/pybabel %{buildroot}/%{_bindir}/pybabel3

%files
%defattr(-,root,root,-)
%{_bindir}/pybabel3
%{python3_sitelib}/*

%changelog
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.10.3-3
- Bump version as a part of openssl upgrade
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.10.3-2
- Update release to compile with python 3.11
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 2.10.3-1
- Automatic Version Bump
* Thu Oct 28 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.9.1-1
- Upgrade to v2.9.1 to fix CVE-2021-42771
* Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 2.8.0-3
- Fix build with new rpm
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.8.0-2
- openssl 1.1.1
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 2.8.0-1
- Automatic Version Bump
* Mon Jun 15 2020 Tapas Kundu <tkundu@vmware.com> 2.6.0-4
- Mass removal python2
* Tue Aug 27 2019 Shreyas B. <shreyasb@vmware.com> 2.6.0-3
- Fixed make check errors.
* Tue Nov 13 2018 Tapas Kundu <tkundu@vmware.com> 2.6.0-2
- Fixed make check errors.
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 2.6.0-1
- Update to version 2.6.0
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 2.4.0-3
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.4.0-2
- Change python to python2 and add python2 scripts to bin directory
* Tue Apr 25 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.4.0-1
- Initial
