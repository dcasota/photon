Summary:	Iotop is a Python program with a top like UI used to show the processes and their corresponding IO activity.
Name:		iotop
Version:	0.6
Release:	8%{?dist}
License:	GPLv2
URL:		http://guichaz.free.fr/iotop/
Group:		System/Monitoring
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://guichaz.free.fr/iotop/files/%{name}-%{version}.tar.gz
%define sha512 iotop=8ba9edcff5106534b5267fbbd8e2fc1ba79583d66e00b5271ac764ab5a0b3c48294465671b6c919d97f72db615e151b4f09b5776058731332cbb6219d97a9818
Patch0:         python3_compatibility_fix.patch
BuildRequires:  python3-devel
Requires:       python3
Requires:       python3-libs
Requires:       python3-curses

BuildArch:      noarch

%description
Iotop is a Python program with a top like UI used to show the processes and their corresponding IO activity.

%prep
%autosetup -p1

%build
%py3_build

%install
#!/bin/bash
# http://bugs.python.org/issue644744
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot} --record="INSTALLED_FILES"
# 'brp-compress' gzips the man pages without distutils knowing... fix this
sed -i -e 's@man/man\([[:digit:]]\)/\(.\+\.[[:digit:]]\)$@man/man\1/\2.gz@g' "INSTALLED_FILES"
sed -i -e 's@\(.\+\)\.py$@\1.py*@' \
       -e '/.\+\.pyc$/d' \
       "INSTALLED_FILES"
echo "%dir %{python3_sitelib}/iotop" >> INSTALLED_FILES

%clean
rm -rf %{buildroot}/*

%files -f INSTALLED_FILES
%defattr(-,root,root)
%doc COPYING NEWS THANKS
%{python3_sitelib}/*

%changelog
* Mon Nov 28 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.6-8
- Update release to compile with python 3.11
* Mon Oct 12 2020 Sharan Turlapati <sturlapati@vmware.com> 0.6-7
- Add python3-curses as Requires
* Fri Dec 06 2019 Tapas Kundu <tkundu@vmware.com> 0.6-6
- Build with python3
- Mass removal python2
* Fri Jun 16 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.6-5
- Use python2 explicitly
* Thu Jun 15 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.6-4
- Add python2 to Requires
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.6-3
- Fix arch
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.6-2
- GA - Bump release of all rpms
* Mon Nov 30 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.6-1
- Initial build.	First version
