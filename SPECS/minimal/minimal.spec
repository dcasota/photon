Name:           minimal
Summary:        Metapackage to install minimal profile
Version:        4.0
Release:        1%{?dist}
License:        Apache 2.0
Group:          System Environment/Base
URL:            https://vmware.github.io/photon
Vendor:         VMware, Inc.
Distribution:   Photon

# Keep this list alphabetically sorted
Requires: bc
Requires: bridge-utils
Requires: bzip2
Requires: cloud-init
Requires: cpio
Requires: cracklib-dicts
Requires: dbus
Requires: docker
Requires: e2fsprogs
Requires: file
Requires: filesystem
Requires: findutils
Requires: gdbm
Requires: grep
Requires: grub2-efi-image
Requires: grub2-theme
Requires: gzip
Requires: iana-etc
Requires: iproute2
Requires: iptables
Requires: iputils
Requires: Linux-PAM
Requires: motd
Requires: net-tools
Requires: openssh
Requires: open-vm-tools-gosc
Requires: photon-release
Requires: photon-repos
Requires: procps-ng
Requires: python3
Requires: rpm-plugin-systemd-inhibit
Requires: rpm
Requires: sed
Requires: systemd-pam
Requires: systemd-rpm-macros
Requires: systemd
Requires: systemd-udev
Requires: tdnf
Requires: tzdata
Requires: util-linux
Requires: vim
Requires: which

%description
Metapackage to install minimal profile

%prep

%build

%files
%defattr(-,root,root,0755)

%changelog
* Sun May 28 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.0-1
- Set version to major version of photon
* Mon Jul 18 2022 <okurth@vmware.com> 0.1-7
- Remove pkg-config and libtool
* Wed Oct 20 2021 Shreenidhi Shedi <sshedi@vmware.com> 0.1-6
- Add rpm-plugin-systemd-inhibit
* Thu Oct 14 2021 Shreenidhi Shedi <sshedi@vmware.com> 0.1-5
- Add open-vm-tools avilable for all platforms
* Mon Aug 17 2020 Susant Sahani <ssahani@vmware.com> 0.1-4
- Add systemd packages, sort requires packages in alphabetical order
* Thu Mar 12 2020 Alexey Makhalov <amakhalov@vmware.com> 0.1-3
- Add grub2 packages
* Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 0.1-2
- Add open-vm-tools as requires only for x86_64
* Tue Oct 30 2018 Anish Swaminathan <anishs@vmware.com> 0.1-1
- Initial packaging
