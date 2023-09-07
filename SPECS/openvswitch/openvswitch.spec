%{!?python2_sitelib: %global python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %global python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        Open vSwitch daemon/database/utilities
Name:           openvswitch
Version:        2.12.0
Release:        8%{?dist}
License:        ASL 2.0 and LGPLv2+
URL:            http://www.openvswitch.org/
Group:          System Environment/Daemons
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://openvswitch.org/releases/%{name}-%{version}.tar.gz
%define sha512  openvswitch=e9bf9030a1c5dbcddcf463d332a87c84326c21fb53eac743cd999da9e03f564a394e2362fe5ab2ebec35bb456fc76e10da6910c398886b41fbd28a35465b5aee
Patch0:         openvswitch-CVE-2020-35498.patch
Patch1:         openvswitch-CVE-2020-27827.patch
Patch2:         openvswitch-CVE-2021-36980.patch
Patch3:         openvswitch-CVE-2021-3905.patch
Patch4:         openvswitch-CVE-2022-4337-CVE-2022-4338.patch
Patch5:         openvswitch-CVE-2023-1668.patch
BuildRequires:  gcc >= 4.0.0
BuildRequires:  libcap-ng
BuildRequires:  libcap-ng-devel
BuildRequires:  make
BuildRequires:  openssl
BuildRequires:  openssl-devel
BuildRequires:  systemd
BuildRequires:  python3 >= 3.4.0
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-six
BuildRequires:  python3-xml
BuildRequires:  python2
Requires:       libgcc-atomic
Requires:       libcap-ng
Requires:       openssl
Requires:       python3
Requires:       python3-libs
Requires:       python3-six
Requires:       python3-xml
Requires:       gawk

%description
Open vSwitch provides standard network bridging functions and
support for the OpenFlow protocol for remote per-flow control of
traffic.

%package -n     python-openvswitch
Summary:        python-openvswitch
Requires:       python2
Requires:       python2-libs

%description -n python-openvswitch
Python 2 openvswith bindings.

%package -n     python3-openvswitch
Summary:        python3-openvswitch
Requires:       python3
Requires:       python3-libs

%description -n python3-openvswitch
Python 3 version.

%package        devel
Summary:        Header and development files for openvswitch
Requires:       %{name} = %{version}
%description    devel
openvswitch-devel package contains header files and libs.

%package        devel-static
Summary:        Static libs for openvswitch
Requires:       %{name} = %{version}
%description    devel-static
openvswitch-devel-static package contains static libs.

%package        doc
Summary:        Documentation for openvswitch
Requires:       %{name} = %{version}-%{release}
%description    doc
It contains the documentation and manpages for openvswitch.

%package -n     ovn-common
Summary:        Common files for OVN
Requires:       %{name} = %{version}-%{release}
%description -n ovn-common
It contains the common userspace components for OVN.

%package -n     ovn-host
Summary:        Host components of OVN
Requires:       ovn-common = %{version}-%{release}
%description -n ovn-host
It contains the userspace components for OVN to be run on each hypervisor.

%package -n     ovn-central
Summary:        Central components of OVN
Requires:       ovn-common = %{version}-%{release}
%description -n ovn-central
It contains the user space components for OVN to be run on central host.

%package -n     ovn-controller-vtep
Summary:        OVN VTEP controller binaries
Requires:       ovn-common = %{version}-%{release}
%description -n ovn-controller-vtep
It contains the user space components for OVN Controller VTEP.

%package -n     ovn-docker
Summary:        OVN drivers for docker
Requires:       ovn-common = %{version}-%{release}
%description -n ovn-docker
It contains the OVN drivers for docker networking.

%package -n     ovn-doc
Summary:        Documentation for OVN
Requires:       ovn-common = %{version}-%{release}
%description -n ovn-doc
It contains the documentation and manpages for OVN.

%prep
%autosetup -p1
# AM_INIT_AUTOMAKE macro was generated using automake 1.15.1 and we are using
# different version of automake, thus, aclocal.m4 needs to be recreated
%{__aclocal}
%{__autoconf}

%build
export PYTHON2=no
%configure --enable-ssl --enable-shared
%make_build

%install
%make_install
find %{buildroot}/%{_libdir} -name '*.la' -delete
mkdir -p %{buildroot}/%{python2_sitelib}
mkdir -p %{buildroot}/%{python3_sitelib}
cp -a %{buildroot}/%{_datadir}/openvswitch/python/ovs %{buildroot}/%{python2_sitelib}
cp -a %{buildroot}/%{_datadir}/openvswitch/python/ovs %{buildroot}/%{python3_sitelib}

mkdir -p %{buildroot}/%{_libdir}/systemd/system
install -p -D -m 0644 rhel/usr_share_openvswitch_scripts_systemd_sysconfig.template %{buildroot}/%{_sysconfdir}/sysconfig/openvswitch

/usr/bin/python3 build-aux/dpdkstrip.py --nodpdk < rhel/usr_lib_systemd_system_ovs-vswitchd.service.in > rhel/usr_lib_systemd_system_ovs-vswitchd.service
for service in openvswitch ovsdb-server ovs-vswitchd ovn-controller ovn-controller-vtep ovn-northd; do
       install -p -D -m 0644 rhel/usr_lib_systemd_system_${service}.service %{buildroot}/%{_unitdir}/${service}.service
done

mkdir -p %{buildroot}/%{_sysconfdir}/openvswitch
install -p -D -m 0644 rhel/etc_openvswitch_default.conf %{buildroot}/%{_sysconfdir}/openvswitch/default.conf
sed -i '/OVS_USER_ID=.*/c\OVS_USER_ID=' %{buildroot}/%{_sysconfdir}/openvswitch/default.conf

%check
make %{_smp_mflags} -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%preun
%systemd_preun %{name}.service

%preun -n ovn-central
%systemd_preun ovn-northd.service

%preun -n ovn-host
%systemd_preun ovn-controller.service

%preun -n ovn-controller-vtep
%systemd_preun ovn-controller-vtep.service

%post
%systemd_post %{name}.service

%post -n ovn-central
%systemd_post ovn-northd.service

%post -n ovn-host
%systemd_post ovn-controller.service

%post -n ovn-controller-vtep
%systemd_post ovn-controller-vtep.service

%postun
%systemd_postun %{name}.service

%postun -n ovn-central
%systemd_postun ovn-northd.service

%postun -n ovn-host
%systemd_postun ovn-controller.service

%postun -n ovn-controller-vtep
%systemd_postun ovn-controller-vtep.service

%files
%defattr(-,root,root)
%{_bindir}/ovs-*
%{_bindir}/ovsdb-*
%{_bindir}/vtep-ctl
%{_sbindir}/ovs-*
%{_sbindir}/ovsdb-server
%{_unitdir}/openvswitch.service
%{_unitdir}/ovs-vswitchd.service
%{_unitdir}/ovsdb-server.service
%{_libdir}/lib*
%{_sysconfdir}/openvswitch/default.conf
%{_sysconfdir}/bash_completion.d/ovs-*-bashcomp.bash
%{_datadir}/openvswitch/*.ovsschema
%{_datadir}/openvswitch/python/*
%{_datadir}/openvswitch/scripts/ovs-*
%config(noreplace) %{_sysconfdir}/sysconfig/openvswitch

%files -n python-openvswitch
%{python2_sitelib}/*

%files -n python3-openvswitch
%{python3_sitelib}/*

%files devel
%{_includedir}/ovn/*.h
%{_includedir}/openflow/*.h
%{_includedir}/openvswitch/*.h
%{_libdir}/pkgconfig/*.pc

%files devel-static
%{_libdir}/*.a

%files doc
%{_mandir}/man1/ovs-*.1.gz
%{_mandir}/man1/ovsdb-*.1.gz
%{_mandir}/man5/ovs-vswitchd.conf.db.5.gz
%{_mandir}/man5/vtep.5.gz
%{_mandir}/man7/ovs-fields.7.gz
%{_mandir}/man8/ovs-*.8.gz
%{_mandir}/man8/vtep-ctl.8.gz
%{_mandir}/man5/ovsdb-server.5.gz
%{_mandir}/man7/ovs-actions.7.gz

%files -n ovn-common
%{_bindir}/ovn-nbctl
%{_bindir}/ovn-sbctl
%{_bindir}/ovn-trace
%{_bindir}/ovn-detrace
%{_datadir}/openvswitch/scripts/ovn-ctl
%{_datadir}/openvswitch/scripts/ovndb-servers.ocf

%files -n ovn-host
%{_unitdir}/ovn-controller.service
%{_bindir}/ovn-controller

%files -n ovn-central
%{_unitdir}/ovn-northd.service
%{_bindir}/ovn-northd
%{_datadir}/openvswitch/ovn-nb.ovsschema
%{_datadir}/openvswitch/ovn-sb.ovsschema

%files -n ovn-controller-vtep
%{_unitdir}/ovn-controller-vtep.service
%{_bindir}/ovn-controller-vtep

%files -n ovn-docker
%{_bindir}/ovn-docker-overlay-driver
%{_bindir}/ovn-docker-underlay-driver

%files -n ovn-doc
%{_mandir}/man1/ovn-detrace.1.gz
%{_mandir}/man7/ovn-architecture.7.gz
%{_mandir}/man8/ovn-ctl.8.gz
%{_mandir}/man8/ovn-nbctl.8.gz
%{_mandir}/man8/ovn-sbctl.8.gz
%{_mandir}/man8/ovn-controller-vtep.8.gz
%{_mandir}/man8/ovn-controller.8.gz
%{_mandir}/man5/ovn-nb.5.gz
%{_mandir}/man5/ovn-sb.5.gz
%{_mandir}/man8/ovn-northd.8.gz
%{_mandir}/man8/ovn-trace.8.gz

%changelog
*   Wed Sep 06 2023 Anmol Jain <anmolja@vmware.com> 2.12.0-8
-   Fix for CVE-2023-1668
*   Wed Jan 18 2023 Dweep Advani <dadvani@vmware.com> 2.12.0-7
-   Fixed CVE-2022-4337 and CVE-2022-4338
*   Tue Oct 18 2022 Harinadh D <hdommaraju@vmware.com> 2.12.0-6
-   fix for CVE-2021-3905
*   Tue Aug 17 2021 Dweep Advani <dadvani@vmware.com> 2.12.0-5
-   Patched for CVE-2021-36980
*   Thu Apr 01 2021 Dweep Advani <dadvani@vmware.com> 2.12.0-4
-   Patched for CVE-2020-27827
*   Thu Feb 25 2021 Dweep Advani <dadvani@vmware.com> 2.12.0-3
-   Patched for CVE-2020-35498
*   Fri Sep 18 2020 Tapas Kundu <tkundu@vmware.com> 2.12.0-2
-   Packged python bindings in right path
*   Wed Feb 05 2020 Tapas Kundu <tkundu@vmware.com> 2.12.0-1
-   Build with Python3
*   Tue Nov 13 2018 Anish Swaminathan <anishs@vmware.com> 2.8.2-3
-   Replace with configure macro
*   Wed Feb 28 2018 Vinay Kulkarni <kulkarniv@vmware.com> 2.8.2-2
-   Setup the default conf file for local ovsdb server.
*   Tue Feb 27 2018 Vinay Kulkarni <kulkarniv@vmware.com> 2.8.2-1
-   Update to OVS 2.8.2
*   Tue Oct 10 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.7.0-9
-   Fix CVE-2017-14970
*   Wed Oct 04 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.7.0-8
-   Fix CVE-2017-9263
*   Tue Sep 19 2017 Anish Swaminathan <anishs@vmware.com> 2.7.0-7
-   Add gawk to Requires
*   Tue Aug 29 2017 Sarah Choi <sarahc@vmware.com> 2.7.0-6
-   Add python2/python-six/python-xml to Requires
*   Thu Jul 13 2017 Nishant Nelogal <nnelogal@vmware.com> 2.7.0-5
-   Created OVN packages and systemd service scripts
*   Fri Jun 16 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.7.0-4
-   Fix CVE-2017-9214, CVE-2017-9265
*   Mon Jun 12 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.7.0-3
-   Fix CVE-2017-9264
*   Tue May 23 2017 Xiaolin Li <xiaolinl@vmware.com> 2.7.0-2
-   Added python and python3 subpackage.
*   Sat Apr 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.7.0-1
-   Update to 2.7.0
*   Fri Feb 10 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.6.1-2
-   Build ovs shared library
*   Wed Nov 16 2016 Vinay Kulkarni <kulkarniv@vmware.com> 2.6.1-1
-   Update to openvswitch 2.6.1
*   Sat Sep 24 2016 Vinay Kulkarni <kulkarniv@vmware.com> 2.5.0-1
-   Update to openvswitch 2.5.0
*   Fri Sep 09 2016 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.1-1
-   Update to openvswitch 2.4.1
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.4.0-3
-   GA - Bump release of all rpms
*   Sat Oct 31 2015 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.0-2
-   OVS requires libatomic.so.1 provided by gcc.
*   Mon Oct 12 2015 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.0-1
-   Update to OVS v2.4.0
*   Fri May 29 2015 Kumar Kaushik <kaushikk@vmware.com> 2.3.1-1
-   Initial build. First version
