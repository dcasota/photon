Summary:        Programs for handling passwords in a secure way
Name:           shadow
Version:        4.13
Release:        4%{?dist}
URL:            https://github.com/shadow-maint/shadow
License:        BSD
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/shadow-maint/shadow/releases/download/%{version}/%{name}-%{version}.tar.xz
%define sha512 %{name}=2949a728c3312bef13d23138d6b79caf402781b1cb179e33b5be546c1790971ec20778d0e9cd3dbe09691d928ffcbe88e60da42fab58c69a90d5ebe5e3e2ab8e

Source1: chage
Source2: chpasswd
Source3: login
Source4: other
Source5: passwd
Source6: sshd
Source7: su
Source8: system-account
Source9: system-auth
Source10: system-password
Source11: system-session
Source12: useradd

BuildRequires: cracklib-devel
BuildRequires: Linux-PAM-devel

Requires: cracklib
Requires: Linux-PAM
Requires: libpwquality
Requires: openssl
Requires: %{name}-libs = %{version}-%{release}
Requires: %{name}-tools = %{version}-%{release}

%description
The Shadow package contains programs for handling passwords in a secure way.

%package        tools
Summary:        Contains subset of tools which might be replaced by toybox
Group:          Applications/System
Requires:       %{name}-libs = %{version}-%{release}
Requires:       %{name} = %{version}-%{release}
Conflicts:      toybox < 0.8.2-2

%description    tools
Contains subset of tools which might be replaced by toybox

%package        lang
Summary:        Additional language files for shadow
Group:          Applications/System
Requires:       %{name} = %{version}-%{release}

%description    lang
These are the additional language files of shadow.

%package        devel
Summary:        Development libraries and headers for %{name}.
Requires:       %{name} = %{version}-%{release}

%description    devel
Development libraries and headers for %{name}.

%package        libs
Summary:        Libraries needed by %{name}.

%description    libs
Libraries needed by %{name}.

%prep
%autosetup -p1 -n %{name}-%{version}
sed -i 's/groups$(EXEEXT) //' src/Makefile.in
find man -name Makefile.in -exec sed -i 's/groups\.1 / /' {} \;
sed -i -e 's@#ENCRYPT_METHOD DES@ENCRYPT_METHOD SHA512@' \
    -e 's@/var/spool/mail@/var/mail@' etc/login.defs

sed -i 's@DICTPATH.*@DICTPATH\t/usr/share/cracklib/pw_dict@' \
    etc/login.defs

%build
%configure \
    $(test %{_host} != %{_build} && echo "--with-sysroot=/target-%{_arch}") \
    --with-libpam \
    --with-libcrack \
    --with-group-name-max-length=32

%make_build

%install
%make_install %{?_smp_mflags}
mkdir -p %{buildroot}%{_sysconfdir}/default
cp %{SOURCE12} %{buildroot}%{_sysconfdir}/default
# Disable usergroups. Use "users" group by default (see /usr/sbin/useradd)
# for all nonroot users.
sed -i 's/USERGROUPS_ENAB.*/USERGROUPS_ENAB no/' %{buildroot}%{_sysconfdir}/login.defs
cp etc/{limits,login.access} %{buildroot}%{_sysconfdir}
for FUNCTION in FAIL_DELAY \
                FAILLOG_ENAB \
                LASTLOG_ENAB \
                MAIL_CHECK_ENAB \
                OBSCURE_CHECKS_ENAB \
                PORTTIME_CHECKS_ENAB \
                QUOTAS_ENAB \
                CONSOLE MOTD_FILE \
                FTMP_FILE NOLOGINS_FILE \
                ENV_HZ PASS_MIN_LEN \
                SU_WHEEL_ONLY \
                CRACKLIB_DICTPATH \
                PASS_CHANGE_TRIES \
                PASS_ALWAYS_WARN \
                CHFN_AUTH ENCRYPT_METHOD \
                ENVIRON_FILE; do
  sed -i "s/^${FUNCTION}/# &/" %{buildroot}%{_sysconfdir}/login.defs
done

sed -i "s/^PASS_MAX_DAYS.*/PASS_MAX_DAYS    90/" %{buildroot}%{_sysconfdir}/login.defs

install -vm644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/
install -vm644 %{SOURCE2} %{buildroot}%{_sysconfdir}/pam.d/
install -vm644 %{SOURCE3} %{buildroot}%{_sysconfdir}/pam.d/
install -vm644 %{SOURCE4} %{buildroot}%{_sysconfdir}/pam.d/
install -vm644 %{SOURCE5} %{buildroot}%{_sysconfdir}/pam.d/
install -vm644 %{SOURCE6} %{buildroot}%{_sysconfdir}/pam.d/
install -vm644 %{SOURCE7} %{buildroot}%{_sysconfdir}/pam.d/
install -vm644 %{SOURCE8} %{buildroot}%{_sysconfdir}/pam.d/
install -vm644 %{SOURCE9} %{buildroot}%{_sysconfdir}/pam.d/
install -vm644 %{SOURCE10} %{buildroot}%{_sysconfdir}/pam.d/
install -vm644 %{SOURCE11} %{buildroot}%{_sysconfdir}/pam.d/

for PROGRAM in chfn chgpasswd chsh groupadd groupdel \
               groupmems groupmod newusers useradd userdel usermod; do
  install -v -m644 %{buildroot}%{_sysconfdir}/pam.d/chage %{buildroot}%{_sysconfdir}/pam.d/${PROGRAM}
  sed -i "s/chage/$PROGRAM/" %{buildroot}%{_sysconfdir}/pam.d/${PROGRAM}
done

find %{buildroot}%{_libdir} -name '*.la' -delete

%find_lang %{name}

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%post
/sbin/ldconfig
%{_sbindir}/pwconv
%{_sbindir}/grpconv

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/login.defs
%config(noreplace) %{_sysconfdir}/login.access
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/default/useradd
%config(noreplace) %{_sysconfdir}/limits
%{_bindir}/*
%{_sbindir}/*
%exclude %{_bindir}/su
%exclude %{_bindir}/login
%exclude %{_bindir}/passwd
%exclude %{_datadir}/locale/cs
%exclude %{_datadir}/locale/da
%exclude %{_datadir}/locale/de
%exclude %{_datadir}/locale/fi
%exclude %{_datadir}/locale/fr
%exclude %{_datadir}/locale/hu
%exclude %{_datadir}/locale/id
%exclude %{_datadir}/locale/it
%exclude %{_datadir}/locale/ja
%exclude %{_datadir}/locale/ko
%exclude %{_datadir}/locale/pl
%exclude %{_datadir}/locale/pt_BR
%exclude %{_datadir}/locale/ru
%exclude %{_datadir}/locale/sv
%exclude %{_datadir}/locale/tr
%exclude %{_datadir}/locale/zh_CN
%exclude %{_datadir}/locale/zh_TW
%config(noreplace) %{_sysconfdir}/pam.d/*

%files libs
%defattr(-,root,root)
%{_libdir}/libsubid.so.*

%files tools
%defattr(-,root,root)
%{_bindir}/passwd
%{_bindir}/su
%{_bindir}/login

%files devel
%defattr(-,root,root)
%{_libdir}/libsubid.so
%{_libdir}/libsubid.a
%{_includedir}/%{name}/subid.h

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.13-4
- Bump version as a part of openssl upgrade
* Wed Jan 25 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.13-3
- Exclude passwd from main package
* Mon Jan 02 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 4.13-2
- Rebuild with new cracklib
* Fri Nov 11 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.13-1
- Upgrade to v4.13
* Wed Feb 23 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.8.1-4
- Fix binary path
* Wed Feb 10 2021 Shreenidhi Shedi <sshedi@vmware.com> 4.8.1-3
- Added patch to be lenient with usernames
* Fri Sep 25 2020 Ankit Jain <ankitja@vmware.com> 4.8.1-2
- pam_cracklib has been deprecated.
- Replaced it with pam_pwquality
* Thu Jul 09 2020 Gerrit Photon <photon-checkins@vmware.com> 4.8.1-1
- Fix for Automatic Version Bump
* Thu Apr 16 2020 Alexey Makhalov <amakhalov@vmware.com> 4.6-5
- Do not conflict with toybox >= 0.8.2-2
* Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 4.6-4
- Cross compilation support
* Wed Oct 24 2018 Michelle Wang <michellew@vmware.com> 4.6-3
- Add su and login into shadow-tool.
* Tue Oct 2 2018 Michelle Wang <michellew@vmware.com> 4.6-2
- Add conflict toybox for shadow-tools.
* Wed Sep 19 2018 Srinidhi Rao <srinidhir@vmware.com> 4.6-1
- Upgrading the version to 4.6.
* Mon Jul 30 2018 Tapas Kundu <tkundu@vmware.com> 4.2.1-16
- Added fix for CVE-2018-7169.
* Fri Apr 20 2018 Alexey Makhalov <amakhalov@vmware.com> 4.2.1-15
- Move pam.d config file to here for better tracking.
- Add pam_loginuid module as optional in a session.
* Tue Oct 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.2.1-14
- Added -tools subpackage.
- Main package requires -tools or toybox.
* Tue Aug 15 2017 Anish Swaminathan <anishs@vmware.com> 4.2.1-13
- Added fix for CVE-2017-12424, CVE-2016-6252.
* Thu Apr 27 2017 Divya Thaluru <dthaluru@vmware.com> 4.2.1-12
- Allow '.' in username.
* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 4.2.1-11
- BuildRequires Linux-PAM-devel.
* Wed Nov 23 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.1-10
- Added -lang subpackage.
* Tue Oct 04 2016 ChangLee <changlee@vmware.com> 4.2.1-9
- Modified %check.
* Tue Jun 21 2016 Divya Thaluru <dthaluru@vmware.com> 4.2.1-8
- Added logic to not replace pam.d conf files in upgrade scenario.
* Fri May 27 2016 Divya Thaluru <dthaluru@vmware.com> 4.2.1-7
- Adding pam_cracklib module as requisite to pam password configuration.
* Wed May 25 2016 Divya Thaluru <dthaluru@vmware.com> 4.2.1-6
- Modifying pam_systemd module as optional in a session.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.2.1-5
- GA Bump release of all rpms.
* Mon May 2 2016 Xiaolin Li <xiaolinl@vmware.com> 4.2.1-4
- Enabling pam_systemd module in a session.
* Fri Apr 29 2016 Divya Thaluru <dthaluru@vmware.com> 4.2.1-3
- Setting password aging limits to 90 days.
* Wed Apr 27 2016 Divya Thaluru <dthaluru@vmware.com> 4.2.1-3
- Setting password aging limits to 365 days.
* Wed Mar 23 2016 Divya Thaluru <dthaluru@vmware.com> 4.2.1-2
- Enabling pam_limits module in a session.
* Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com> 4.2.1-1
- Update version.
* Wed Dec 2 2015 Divya Thaluru <dthaluru@vmware.com> 4.1.5.1-6
- Fixed PAM Configuration file for passwd.
* Mon Oct 26 2015 Sharath George <sharathg@vmware.com> 4.1.5.1-5
- Allow mixed case in username.
* Mon Jun 29 2015 Divya Thaluru <dthaluru@vmware.com> 4.1.5.1-4
- Fixed PAM Configuration file for chpasswd.
* Tue Jun 16 2015 Alexey Makhalov <amakhalov@vmware.com> 4.1.5.1-3
- Use group id 100(users) by default.
* Wed May 27 2015 Divya Thaluru <dthaluru@vmware.com> 4.1.5.1-2
- Adding PAM support.
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 4.1.5.1-1
- Initial build First version.
