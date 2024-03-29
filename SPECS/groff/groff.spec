Summary:    Programs for processing and formatting text
Name:       groff
Version:    1.22.4
Release:    1%{?dist}
License:    GPLv3+
URL:        http://www.gnu.org/software/groff
Group:      Applications/Text
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: http://ftp.gnu.org/gnu/groff/%{name}-%{version}.tar.gz
%define sha512 %{name}=1c42d3cd71efaf067b5850945d9097fa1f0fadd5e2b6ba7446bd9d4f439fe1ad058e4ddb0d4e0f503682137dfc7c822944ce1e3e5cf981673f8ba197ea77126d

Provides:   perl(oop_fh.pl)
Provides:   perl(main_subs.pl)
Provides:   perl(man.pl)
Provides:   perl(subs.pl)

Requires: perl
Requires: perl-DBI
Requires: perl-DBIx-Simple
Requires: perl-DBD-SQLite
Requires: perl-File-HomeDir

%define BuildRequiresNative groff

%description
The Groff package contains programs for processing
and formatting text.

%prep
%autosetup -p1

%build
export PAGE=letter
%configure \
    --with-grofferdir=%{_datadir}/%{name}/%{version}/groffer
# package does not support parallel make
%make_build $(test %{_host} != %{_build} && echo "GROFFBIN=groff")

%install
install -vdm 755 %{_docdir}/%{name}-1.22/pdf
%make_install %{?_smp_mflags}
rm -rf %{buildroot}%{_infodir}

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/groff/*
%{_datadir}/%{name}/*
%{_docdir}/%{name}-%{version}/*
%{_mandir}/*/*

%changelog
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 1.22.4-1
- Automatic Version Bump
* Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 1.22.3-3
- Cross compilation support
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.22.3-2
- GA - Bump release of all rpms
* Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 1.22.3-1
- Updated to version 1.22.3
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.22.2-1
- Initial build. First version
