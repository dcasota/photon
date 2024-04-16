Summary:        Virtualization API library that supports KVM, QEMU, Xen, ESX etc
Name:           libvirt
Version:        4.7.0
Release:        14%{?dist}
License:        LGPL
URL:            http://libvirt.org/
Source0:        http://libvirt.org/sources/%{name}-%{version}.tar.xz
%define sha512  libvirt=a4b320460b923508d9519c65c8be18b5013eb7ed4d581984cc5edf0d3476c34f959d69ad4ca7a0e257dac91351e11718785efc3f201d4b58fa999dbca1daac47
Group:          Virtualization/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Patch0:         libvirt-CVE-2019-3840.patch
Patch1:         libvirt-CVE-2019-10166.patch
Patch2:         libvirt-CVE-2019-10167.patch
Patch3:         libvirt-CVE-2019-10168.patch
Patch4:         libvirt-4.7.0-CVE-2019-20485.patch
Patch5:         libvirt-CVE-2020-10703.patch
Patch6:         libvirt-CVE-2019-10161.patch
Patch7:         libvirt-CVE-2021-3631.patch
Patch8:         libvirt-CVE-2021-3667.patch
Patch9:         libvirt-CVE-2021-3975.patch
Patch10:        CVE-2024-2494.patch
Patch11:        CVE-2024-2496.patch
BuildRequires:  cyrus-sasl
BuildRequires:  device-mapper-devel
BuildRequires:  gnutls-devel
BuildRequires:  libxml2-devel
BuildRequires:  e2fsprogs-devel
BuildRequires:  libcap-ng-devel
BuildRequires:  libnl-devel
BuildRequires:  libselinux-devel
BuildRequires:  libssh2-devel
BuildRequires:  systemd-devel
BuildRequires:  parted
BuildRequires:  python3-devel
BuildRequires:  readline-devel
BuildRequires:  libxslt
BuildRequires:  libtirpc-devel
BuildRequires:  rpcsvc-proto-devel
Requires:       cyrus-sasl
Requires:       device-mapper
Requires:       gnutls
Requires:       libxml2
Requires:       e2fsprogs
Requires:       libcap-ng
Requires:       libnl
Requires:       libselinux
Requires:       libssh2
Requires:       systemd
Requires:       parted
Requires:       python3
Requires:       readline
Requires:       libtirpc

%description
Libvirt is collection of software that provides a convenient way to manage virtual machines and other virtualization functionality, such as storage and network interface management. These software pieces include an API library, a daemon (libvirtd), and a command line utility (virsh).  An primary goal of libvirt is to provide a single way to manage multiple different virtualization providers/hypervisors. For example, the command 'virsh list --all' can be used to list the existing virtual machines for any supported hypervisor (KVM, Xen, VMWare ESX, etc.) No need to learn the hypervisor specific tools!

%package docs
Summary:        libvirt docs
Group:          Development/Tools
%description docs
The contains libvirt package doc files.

%package devel
Summary:        libvirt devel
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}
Requires:       libtirpc-devel
%description devel
This contains development tools and libraries for libvirt.

%prep
%autosetup -p1

%build
sh configure \
    --disable-silent-rules \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --with-udev=no \
    --with-pciaccess=no

%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

%check
%make_check

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/libvirt*.so.*
%{_libdir}/libvirt/storage-file/libvirt_storage_file_fs.so
%{_libdir}/libvirt/storage-backend/*
%{_libdir}/libvirt/connection-driver/*.so
%{_libdir}/libvirt/lock-driver/*.so
%{_libdir}/sysctl.d/60-libvirtd.conf
%{_libdir}/systemd/system/*
/usr/libexec/libvirt*
%{_sbindir}/*

%config(noreplace)%{_sysconfdir}/sasl2/libvirt.conf
%config(noreplace)%{_sysconfdir}/libvirt/*.conf
%{_sysconfdir}/libvirt/nwfilter/*
%{_sysconfdir}/libvirt/qemu/*
%{_sysconfdir}/logrotate.d/*
%{_sysconfdir}/sysconfig/*
%{_bindir}/*

%files devel
%{_includedir}/libvirt/*
%{_libdir}/libvirt*.so
%{_libdir}/pkgconfig/libvirt*

%dir %{_datadir}/libvirt/api/
%{_datadir}/libvirt/api/libvirt-api.xml
%{_datadir}/libvirt/api/libvirt-admin-api.xml
%{_datadir}/libvirt/api/libvirt-qemu-api.xml
%{_datadir}/libvirt/api/libvirt-lxc-api.xml

%files docs
/usr/share/augeas/lenses/*
/usr/share/doc/%{name}-%{version}/*
/usr/share/gtk-doc/*
/usr/share/libvirt/*
/usr/share/locale/*
%{_mandir}/*

%changelog
*   Fri Apr 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 4.7.0-14
-   Fix CVE-2024-2494 and CVE-2024-2496
*   Tue Mar 26 2024 Harinadh D <harinadh.dommaraju@broadcom.com> 4.7.0-13
-   Version bump to use parted 3.5
*   Wed Jan 24 2024 Harinadh D <hdommaraju@vmware.com> 4.7.0-12
-   Version bump to use libssh2 1.11.0
*   Fri Sep 02 2022 Mukul Sikka <msikka@vmware.com> 4.7.0-11
-   Fix CVE-2021-3975
*   Mon Jul 04 2022 Mukul Sikka <msikka@vmware.com> 4.7.0-10
-   Fix CVE-2021-3631 and CVE-2021-3667
*   Sun Jun 19 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.7.0-9
-   Bump version as a part of libxslt upgrade
*   Thu Nov 18 2021 Nitesh Kumar <kunitesh@vmware.com> 4.7.0-8
-   Version bump up to use libxml2 2.9.11-4.
*   Tue Jun 09 2020 Harinadh Dommaraju <hdommaraju@vmware.com> 4.7.0-7
-   Fix CVE-2019-10161
*   Tue Jun 09 2020 Harinadh Dommaraju <hdommaraju@vmware.com> 4.7.0-6
-   Fix CVE-2020-10703
*   Thu Apr 02 2020 Harinadh Dommaraju <hdommaraju@vmware.com> 4.7.0-5
-   Fix CVE-2019-20485
*   Mon Aug 19 2019 Harinadh Dommaraju <hdommaraju@vmware.com> 4.7.0-4
-   Upgrading package to fix CVE-2019-10166, CVE-2019-10167, CVE-2019-10168
*   Tue May 28 2019 Siju Maliakkal <smaliakkal@vmware.com> 4.7.0-3
-   Fix CVE-2019-3840
*   Tue Sep 25 2018 Alexey Makhalov <amakhalov@vmware.com> 4.7.0-2
-   Use libtirpc
*   Wed Sep 12 2018 Keerthana K <keerthanak@vmware.com> 4.7.0-1
-   Update to version 4.7.0
*   Thu Dec 07 2017 Xiaolin Li <xiaolinl@vmware.com> 3.2.0-4
-   Move so files in folder connection-driver and lock-driver to main package.
*   Mon Dec 04 2017 Xiaolin Li <xiaolinl@vmware.com> 3.2.0-3
-   Fix CVE-2017-1000256
*   Wed Aug 23 2017 Rui Gu <ruig@vmware.com> 3.2.0-2
-   Fix missing deps in devel package
*   Thu Apr 06 2017 Kumar Kaushik <kaushikk@vmware.com> 3.2.0-1
-   Upgrading version to 3.2.0
*   Fri Feb 03 2017 Vinay Kulkarni <kulkarniv@vmware.com> 3.0.0-1
-   Initial version of libvirt package for Photon.
