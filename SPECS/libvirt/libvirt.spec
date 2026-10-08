%global build_if %{photon_subrelease} >= 92

# The systemd units, grouped by what an upgrade does to them (as upstream's
# libvirt.spec does): the daemons restart, virtlockd and virtlogd re-exec on
# reload to keep the locks and logs of running guests, and libvirt-guests and
# the one-shot units are left alone. %%install fails if this list and the units
# meson installs ever differ.
%global libvirt_restart_units libvirtd.service virtproxyd.service virtlxcd.service virtnetworkd.service virtnwfilterd.service virtsecretd.service virtstoraged.service virtvboxd.service
%global libvirt_reload_units virtlockd.service virtlogd.service
%global libvirt_socket_units libvirtd.socket libvirtd-ro.socket libvirtd-admin.socket libvirtd-tcp.socket libvirtd-tls.socket virtproxyd.socket virtproxyd-ro.socket virtproxyd-admin.socket virtproxyd-tcp.socket virtproxyd-tls.socket virtlxcd.socket virtlxcd-ro.socket virtlxcd-admin.socket virtnetworkd.socket virtnetworkd-ro.socket virtnetworkd-admin.socket virtnwfilterd.socket virtnwfilterd-ro.socket virtnwfilterd-admin.socket virtsecretd.socket virtsecretd-ro.socket virtsecretd-admin.socket virtstoraged.socket virtstoraged-ro.socket virtstoraged-admin.socket virtvboxd.socket virtvboxd-ro.socket virtvboxd-admin.socket virtlockd.socket virtlockd-admin.socket virtlogd.socket virtlogd-admin.socket
%global libvirt_other_units libvirt-guests.service virt-secret-init-encryption.service virt-guest-shutdown.target
%global libvirt_units %{libvirt_socket_units} %{libvirt_restart_units} %{libvirt_reload_units} %{libvirt_other_units}

# Seconds the erase may spend destroying the active virtual networks before
# the units stop (worst case, independent of the number of networks): one
# net-destroy stops a dnsmasq and removes a bridge and its firewall rules,
# well under a second each, so 60 s only bounds a daemon that does not answer.
%global libvirt_net_teardown_timeout 60

Summary:        Virtualization API library that supports KVM, QEMU, Xen, ESX etc
Name:           libvirt
Version:        12.6.0
Release:        2%{?dist}
URL:            http://libvirt.org
Group:          Virtualization/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://libvirt.org/sources/%{name}-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}

Source2: %{name}.sysusers.conf

BuildRequires:  audit-devel
BuildRequires:  json-c-devel
BuildRequires:  cyrus-sasl-devel
BuildRequires:  curl-devel
BuildRequires:  c-ares-devel
BuildRequires:  device-mapper-devel
BuildRequires:  e2fsprogs-devel
BuildRequires:  gnutls-devel
BuildRequires:  libcap-ng-devel
BuildRequires:  libnl-devel
BuildRequires:  libselinux-devel
BuildRequires:  libssh2-devel
BuildRequires:  libtirpc-devel
BuildRequires:  libpcap-devel
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
BuildRequires:  lvm2
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  parted-devel
BuildRequires:  python3-devel
BuildRequires:  python3-docutils
BuildRequires:  readline-devel
BuildRequires:  systemd-devel
BuildRequires:  wireshark-devel

Requires:       cyrus-sasl
Requires:       device-mapper
Requires:       e2fsprogs
Requires:       gnutls
Requires:       libcap-ng
Requires:       libnl
Requires:       libpcap
Requires:       libselinux
Requires:       libssh2 >= 1.11.0
Requires:       libtirpc
Requires:       libxml2
Requires:       lvm2
Requires:       parted
Requires:       python3
Requires:       readline
Requires:       systemd
# the network driver runs dnsmasq for every virtual network
Requires:       dnsmasq
# the daemons read the host's SMBIOS data with dmidecode
Requires:       dmidecode
# libvirt-guests.sh sources gettext.sh
Requires:       gettext
Requires(pre):  shadow
Requires(post):   systemd
Requires(preun):  systemd
# timeout bounds the network teardown on erase
Requires(preun):  coreutils
Requires(postun): systemd
Requires(posttrans): systemd

%description
Libvirt is collection of software that provides a convenient way to manage
virtual machines and other virtualization functionality, such as storage
and network interface management. These software pieces include an API library,
a daemon (libvirtd), and a command line utility (virsh). An primary goal of
libvirt is to provide a single way to manage multiple different virtualization
providers/hypervisors. For example, the command 'virsh list --all' can be used
to list the existing virtual machines for any supported hypervisor
(KVM, Xen, VMWare ESX, etc.) No need to learn the hypervisor specific tools.

%package        devel
Summary:        libvirt devel
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}
Requires:       libtirpc-devel

%description    devel
This contains development tools and libraries for libvirt.

%package        docs
Summary:        libvirt docs
Group:          Development/Tools

Requires:      %{name} = %{version}-%{release}
Conflicts:     %{name} < 8.10.0-3

%description    docs
The contains libvirt package doc files.

%package ssh-proxy
Summary: Libvirt SSH proxy
Requires: %{name} = %{version}-%{release}

%description ssh-proxy
Allows SSH into domains via VSOCK without need for network.

%prep
%autosetup -p1

sed -i '/rst2man/d' meson.build

%build
CONFIGURE_OPTS=(
    -Dsysusersdir=%{_sysusersdir} \
    -Dlibiscsi=disabled \
    -Dnbdkit=disabled \
    -Dnbdkit_config_default=disabled \
    -Dapparmor=disabled \
    -Dapparmor_profiles=disabled \
    -Dsecdriver_apparmor=disabled \
    -Dbash_completion=disabled \
    -Daudit=enabled \
    -Dcapng=enabled \
    -Dcurl=enabled \
    -Ddocs=disabled \
    -Ddriver_bhyve=disabled \
    -Ddriver_esx=enabled \
    -Ddriver_interface=disabled \
    -Ddriver_libvirtd=enabled \
    -Ddriver_hyperv=disabled \
    -Ddriver_ch=disabled \
    -Ddriver_qemu=disabled \
    -Ddriver_libxl=disabled \
    -Ddriver_network=enabled \
    -Ddriver_vmware=enabled \
    -Ddriver_vz=disabled \
    -Ddtrace=disabled \
    -Dfuse=disabled \
    -Dfirewalld=disabled \
    -Dfirewalld_zone=disabled \
    -Dglusterfs=disabled \
    -Dinit_script=systemd \
    -Dlibnl=enabled \
    -Dlibpcap=enabled \
    -Dlibssh=disabled \
    -Dnss=disabled \
    -Dnumactl=disabled \
    -Dnumad=disabled \
    -Dsasl=enabled \
    -Dnetcf=disabled \
    -Dnumactl=disabled \
    -Dopenwsman=disabled \
    -Dpciaccess=disabled \
    -Dsanlock=disabled \
    -Dpm_utils=disabled \
    -Dpolkit=enabled \
    -Dremote_default_mode=legacy \
    -Drpath=disabled \
    -Dpciaccess=disabled \
    -Dselinux=enabled \
    -Dstorage_iscsi=disabled \
    -Dstorage_iscsi_direct=disabled \
    -Dlibiscsi=disabled \
    -Dstorage_gluster=disabled \
    -Dstorage_rbd=disabled \
    -Dstorage_zfs=disabled \
    -Dlibiscsi=disabled \
    -Dstorage_fs=enabled \
    -Dudev=disabled \
    -Dwireshark_dissector=disabled \
    -Dattr=disabled \
    )

%meson "${CONFIGURE_OPTS[@]}"
%meson_build

%install
%{meson_install}
install -p -D -m 0644 %{SOURCE2} %{buildroot}%{_sysusersdir}/%{name}.conf

# the scriptlets must handle exactly the units meson installed
built_units=$(cd %{buildroot}%{_unitdir} && ls -1 *.service *.socket *.target | sort)
listed_units=$(printf '%s\n' %{libvirt_units} | sort)
if [ "${built_units}" != "${listed_units}" ]; then
  echo "systemd units installed but not in libvirt_units, or listed but not installed:"
  printf '%s\n' ${built_units} ${listed_units} | sort | uniq -u
  exit 1
fi

%if 0%{?with_check}
%check
%meson_test
%endif

%clean
rm -rf %{buildroot}/*

%pre
%sysusers_create_compat %{SOURCE2}

%post
/sbin/ldconfig
%systemd_post %{libvirt_units}

%preun
if [ $1 -eq 0 ] && [ -d /run/systemd/system ]; then
  # A virtual network outlives the daemon that started it (KillMode=process):
  # stopping the units below would leave its bridge, its firewall rules and
  # its dnsmasq running from deleted files. Destroy the active networks
  # first, through the daemon that manages them.
  active_networks=0
  for status in %{_rundir}/%{name}/network/*.xml; do
    [ -e "${status}" ] && active_networks=1
    break
  done
  if [ ${active_networks} -eq 1 ]; then
    # One deadline for the whole teardown, whatever the number of networks:
    # a wedged daemon must not hang the erase.
    deadline=$(( $(date +%%s) + %{libvirt_net_teardown_timeout} ))
    warn() {
      echo "libvirt: $*" >&2
      echo "$*" | systemd-cat -t libvirt-erase -p warning || :
    }
    bounded() {
      left=$(( deadline - $(date +%%s) ))
      if [ ${left} -le 0 ]; then
        warn "network teardown exceeded %{libvirt_net_teardown_timeout} s, skipped: $*"
        return 1
      fi
      timeout ${left} "$@"
    }
    if systemctl -q is-active libvirtd.service; then
      uri='network:///system?mode=legacy'
    else
      uri='network:///system?mode=direct'
      bounded systemctl start virtnetworkd.service || warn "could not start virtnetworkd.service"
    fi
    networks=$(bounded virsh -q -c "${uri}" net-list --name) || warn "could not list the active networks through ${uri}"
    printf '%%s\n' "${networks}" | while IFS= read -r net; do
      [ -n "${net}" ] || continue
      bounded virsh -q -c "${uri}" net-destroy "${net}" || warn "could not destroy network ${net}; its bridge and dnsmasq may remain"
    done
  fi
fi
%systemd_preun %{libvirt_units}

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] && [ -d /run/systemd/system ]; then
  systemctl daemon-reload || :
fi

%posttrans
# After an install or upgrade, restart what runs: the daemons would otherwise
# keep running the replaced binaries. Done here, like upstream's libvirt.spec,
# so that it does not depend on the scriptlets of the version upgraded from.
if [ -d /run/systemd/system ]; then
  systemctl daemon-reload || :
  systemctl try-restart %{libvirt_restart_units} || :
  systemctl try-reload-or-restart %{libvirt_reload_units} || :
fi

%files
%defattr(-,root,root)
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/%{name}*.so.*
%{_libdir}/%{name}/connection-driver/*
%{_libdir}/%{name}/lock-driver/lockd.so
%{_libdir}/%{name}/storage-backend/*
%{_libdir}/sysctl.d/60-libvirtd.conf
%{_unitdir}/*.service
%{_unitdir}/*.socket
%{_unitdir}/*.target
%dir %attr(0755, root, root) %{_unitdir}/libvirtd.service.d/
%{_unitdir}/libvirtd.service.d/10-secret.conf
%dir %attr(0700, root, root) %{_sysconfdir}/%{name}/secrets/
%dir %attr(0700, root, root) %{_sharedstatedir}/%{name}/secrets/
%ghost %dir %attr(0700, root, root) %{_rundir}/%{name}/secrets/
%{_libexecdir}/%{name}*
%exclude %{_libexecdir}/%{name}-ssh-proxy
%{_libexecdir}/virt-login-shell-helper
# libvirt rewrites the filters and the default network (it adds their UUIDs)
# when it loads them: an upgrade must keep those files, or the daemon restarted
# after it finds the running network under another UUID
%dir %{_sysconfdir}/%{name}/nwfilter
%config(noreplace) %{_sysconfdir}/%{name}/nwfilter/*.xml
%{_sysconfdir}/%{name}/qemu/networks/autostart/default.xml
%config(noreplace) %{_sysconfdir}/%{name}/qemu/networks/default.xml
%{_sysconfdir}/logrotate.d/*
%{_sysusersdir}/%{name}*.conf

%config(noreplace)%{_sysconfdir}/%{name}/*.conf
%config(noreplace)%{_sysconfdir}/sasl2/%{name}.conf

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/*
%{_libdir}/%{name}*.so
%{_libdir}/pkgconfig/%{name}*

%files ssh-proxy
%config(noreplace) %{_sysconfdir}/ssh/ssh_config.d/30-%{name}-ssh-proxy.conf
%{_libexecdir}/%{name}-ssh-proxy

%files docs
%defattr(-,root,root)
%{_docdir}/%{name}/*
%{_datadir}/locale/*
%{_datadir}/%{name}/test-screenshot.png
%{_datadir}/%{name}/schemas/*.rng
%{_datadir}/augeas/*
%{_datadir}/%{name}/cpu_map/*
%{_datadir}/polkit-1/*

%changelog
* Sat Oct 03 2026 Daniel Casota <dcasota@gmail.com> 12.6.0-2
- Require dnsmasq, dmidecode, gettext; add systemd scriptlets
* Thu Aug 20 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 12.6.0-1
- Upgrade to v12.6.0
- Remove rpcsvc-proto dependency
* Sat Aug 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 9.3.0-19
- Extend to build for 91 and above
* Mon Aug 03 2026 Mukul Sikka <mukul.sikka@broadcom.com> 9.3.0-18
- Patched for CVE-2025-13193
* Wed Jun 03 2026 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 9.3.0-17
- Release version bump as part of libxml2/libxslt
* Mon Jun 01 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 9.3.0-16
- Release bump to rebuild against wireshark 4.6.6
* Sat May 16 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 9.3.0-15
- Extended to build for subrelease 91 and above
* Tue May 05 2026 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 9.3.0-14
- Version bump due to gnutls update
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 9.3.0-13
- Bump version as a part of python3.14 upgrade
* Sat Aug 16 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 9.3.0-12
- Fix requires on doc sub package
* Wed Jan 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 9.3.0-11
- Bump version as a part of meson upgrade
* Wed Dec 11 2024 Ajay Kaher <ajay.kaher@broadcom.com> 9.3.0-10
- Release bump for SRP compliance
* Tue Sep 03 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 9.3.0-9
- Version bump up to consume wireshark v4.2.7
* Thu Jun 06 2024 Mukul Sikka <mukul.sikka@broadcom.com> 9.3.0-8
- Fix CVE-2024-1441
* Mon May 13 2024 Mukul Sikka <mukul.sikka@broadcom.com> 9.3.0-7
- Fix CVE-2024-4418
* Fri Apr 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 9.3.0-6
- Fix CVE-2024-2494 and CVE-2024-2496
* Mon Apr 01 2024 Anmol Jain <anmol.jain@broadcom.com> 9.3.0-5
- Bump version as a part of wireshark upgrade
* Wed Nov 29 2023 Shreenidhi Shedi <sshedi@vmware.com> 9.3.0-4
- Bump version as a part of gnutls upgrade
* Thu Sep 07 2023 Harinadh D <hdommaraju@vmware.com> 9.3.0-3
- version bump to use libssh2 1.11.0
* Mon Jul 24 2023 Mukul Sikka <msikka@vmware.com> 9.3.0-2
- Fix CVE-2023-3750
* Tue Jun 06 2023 Mukul Sikka <msikka@vmware.com> 9.3.0-1
- Version upgrade to v9.3.0
* Fri Jun 02 2023 Shreenidhi Shedi <sshedi@vmware.com> 8.10.0-3
- Move doc files to docs sub package
* Thu May 25 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 8.10.0-2
- Bump version as a part of libxml2 upgrade
* Sat Jan 07 2023 Susant Sahani <ssahani@vmware.com> 8.10.0-1
- Version Bump
* Tue Dec 20 2022 Guruswamy Basavaiah <bguruswamy@vmware.com> 8.8.0-4
- Bump release as a part of readline upgrade
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 8.8.0-3
- Update release to compile with python 3.11
* Sun Nov 13 2022 Shreenidhi Shedi <sshedi@vmware.com> 8.8.0-2
- Bump version as a part of libtirpc upgrade
* Thu Nov 03 2022 Nitesh Kumar <kunitesh@vmware.com> 8.8.0-1
- Version upgrade to v8.8.0
* Fri Oct 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 8.2.0-4
- Bump version as a part of libxslt upgrade
* Tue Aug 30 2022 Shreenidhi Shedi <sshedi@vmware.com> 8.2.0-3
- Bump version as a part of gnutls upgrade
* Thu Jun 16 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 8.2.0-2
- Bump version as a part of libxslt upgrade
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 8.2.0-1
- Automatic Version Bump
* Thu Mar 17 2022 Nitesh Kumar <kunitesh@vmware.com> 7.10.0-2
- Version Bump up to consume original python files from python-docutils
* Thu Dec 02 2021 Susant Sahani <ssahani@vmware.com> 7.10.0-1
- Version Bump
* Wed Nov 17 2021 Nitesh Kumar <kunitesh@vmware.com> 7.5.0-2
- Release bump up to use libxml2 2.9.12-1.
* Wed Jul 14 2021 Susant Sahani <ssahani@vmware.com> 7.5.0-1
- Version Bump and switch to meson
* Mon May 03 2021 Gerrit Photon <photon-checkins@vmware.com> 7.3.0-1
- Automatic Version Bump
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 7.2.0-1
- Automatic Version Bump
* Fri Mar 19 2021 Susat Sahani <ssahani@vmware.com> 7.1.0-1
- Bump up version
* Wed Aug 19 2020 Harinadh Dommaraju <hdommaraju@vmware.com> 4.7.0-4
- fix CVE-2019-10166, CVE-2019-10167, CVE-2019-10168,
- CVE-2019-3840,CVE-2019-20485,CVE-2020-10703
* Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 4.7.0-3
- Build with python3
- Mass removal python2
* Tue Sep 25 2018 Alexey Makhalov <amakhalov@vmware.com> 4.7.0-2
- Use libtirpc
* Wed Sep 12 2018 Keerthana K <keerthanak@vmware.com> 4.7.0-1
- Update to version 4.7.0
* Thu Dec 07 2017 Xiaolin Li <xiaolinl@vmware.com> 3.2.0-4
- Move so files in folder connection-driver and lock-driver to main package.
* Mon Dec 04 2017 Xiaolin Li <xiaolinl@vmware.com> 3.2.0-3
- Fix CVE-2017-1000256
* Wed Aug 23 2017 Rui Gu <ruig@vmware.com> 3.2.0-2
- Fix missing deps in devel package
* Thu Apr 06 2017 Kumar Kaushik <kaushikk@vmware.com> 3.2.0-1
- Upgrading version to 3.2.0
* Fri Feb 03 2017 Vinay Kulkarni <kulkarniv@vmware.com> 3.0.0-1
- Initial version of libvirt package for Photon.
