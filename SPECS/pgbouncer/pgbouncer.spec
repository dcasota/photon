Summary:          Connection pooler for PostgreSQL.
Name:             pgbouncer
Version:          1.26.0
Release:          1%{?dist}
URL:              https://wiki.postgresql.org/wiki/PgBouncer
Group:            Application/Databases.
Vendor:           VMware, Inc.
Distribution:     Photon

Source0:          https://%{name}.github.io/downloads/files/%{version}/%{name}-%{version}.tar.gz
Source1:          pgbouncer.service
Source2:          %{name}.sysusers

Source3: license.txt
%include %{SOURCE3}

BuildRequires:    libevent-devel
BuildRequires:    openssl-devel
BuildRequires:    systemd
BuildRequires:    systemd-devel
BuildRequires:    c-ares-devel
BuildRequires:    pkg-config
BuildRequires:    python3
BuildRequires:    go-md2man

Requires:         c-ares
Requires:         libevent
Requires:         openssl
Requires(pre):    systemd-rpm-macros
Requires(pre):    /usr/sbin/useradd /usr/sbin/groupadd

%description
Pgbouncer is a light-weight, robust connection pooler for PostgreSQL.

%prep
%autosetup -p1

%build
# Since 1.25 the release tarball no longer carries the man pages and make
# renders them with pandoc, which Photon OS does not ship: render the same
# filtered markdown with go-md2man, converting pandoc's title line into
# go-md2man's .TH form; make then finds them up to date.
pushd doc
PACKAGE_VERSION=%{version} python3 filter.py frag-usage-man.md usage.md > %{name}_1.md
PACKAGE_VERSION=%{version} python3 filter.py frag-config-man.md config.md > %{name}_5.md
for s in 1 5; do
  sed -i "1s/^%% \([A-Z.]*\)(${s}) %{version} | \(.*\)\$/%% \1 ${s} \"\" \"PgBouncer %{version}\" \"\2\"/" %{name}_${s}.md
  head -n 1 %{name}_${s}.md | grep -Eqx "%% [A-Z.]+ ${s} \"\" \"PgBouncer %{version}\" \"[^\"]+\""
  go-md2man -in %{name}_${s}.md -out %{name}.${s}
done
popd

%configure --with-cares --with-systemd
%make_build

%install
%make_install %{?_smp_mflags}
install -vdm 744 %{buildroot}%{_var}/log/pgbouncer
install -p -d %{buildroot}%{_sysconfdir}/
install -p -d %{buildroot}%{_sysconfdir}/sysconfig
install -p -m 644 etc/pgbouncer.ini %{buildroot}%{_sysconfdir}/
# auth_file of the default pgbouncer.ini: no users until the admin adds them
install -d -m 750 %{buildroot}%{_sysconfdir}/%{name}
touch %{buildroot}%{_sysconfdir}/%{name}/userlist.txt
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -p -D -m 0644 %{SOURCE2} %{buildroot}%{_sysusersdir}/%{name}.conf

%if 0%{?with_check}
%check
pushd test
%make_build all
popd
%endif

%pre
%sysusers_create_compat %{SOURCE2}

%post
if [ $1 -eq 1 ] ; then
  chown -R %{name}:%{name} \
           %{_var}/log/%{name}
fi
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
if [ $1 -eq 0 ] ; then
  rm -rf %{_var}/log/%{name} \
         %{_var}/run/%{name}
fi
%systemd_postun_with_restart %{name}.service

%posttrans
# Up to 1.17.0-7 the unit was installed in /etc/systemd/system, so an enabled
# service's wants link points at a file the upgrade removed: enable it again.
wants=%{_sysconfdir}/systemd/system/multi-user.target.wants/%{name}.service
if [ -L "${wants}" ] && [ ! -e "${wants}" ]; then
  systemctl reenable %{name}.service || :
fi

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/%{name}.ini
%dir %attr(0750,root,%{name}) %{_sysconfdir}/%{name}
%config(noreplace) %attr(0640,root,%{name}) %{_sysconfdir}/%{name}/userlist.txt
%{_mandir}/man1/%{name}.*
%{_mandir}/man5/%{name}.*
%{_docdir}/pgbouncer/*
%{_sysusersdir}/%{name}.conf
%dir %attr(-,%{name},%{name}) %{_var}/log/%{name}

%changelog
* Wed Oct 07 2026 Daniel Casota <dcasota@gmail.com> 1.26.0-1
- Upgrade to 1.26.0 for 9 CVEs; systemd Type=notify unit
* Mon Jun 02 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.17.0-7
- Fix spec issues
* Thu May 08 2025 Mukul Sikka <mukul.sikka@broadcom.com> 1.17.0-6
- Renaming sysusers to conf to fix auto user creation
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.17.0-5
- Release bump for SRP compliance
* Wed Oct 18 2023 Anmol Jain <anmolja@vmware.com> 1.17.0-4
- Using system c-ares to fix CVE-2021-3672
* Tue Aug 08 2023 Mukul Sikka <msikka@vmware.com> 1.17.0-3
- Resolving systemd-rpm-macros for group creation
* Fri Mar 10 2023 Mukul Sikka <msikka@vmware.com> 1.17.0-2
- Use systemd-rpm-macros for user creation
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.17.0-1
- Automatic Version Bump
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.15.0-2
- Bump up release for openssl
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.15.0-1
- Automatic Version Bump
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.14.0-2
- openssl 1.1.1
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.14.0-1
- Automatic Version Bump
* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 1.9.0-1
- Updated to version 1.9.0
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 1.7.2-7
- Remove shadow from requires and use explicit tools for post actions
* Mon Jul 24 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.7.2-6
- Seperate the service file from the spec file
* Wed May 31 2017 Rongrong Qiu <rqiu@vmware.com> 1.7.2-5
- Add RuntimeDirectory and Type=forking
* Thu Apr 13 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.7.2-4
- Fixed the requires.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.7.2-3
- GA - Bump release of all rpms
* Wed May 04 2016 Anish Swaminathan <anishs@vmware.com> 1.7.2-2
- Edit scriptlets.
* Thu Apr 28 2016 Kumar Kaushik <kaushikk@vmware.com> 1.7.2-1
- Initial Version.
