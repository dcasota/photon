Summary:    Versatile resource statistics tool
Name:       dool
Version:    1.2.0
Release:    1%{?dist}
License:    GPLv2
URL:        https://github.com/scottchiefbaker/dool
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution:  Photon

Source0: https://github.com/scottchiefbaker/dool/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=b194ea4ac735f93d494c6c227270867e728f55602d787db2e5a0d7997ddf74662eefd3fb549429400349f5f36a4c86a398389afca0d931d6e1f79e67dedfd670

%if 0%{?with_check}
BuildRequires: python3
BuildRequires: python3-curses
%endif

Requires: python3
Requires: python3-curses

Provides: dstat = %{version}-%{release}
Obsoletes: dstat <= 0.7.4

%description
Dstat gives you detailed selective information in columns and clearly
indicates in what magnitude and unit the output is displayed.
Less confusion, less mistakes. And most importantly, it makes it very
easy to write plugins to collect your own counters and extend in ways
you never expected.

%prep
%autosetup -p1

%install
%make_install %{?_smp_mflags}

ln -sv %{name} %{buildroot}%{_bindir}/dstat

%if 0%{?with_check}
%check
export PATH=$PATH:%{buildroot}%{_bindir}
dool --version
dool -taf 1 3
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,0755)
%doc %{_mandir}/*
%{_bindir}/%{name}
%{_bindir}/dstat
%{_datadir}/%{name}/

%changelog
* Fri Jul 28 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.2.0-1
- Initial version.
