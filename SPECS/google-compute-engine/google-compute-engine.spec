%define debug_package %{nil}

Summary:        Package for Google Compute Engine Linux images
Name:           google-compute-engine
Version:        20191210
Release:        3%{?dist}
License:        Apache License 2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/GoogleCloudPlatform/compute-image-packages/
Source0:        https://github.com/GoogleCloudPlatform/compute-image-packages/archive/compute-image-packages-%{version}.tar.gz
%define sha512  compute-image-packages=107f4076cecf1d6501dd37d752fdae5836f8b843351ffdf1832e445f9b35a1cc653fceffcb21fb33788629a3c53ae280939dbc559bbee0d5987270ee19ac5fd4
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-setuptools
Requires:       python3-libs
Requires:       python3-boto
Requires:       python3-distro
Obsoletes:      google-daemon
BuildArch:      noarch

%description
Collection of packages installed on Google supported Compute Engine images.

%package -n     google-compute-engine-services
Summary:        Service files for compute engine package
#Requires:      %{name}=%{version}-%{release}

%description -n google-compute-engine-services
Collection of service files for packages installed on Google supported Compute Engine images.

%prep
%autosetup -n compute-image-packages-%{version}

%build
cd packages/python-google-compute-engine
%py3_build

%install
cd packages/python-google-compute-engine
%py3_install
install -d %{buildroot}%{_libdir}/systemd/system
cd ../..
cp packages/google-compute-engine/src/lib/systemd/system/*.service %{buildroot}%{_libdir}/systemd/system

%post -n google-compute-engine-services
systemctl stop --no-block google-accounts-daemon
systemctl stop --no-block google-clock-skew-daemon
systemctl stop --no-block google-network-daemon

systemctl enable google-accounts-daemon.service
systemctl enable google-clock-skew-daemon.service
systemctl enable google-instance-setup.service
systemctl enable google-network-daemon.service
systemctl enable google-shutdown-scripts.service
systemctl enable google-startup-scripts.service

systemctl start --no-block google-accounts-daemon
systemctl start --no-block google-clock-skew-daemon
systemctl start --no-block google-network-daemon

%postun -n google-compute-engine-services
systemctl stop --no-block google-accounts-daemon
systemctl stop --no-block google-clock-skew-daemon
systemctl stop --no-block google-network-daemon

systemctl --no-reload disable google-accounts-daemon.service
systemctl --no-reload disable google-clock-skew-daemon.service
systemctl --no-reload disable google-instance-setup.service
systemctl --no-reload disable google-network-daemon.service
systemctl --no-reload disable google-shutdown-scripts.service
systemctl --no-reload disable google-startup-scripts.service

%files
%defattr(-,root,root)
%{_bindir}/google_accounts_daemon
%{_bindir}/google_clock_skew_daemon
%{_bindir}/google_instance_setup
%{_bindir}/google_metadata_script_runner
%{_bindir}/google_network_daemon
%{python3_sitelib}/*

%files -n google-compute-engine-services
%defattr(-,root,root)
%{_libdir}/systemd/system/*.service

%changelog
* Mon Nov 28 2022 Prashant S Chauhan <psinghchauha@vmware.com> 20191210-3
- Update release to compile with python 3.11
* Mon Nov 02 2020 Prashant S Chauhan <psinghchauhau@vmware.com> 20191210-2
- Add python3-distro as requires
* Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 20191210-1
- Automatic Version Bump
* Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 20180905-2
- Mass removal python2
* Wed Sep 12 2018 Anish Swaminathan <anishs@vmware.com>  20180905-1
- Upgrade to 20180905
* Wed Aug 23 2017 Anish Swaminathan <anishs@vmware.com> 20170426-3
- Remove boto configuration from instance setup
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 20170426-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Fri Apr 28 2017 Anish Swaminathan <anishs@vmware.com> 20170426-1
- Initial packaging for Photon
