%define container_selinux_ver   2.181.0

Summary:        SELinux policy
Name:           selinux-policy
Version:        36.5
Release:        5%{?dist}
License:        GPLv2
Group:          System Environment/Libraries
Url:            https://github.com/SELinuxProject/selinux/wiki
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/fedora-selinux/selinux-policy/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=85bf6c98b1d226019122226ca4761821c6d8b46c7c40b00b67a9279f3d1fc847ea4bdde2fddcdaa161aa577b86a495f5ad80f8736acd813ad74a366b9aeaaa89

Source1: https://github.com/containers/container-selinux/archive/container-selinux-%{container_selinux_ver}.tar.gz
%define sha512 container-selinux=8d85263599cf66b2d83e510ab75056d425ae5cd9b330c820d053e328575129ccca5320c92f29c8e0310d49b90261755567a28b93ae684f21f49698789ea6bf1b

Source2:        build.conf
Source3:        modules.conf
Source4:        macros.%{name}
Source5:        config

Patch0: contrib-container.patch
Patch1: contrib-cron.patch
Patch2: contrib-dbus.patch
Patch3: contrib-virt.patch
Patch4: kernel-storage.patch
Patch5: roles-staff.patch
Patch6: roles-unprivuser.patch
Patch7: motd_t-new-domain-for-motdgen.patch
Patch8: system-getty.patch
Patch9: system-init.patch
Patch10: system-logging.patch
Patch11: system-modutils.patch
Patch12: system-systemd.patch
Patch13: system-sysnetwork.patch
Patch14: system-udev.patch
Patch15: system-userdomain.patch
Patch16: admin_usermanage.patch
Patch17: system-fstool.patch
Patch18: iptables-allow-kernel_t-fifo_files.patch
Patch19: authlogin.if-add-transition-rules-for-shadow.patch
Patch20: allow-lvm_t-to-transit-to-unconfined_t.patch
Patch21: fix-fc-conflicts.patch
Patch22: fix-AVC-denials-based-on-package-test-results.patch
Patch23: Fix-kubernetes-denials-for-K8-deployment.patch
Patch24: Fix-bin-denials-for-K8-deployment-with-containerd.patch
Patch25: Fix-etcd-denials-for-K8-deployment-with-containerd.patch
Patch26: fix_systemd_gpt_denials.patch
Patch27: Fix-kubernetes-watch-denials-for-K8-deployment.patch

BuildArch:      noarch

BuildRequires: checkpolicy
BuildRequires: python3-devel
BuildRequires: semodule-utils
BuildRequires: libselinux-utils
BuildRequires: libselinux-devel
BuildRequires: policycoreutils

Requires: policycoreutils
Requires: coreutils-selinux

%description
Provides default Photon OS SELinux policy.

%package devel
Summary: SELinux policy devel
Requires: %{name} = %{version}-%{release}
Requires: m4
Requires: checkpolicy
Requires: selinux-python
Requires: semodule-utils
Requires: rpm-build
Requires: build-essential

%description devel
SELinux policy development

%prep
# Using autosetup is not feasible
%setup -q -b 1 -n container-selinux-%{container_selinux_ver}
# Using autosetup is not feasible
%setup -q
cp -r ../container-selinux-%{container_selinux_ver}/container.* policy/modules/contrib/
%autopatch -p1

%build
cp %{SOURCE2} .
cp %{SOURCE3} policy/
%make_build

%install
%make_install %{?_smp_mflags}
mkdir -p %{buildroot}%{_sharedstatedir}/selinux/default
# Use priority 100 instead of default 400
%make_install %{?_smp_mflags} SEMODULE="%{_sbindir}/semodule -p %{buildroot} -X 100" load
%make_install %{?_smp_mflags} install-headers
mkdir %{buildroot}%{_datadir}/selinux/devel
cp doc/Makefile.example %{buildroot}%{_datadir}/selinux/devel/Makefile
cp config/file_contexts.subs_dist %{buildroot}%{_sysconfdir}/selinux/default/contexts/files/
cp -p %{SOURCE5} %{buildroot}%{_sysconfdir}/selinux/config

mkdir -p %{buildroot}%{_rpmmacrodir}
cp -p %{SOURCE4} %{buildroot}%{_rpmmacrodir}/

rel="$(echo %{release} | sed 's/\.[^.]*$//')"
sed -i "s/SELINUXPOLICYVERSION/%{version}-${rel}/" %{buildroot}%{_rpmmacrodir}/macros.%{name}
sed -i "s@SELINUXSTOREPATH@%{_sharedstatedir}/selinux@" %{buildroot}%{_rpmmacrodir}/macros.%{name}

%posttrans
if [ $1 -ge 0 ]; then
  %{_sbindir}/setfiles %{_sysconfdir}/selinux/default/contexts/files/file_contexts /
fi

%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/selinux/
%config(noreplace) %{_sysconfdir}/selinux/config
%{_sysconfdir}/selinux/default
%{_sharedstatedir}/selinux/default
%{_sysconfdir}/selinux/default/contexts/files/file_contexts.subs_dist
%{_rpmmacrodir}/macros.%{name}

%files devel
%defattr(-,root,root,-)
%{_datadir}/selinux

%changelog
* Tue Oct 24 2023 Shreenidhi Shedi <sshedi@vmware.com> 36.5-5
- Fix devel package requires
* Fri Feb 17 2023 Shivani Agarwal <shivania2@vmware.com> 36.5-4
- Added rpm macros and selinux policy for k8's watch denial message
* Fri Sep 16 2022 Shivani Agarwal <shivania2@vmware.com> 36.5-3
- Added selinux policy for k8's deployment with containerd
* Fri Sep 16 2022 Shreenidhi Shedi <sshedi@vmware.com> 36.5-2
- Bump version and fix build failure after libsepol upgrade
* Mon Mar 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 36.5-1
- Upgrade to v36.5
* Tue Mar 22 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.14.8-4
- Fix some more AVC denials
* Wed Mar 16 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.14.8-3
- Fix passwd, shadow transitions
* Mon Mar 07 2022 Alexey Makhalov <amakhalov@vmware.com> 3.14.8-2
- Fix iptables and sshd issues
* Thu Aug 06 2020 Vikash Bansal <bvikas@vmware.com> 3.14.8-1
- Version Bump up to 3.14.8
* Thu Aug 06 2020 Vikash Bansal <bvikas@vmware.com> 3.14.6-1
- Version Bump up to 3.14.6
* Fri Jul 31 2020 Vikash Bansal <bvikas@vmware.com> 3.14.5-8
- Add support of rabbitmq module
- Fixed issue of accessing "ds-identify.log" by blkid
* Tue Jul 28 2020 Vikash Bansal <bvikas@vmware.com> 3.14.5-7
- Fix motgen "avc:denied" error and removed duplicate rules.
* Tue Jul 21 2020 Vikash Bansal <bvikas@vmware.com> 3.14.5-6
- Fix "avc:denied" errors for passwd and systemd-timesync
* Mon Jul 20 2020 Vikash Bansal <bvikas@vmware.com> 3.14.5-5
- Add support of cloudform & redis  module in modules.conf
* Wed Jul 15 2020 Vikash Bansal <bvikas@vmware.com> 3.14.5-4
- Added file_contexts.subs_dist
- This file is used to configure base path aliases
* Sun Jul 05 2020 Vikash Bansal <bvikas@vmware.com> 3.14.5-3
- Resolve "avc:  denied" errors
* Thu Jun 04 2020 Vikash Bansal <bvikas@vmware.com> 3.14.5-2
- Add coreutils-selinux in requires, needed for setting labels
* Fri Apr 24 2020 Alexey Makhalov <amakhalov@vmware.com> 3.14.5-1
- Initial build.
