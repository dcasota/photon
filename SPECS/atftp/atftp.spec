Summary:          Advanced Trivial File Transfer Protocol (ATFTP) - TFTP server
Name:             atftp
Version:          0.7.5
Release:          2%{?dist}
URL:              http://sourceforge.net/projects/atftp
License:          GPLv2+ and GPLv3+ and LGPLv2+
Group:            System Environment/Daemons
Vendor:           VMware, Inc.
Distribution:     Photon

Source0: http://sourceforge.net/projects/%{name}/files/latest/download/%{name}-%{version}.tar.gz
%define sha512 %{name}=457101136e59f7a1657ce591e9ea678ab9091a59219d41b6c522fad4a3555c5cbcb8c9e0c3267fd871940d99b5f8673ab4ce5ec9737dee52f017e5c80a4e59d7

Source1: atftpd.socket
Source2: atftpd.service

BuildRequires:    systemd-devel

Requires:         systemd
Requires(pre):    /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun): /usr/sbin/userdel /usr/sbin/groupdel

Provides:         tftp-server
Obsoletes:        tftp-server

Provides:         tftp
Obsoletes:        tftp

%description
Multithreaded TFTP server implementing all options (option extension and
multicast) as specified in RFC1350, RFC2090, RFC2347, RFC2348 and RFC2349.
Atftpd also support multicast protocol knowed as mtftp, defined in the PXE
specification. The server supports being started from inetd(8) as well as
a deamon using init scripts.

%package client
Summary:    Advanced Trivial File Transfer Protocol (ATFTP) - TFTP client
Group:      Applications/Internet

%description client
Advanced Trivial File Transfer Protocol client program for requesting
files using the TFTP protocol.

%prep
%autosetup -p1

%build
sh ./autogen.sh
%configure
%make_build

%install
%make_install %{?_smp_mflags}

mkdir -p %{buildroot}%{_sharedstatedir}/tftpboot \
         %{buildroot}%{_unitdir} \
         %{buildroot}%{_sysconfdir}/sysconfig

install -p -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/

sed -i -e "s|@SBINDIR@|%{_sbindir}|" -e "s|@SYSCONFDIR@|%{_sysconfdir}|" %{SOURCE2}
install -p -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/

cat << EOF >> %{buildroot}%{_sysconfdir}/sysconfig/atftpd
ATFTPD_USER=tftp
ATFTPD_GROUP=tftp
ATFTPD_OPTIONS=
ATFTPD_USE_INETD=false
ATFTPD_DIRECTORY=%{_sharedstatedir}/tftpboot
ATFTPD_BIND_ADDRESSES=
EOF

%check
sed -i 's/^start_server$/chown -R nobody $DIRECTORY\nstart_server/g' test/test.sh || true
%make_build check

%pre
if [ $1 -eq 1 ]; then
  getent group  tftp >/dev/null || groupadd -r tftp
  getent passwd tftp >/dev/null || useradd  -c "tftp" -s /bin/false -g tftp -M -r tftp
fi

%preun
%systemd_preun atftpd.socket

%post
/sbin/ldconfig
%systemd_post atftpd.socket

%postun
/sbin/ldconfig
%systemd_postun_with_restart atftpd.socket

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir %attr(0750,nobody,nobody) %{_sharedstatedir}/tftpboot
%{_mandir}/man8/atftpd.8.gz
%{_mandir}/man8/in.tftpd.8.gz
%{_sbindir}/atftpd
%{_sbindir}/in.tftpd
%{_unitdir}/atftpd.service
%{_unitdir}/atftpd.socket
%{_sysconfdir}/sysconfig/atftpd

%files client
%defattr(-,root,root)
%{_mandir}/man1/%{name}.1.gz
%{_bindir}/%{name}

%changelog
* Mon Jan 08 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.7.5-2
- Fix service file, start socket unit automatically
* Mon Sep 27 2021 Shreenidhi Shedi <sshedi@vmware.com> 0.7.5-1
- Upgrade to v0.7.5, fixes CVE-2021-41054
* Wed Jan 20 2021 Tapas Kundu <tkundu@vmware.com> 0.7.2-2
- Fix CVE-2020-6097
* Tue Jun 25 2019 Tapas Kundu <tkundu@vmware.com> 0.7.2-1
- Updated to release 0.7.2
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 0.7.1-8
- Remove shadow from requires and use explicit tools for post actions
* Thu May 26 2016 Divya Thaluru <dthaluru@vmware.com>  0.7.1-7
- Fixed logic to restart the active services after upgrade
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.7.1-6
- GA - Bump release of all rpms
* Fri May 6 2016 Divya Thaluru <dthaluru@vmware.com>  0.7.1-5
- Adding post-install run time dependencies
* Tue May 3 2016 Divya Thaluru <dthaluru@vmware.com>  0.7.1-4
- Fixing spec file to handle rpm upgrade scenario correctly
* Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com>  0.7.1-3
- Add systemd to Requires and BuildRequires.
- Use systemctl to enable/disable service.
* Mon Nov 23 2015 Xiaolin Li <xiaolinl@vmware.com> 0.7.1-2
- Chang tftpd from xinetd service to systemd service.
* Thu Nov 12 2015 Kumar Kaushik <kaushikk@vmware.com> 0.7.1-1
- Initial build. First version
