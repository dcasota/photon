Summary:        Monitoring plugins are used to monitor status of hosts and services on the network
Name:           monitoring-plugins
Version:        2.3.1
Release:        2%{?dist}
License:        GPL-3.0
Group:          Development/Tools
URL:            https://github.com/%{name}
Source0:        https://github.com/%{name}/%{name}/archive/refs/tags/%{name}-%{version}
%define sha512 monitoring-plugins=6cf51c86d72e49b6ff5e7de65ecf20fff546870ee24469c37a08bfc2f5461ebcfb69af2d84ff7e15d5590ae107ebba3ee2d32c5bab9895033bba3f1689209f0c
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  make
BuildRequires:  m4
BuildRequires:  which
BuildRequires:  net-snmp-perl
BuildRequires:  lm-sensors
Requires:       net-snmp-perl

%description
Monitoring plugins maintains a bundle of more than 50 standard plugins.
Typically, the monitoring software runs these plugins to determine the
current status of hosts and services on your network. Each plugin is a
stand alone command line tool that provides a specific type to check.

%prep
%autosetup -n %{name}-%{version}
bash tools/setup
%configure

%build
make %{?_smp_mflags}

%install
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_prefix}/libexec
%{_prefix}/share/locale/fr
%{_prefix}/share/locale/de

%changelog
* Thu Dec 08 2022 Dweep Advani <dadvani@vmware.com> 2.3.1-2
- Rebuild for perl version upgrade to 5.36.0
* Tue May 11 2021 Sharan Turlapati <sturlapati@vmware.com> 2.3.1-1
- Initial version of monitoring-plugins for Photon
