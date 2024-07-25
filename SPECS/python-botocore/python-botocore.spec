Summary:        Amazon Web Services Library.
Name:           python3-botocore
Version:        1.27.56
Release:        2%{?dist}
License:        Apache 2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/boto/botocore
Source0:        https://github.com/boto/botocore/archive/botocore-%{version}.tar.gz
%define sha512  botocore=cbbb95ee5ba0381e6c12c6ee72224976c6618fd7a645a0fa8de60308e1682e5fe37d4bbc49b8c61dffa7482479596ad24df350554eb6a46e63ec8ac8957bfb47
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:  python3-pip
BuildRequires:  python3-dateutil
BuildRequires:  python3-urllib3
%endif
Requires:       python3
Requires:       python3-libs
Requires:       python3-jmespath
Requires:       python3-dateutil
Requires:       python3-urllib3
BuildArch:      noarch
Provides:       python%{python3_version}dist(botocore)

%description
A low-level interface to a growing number of Amazon Web Services. The botocore package is the foundation for the AWS CLI as well as boto3.

%prep
%autosetup -n botocore-%{version}

%build
%py3_build

%install
%py3_install

%check
pip3 install nose
pip3 install mock
pip3 install jmespath
nosetests tests/unit

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.27.56-2
- Update release to compile with python 3.11
*   Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 1.27.56-1
-   Automatic Version Bump
*   Wed Jul 21 2021 Tapas Kundu <tkundu@vmware.com> 1.21.3-1
-   Update to 1.21.3
*   Fri Nov 06 2020 Gerrit Photon <photon-checkins@vmware.com> 1.19.13-1
-   Automatic Version Bump
*   Tue Sep 29 2020 Gerrit Photon <photon-checkins@vmware.com> 1.18.10-1
-   Automatic Version Bump
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 1.18.5-1
-   Automatic Version Bump
*   Thu Sep 10 2020 Gerrit Photon <photon-checkins@vmware.com> 1.17.59-1
-   Automatic Version Bump
*   Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 1.17.58-1
-   Automatic Version Bump
*   Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 1.17.53-1
-   Automatic Version Bump
*   Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 1.17.49-1
-   Automatic Version Bump
*   Tue Aug 11 2020 Gerrit Photon <photon-checkins@vmware.com> 1.17.41-1
-   Automatic Version Bump
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.17.28-1
-   Automatic Version Bump
*   Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 1.12.0-3
-   Mass removal python2
*   Mon Jan 14 2019 Tapas Kundu <tkundu@vmware.com> 1.12.0-2
-   Fix make check
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 1.12.0-1
-   Update to version 1.12.0
*   Sun Jan 07 2018 Kumar Kaushik <kaushikk@vmware.com> 1.8.15-1
-   Initial packaging for photon.
