Name:           tuned
Version:        2.15.0
Release:        9%{?dist}
Summary:        A dynamic adaptive system tuning daemon
License:        GNU GENERAL PUBLIC LICENSE Version 2
Group:          System/Base
Url:            https://github.com/redhat-performance/tuned
Source:         tuned-%{version}.tar.gz
%define         sha512 tuned=67acdf10ecccd7910c4dcfd737610b4cb7651c7bf937bc0ed9c51869262d9f3a46f262d0b7636bc7a86a8abf579542a46f551e4f6c7561a061d8d58459be4589
Patch0:         remove_desktop_utils_dependency.patch
Patch1:         bootloader-plugin-support-for-photon.patch
Patch2:         tuned-fix-bug-in-sysctl-verify.patch
Patch3:         0001-Schedule-perf-events-iff-scheduler-per-process-confi.patch
Patch4:         0001-realtime-Modify-hung_task-detection-param.patch
Patch5:         0001-tuned-don-t-verify-irq-0-on-x86_64.patch
Patch6:         0001-plugin-bootloader-Support-for-ostree-boot.patch
Patch7:         0001-add-support-for-sched-kernel-cmdline-parameter.patch
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  python3-devel
BuildRequires:  systemd-devel
Requires:       dbus-python3
Requires:       ethtool
Requires:       gawk
Requires:       python3-configobj
Requires:       python3-decorator
Requires:       polkit
Requires:       python3-pyudev
Requires:       python3-linux-procfs
Requires:       python3-pygobject
Requires:       python3-schedutils
Requires:       python3-ethtool
Requires:       linux-python3-perf
Requires:       irqbalance
Requires:       systemd
Requires:       virt-what
%if 0%{?with_check}
BuildRequires:  curl-devel
BuildRequires:  python3-pip
BuildRequires:  python3-configobj
BuildRequires:  python3-pyudev
BuildRequires:  python3-decorator
BuildRequires:  dbus-python3
BuildRequires:  python3-pygobject
%endif
BuildArch:      noarch

%description
The tuned package contains a daemon that tunes system settings dynamically.
It does so by monitoring the usage of several system components periodically.
Based on that information components will then be put into lower or higher
power saving modes to adapt to the current usage. Currently only ethernet
network and ATA harddisk devices are implemented.

%package utils-systemtap
Summary:        Disk and net statistic monitoring systemtap scripts
Group:          System/Base
Requires:       %{name} = %{version}
Requires:       systemtap

%description utils-systemtap
This package contains several systemtap scripts to allow detailed
manual monitoring of the system. Instead of the typical IO/sec it collects
minimal, maximal and average time between operations to be able to
identify applications that behave power inefficient (many small operations
instead of fewer large ones).

%prep
%autosetup -p1

%build
#The tuned daemon is written in pure Python. Nothing requires to be built.

%install
make install DESTDIR=%{buildroot} %{?_smp_mflags}

# conditional support for grub2, grub2 is not available on all architectures
# and tuned is noarch package, thus the following hack is needed
mkdir -p %{buildroot}%{_datadir}/tuned/grub2
mv %{buildroot}%{_sysconfdir}/grub.d/00_tuned %{buildroot}%{_datadir}/tuned/grub2/00_tuned
rmdir %{buildroot}%{_sysconfdir}/grub.d
mkdir -p %{buildroot}%{_var}/lib/tuned
mkdir -p %{buildroot}%{_sysconfdir}/modprobe.d
touch %{buildroot}%{_sysconfdir}/modprobe.d/kvm.rt.tuned.conf
mkdir -p %{buildroot}%{_datadir}/dbus-1/system.d
mv %{buildroot}%{_sysconfdir}/dbus-1/system.d/com.redhat.tuned.conf %{buildroot}%{_datadir}/dbus-1/system.d/com.redhat.tuned.conf

#removing powertop2tuned as we do not have powertop for this.
rm %{buildroot}%{_bindir}/powertop2tuned

%check
pip3 install unittest2
make test %{?_smp_mflags}

%post
%systemd_post tuned.service

%preun
%systemd_preun tuned.service

%postun
%systemd_postun_with_restart tuned.service

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{python3_sitelib}/tuned
%{_sbindir}/tuned
%{_sbindir}/tuned-adm
%{_libexecdir}/tuned
%{_sysconfdir}/tuned/active_profile
%config(noreplace) %{_sysconfdir}/modprobe.d/kvm.rt.tuned.conf
%config(noreplace) %{_sysconfdir}/tuned/tuned-main.conf
%{_datadir}/dbus-1/system.d/com.redhat.tuned.conf
%config(noreplace) %{_sysconfdir}/modprobe.d/tuned.conf
%config(noreplace) /boot/tuned.cfg
%config(noreplace) %{_sysconfdir}/tuned/
%{_libdir}/tmpfiles.d
%{_unitdir}/tuned.service
%dir %{_localstatedir}/log/tuned
%dir /etc/tuned
%dir /var/lib/tuned
%{_mandir}/man5/tuned*
%{_mandir}/man8/tuned*
%{_datadir}/tuned/grub2
%{_libdir}/tuned/
%{_datadir}/doc
%exclude %{_datadir}/icons/hicolor/scalable/apps/tuned.svg
%{_datadir}/man/man7/*
%{_datadir}/polkit-1/actions/com.redhat.tuned.policy
%{_datadir}/bash-completion/completions/tuned-adm
%exclude %{_datadir}/tuned/ui/tuned-gui.glade
%exclude %{_sbindir}/tuned-gui
%exclude %{_libdir}/kernel/install.d/92-tuned.install

%files utils-systemtap
%defattr(-,root,root,-)
%doc doc/README.utils doc/README.scomes COPYING
%{_sbindir}/varnetload
%{_sbindir}/netdevstat
%{_sbindir}/diskdevstat
%{_sbindir}/scomes
%{_mandir}/man8/varnetload.*
%{_mandir}/man8/netdevstat.*
%{_mandir}/man8/diskdevstat.*
%{_mandir}/man8/scomes.*

%changelog
* Mon Sep 11 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 2.15.0-9
- Add support for the 'sched' kernel cmdline parameter
* Fri Aug 25 2023 Ankit Jain <ankitja@vmware.com> 2.15.0-8
- Enable support for ostree-boot
* Mon May 08 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 2.15.0-7
- Skip verification of irq 0 on x86
* Tue Feb 21 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 2.15.0-6
- Fix tuned daemon startup failure by moving tuned's dbus config file
- to the correct location
* Fri Jul 15 2022 Keerthana K <keerthanak@vmware.com> 2.15.0-5
- Add /var/lib/tuned folder to rpm
* Thu Jan 13 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.15.0-4
- Bump up to build with updated dbus-python3
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 2.15.0-3
- Bump up to compile with python 3.10
* Thu Nov 18 2021 Ankit Jain <ankitja@vmware.com> 2.15.0-2
- realtime: modified hung_task detection sysctl param
- to log D-state tasks
* Thu Sep 23 2021 Keerthana K <keerthanak@vmware.com> 2.15.0-1
- Update to version 2.15.0
- Schedule perf events iff scheduler per process configurations are set
* Wed Sep 08 2021 Nitesh Kumar <kunitesh@vmware.com> 2.14.0-4
- Replacement of ITS suggested words.
* Fri Oct 09 2020 svasamsetty <svasamsetty@vmware.com> 2.14.0-3
- Re-enable tuned as it was deactivated due to openssl 1.1.1
* Wed Sep 23 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.14.0-2
- Bootloader plugin support for Photon
- sysctl plugin verify bug fix
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 2.14.0-1
- Automatic Version Bump
* Wed May 13 2020 Tapas Kundu <tkundu@vmware.com> 2.13.0-2
- Replaced requires from python3-perf to linux-python3-perf.
* Wed Mar 18 2020 Tapas Kundu <tkundu@vmware.com> 2.13.0-1
- Initial release.
