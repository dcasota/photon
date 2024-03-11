%define njs_ver     0.8.0
%define nginx_user  %{name}
%define headers_more_nginx_module_ver 0.37

Summary:        High-performance HTTP server and reverse proxy
Name:           nginx
Version:        1.25.2
Release:        3%{?dist}
License:        BSD-2-Clause
URL:            http://nginx.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://nginx.org/download/nginx-%{version}.tar.gz
%define sha512 %{name}=47da46d823f336432aca6c4cd54c76660af60620518d5c518504033a9fd6b411fd6d41e4aac2c8200311a53f96159aa3da8920145e8ed85596c9c2c14e20cb27

Source1: https://github.com/nginx/njs/archive/refs/tags/%{name}-njs-%{njs_ver}.tar.gz
%define sha512 %{name}-njs=5e5fd3b0aba9d1a0b47207081e59d577cbd3db41e141cfa529526a778bbcd4fec1cd4dacaa1dc63ee07868ccf35f4d4cc465abff831bb03d128b0b1f1b04bb28

Source2: https://github.com/openresty/headers-more-nginx-module/archive/refs/tags/headers-more-nginx-module-%{headers_more_nginx_module_ver}.tar.gz
%define sha512 headers-more-nginx-module=0cc2fffe506194d439e3669644d41b7943e2c3cffa3483eb70b92067930b358d506a14646eff8362b191a11c624db29f6b53d830876929dcb4ce1c9d7b2bc40d

Source3: %{name}.service

Patch0: CVE-2023-44487.patch

BuildRequires:  openssl-devel
BuildRequires:  pcre-devel
BuildRequires:  which
BuildRequires:  systemd-devel
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel

Requires: openssl
Requires: pcre
Requires: systemd

Requires(pre): systemd-rpm-macros
Requires(pre): /usr/sbin/useradd /usr/sbin/groupadd

%description
NGINX is a free, open-source, high-performance HTTP server and reverse proxy, as well as an IMAP/POP3 proxy server.

%prep
# Using autosetup is not feasible
%setup -q -a1 -a2

%patch -P0 -p1

%build
sh ./configure \
    --prefix=%{_sysconfdir}/%{name} \
    --sbin-path=%{_sbindir}/%{name} \
    --conf-path=/etc/%{name}/%{name}.conf \
    --pid-path=/var/run/%{name}.pid \
    --lock-path=/var/run/%{name}.lock \
    --error-log-path=/var/log/%{name}/error.log \
    --http-log-path=/var/log/%{name}/access.log \
    --add-module=njs-%{njs_ver}/%{name} \
    --add-dynamic-module=./headers-more-nginx-module-%{headers_more_nginx_module_ver} \
    --with-http_ssl_module \
    --with-pcre \
    --with-ipv6 \
    --with-stream \
    --with-http_auth_request_module \
    --with-http_sub_module \
    --with-http_stub_status_module \
    --with-http_v2_module \
    --with-http_realip_module \
    --user=%{nginx_user} \
    --group=%{nginx_user}

%make_build

%install
%make_install %{?_smp_mflags}
install -vdm755 %{buildroot}%{_unitdir}
install -vdm755 %{buildroot}%{_var}/log
install -vdm755 %{buildroot}%{_var}/opt/%{name}/log
ln -sfrv %{buildroot}%{_var}/opt/%{name}/log %{buildroot}%{_var}/log/%{name}
install -p -m 0644 %{SOURCE3} %{buildroot}%{_unitdir}/%{name}.service

%clean
rm -rf %{buildroot}

%pre
getent group %{nginx_user} > /dev/null || groupadd -r %{nginx_user}

getent passwd %{nginx_user} > /dev/null || \
  useradd -r -d %{_sharedstatedir}/nginx -g %{nginx_user} \
    -s /sbin/nologin -c "Nginx web server" %{nginx_user}

%post
%systemd_post %{name}.service

%postun
%systemd_postun %{name}.service

%preun
%systemd_preun %{name}.service

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/%{name}/fastcgi.conf
%config(noreplace) %{_sysconfdir}/%{name}/fastcgi.conf.default
%config(noreplace) %{_sysconfdir}/%{name}/fastcgi_params
%config(noreplace) %{_sysconfdir}/%{name}/fastcgi_params.default
%config(noreplace) %{_sysconfdir}/%{name}/koi-utf
%config(noreplace) %{_sysconfdir}/%{name}/koi-win
%config(noreplace) %{_sysconfdir}/%{name}/mime.types
%config(noreplace) %{_sysconfdir}/%{name}/mime.types.default
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf.default
%config(noreplace) %{_sysconfdir}/%{name}/scgi_params
%config(noreplace) %{_sysconfdir}/%{name}/scgi_params.default
%config(noreplace) %{_sysconfdir}/%{name}/uwsgi_params
%config(noreplace) %{_sysconfdir}/%{name}/uwsgi_params.default
%{_sysconfdir}/%{name}/modules/ngx_http_headers_more_filter_module.so
%{_sysconfdir}/%{name}/win-utf
%{_sysconfdir}/%{name}/html/*
%{_sbindir}/*
%{_unitdir}/%{name}.service
%dir %{_var}/opt/%{name}/log
%{_var}/log/%{name}

%changelog
* Wed Mar 06 2024 Harinadh D <hdommaraju@vmware.com> 1.25.2-3
- Add headers-more-nginx-module
* Thu Oct 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.25.2-2
- Fix CVE-2023-44487
* Mon Feb 20 2023 Harinadh D <hdommaraju@vmware.com> 1.22.0-4
- Enable http_realip_module
- Author: Brian Munro <bmunro-peralex>
* Wed Oct 26 2022 Keerthana K <keerthanak@vmware.com> 1.22.0-3
- Fix CVE-2022-41741 & CVE-2022-41742
* Tue Aug 16 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.22.0-2
- Fix sevice handling and run in nginx user context
* Tue Jul 19 2022 Harinadh D <hdommaraju@vmware.com> 1.22.0-1
- Version update
- security support is ended for 1.19 and till 1.21
* Tue Apr 12 2022 Nitesh Kumar <kunitesh@vmware.com> 1.19.3-5
- Fix for CVE-2021-3618
* Thu Dec 16 2021 Shreenidhi Shedi <sshedi@vmware.com> 1.19.3-4
- Fix nginx service handling
* Mon Nov 29 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.19.3-3
- Increment for openssl 3.0.0 compatibility
* Wed May 19 2021 Keerthana K <keerthanak@vmware.com> 1.19.3-2
- Fix for CVE-2021-23017
* Tue Sep 29 2020 Gerrit Photon <photon-checkins@vmware.com> 1.19.3-1
- Automatic Version Bump
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.19.2-2
- openssl 1.1.1
* Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 1.19.2-1
- Automatic Version Bump
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.19.0-1
- Automatic Version Bump
* Mon May 04 2020 Keerthana K <keerthanak@vmware.com> 1.16.1-2
- Adding http v2 module support.
* Mon Oct 14 2019 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.16.1-1
- update version to 1.16.1
* Fri Mar 15 2019 Keerthana K <keerthanak@vmware.com> 1.15.3-4
- Enable http_stub_status_module.
* Wed Nov 07 2018 Ajay Kaher <akaher@vmware.com> 1.15.3-3
- mark config files as non replaceable on upgrade.
* Mon Sep 17 2018 Keerthana K <keerthanak@vmware.com> 1.15.3-2
- Adding http_auth_request_module and http_sub_module.
* Fri Sep 7 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.15.3-1
- Upgrade to version 1.15.3
* Fri Jul 20 2018 Keerthana K <keerthanak@vmware.com> 1.13.8-3
- Restarting nginx on failure.
* Fri Jun 08 2018 Dheeraj Shetty <dheerajs@vmware.com> 1.13.8-2
- adding module njs.
* Fri May 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.13.8-1
- Update to version 1.13.8 to support nginx-ingress
* Thu Dec 28 2017 Divya Thaluru <dthaluru@vmware.com>  1.13.5-2
- Fixed the log file directory structure
* Wed Oct 04 2017 Xiaolin Li <xiaolinl@vmware.com> 1.13.5-1
- Update to version 1.13.5
* Mon May 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.11.13-2
- adding module stream to nginx.
* Wed Apr 05 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.11.13-1
- update to 1.11.13
* Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  1.10.0-5
- Add patch for CVE-2016-4450
* Wed Jul 27 2016 Divya Thaluru<dthaluru@vmware.com> 1.10.0-4
- Removed packaging of debug files
* Fri Jul 8 2016 Divya Thaluru<dthaluru@vmware.com> 1.10.0-3
- Modified default pid filepath and fixed nginx systemd service
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.10.0-2
- GA - Bump release of all rpms
* Mon May 16 2016 Xiaolin Li <xiaolinl@vmware.com> 1.10.0-1
- Initial build. First version
