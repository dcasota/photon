Summary:        Shell tool for executing jobs in parallel
Name:           parallel
Version:        20221122
Release:        1%{?dist}
License:        GPLv3+ and GFDL
Group:          Productivity/File utilities
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch
Url:            https://www.gnu.org/software/parallel/
Source0:        https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.bz2
%define sha512  parallel=cdae4ec3a5aaf1ae6c0d9dc35bad930c2b34ad4f91209de80d55258f1945e2df345708000a2facef3b647b6e0d4c275c909faf073961ae0b80b89efa8831211f

%description
GNU parallel is a shell tool for executing jobs concurrently locally or using remote computers.
A job is typically a single command or a small script that has to be run for each of the lines
in the input. The typical input is a list of files, a list of hosts, a list of users,
a list of URLs, or a list of tables.

%package        doc
Summary:        Documentation for parallel tool
%description    doc
It contains documentation for parallel shell tool

%prep
%autosetup

%build
%configure
%make_build %{?_smp_mflags}

%install
cd src/
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%check
%if 0%{?with_check}
%make_build %{?_smp_mflags} check
%endif

%files
%defattr(-,root,root)
%license LICENSES/GPL-3.0-or-later.txt LICENSES/CC-BY-SA-4.0.txt LICENSES/GFDL-1.3-or-later.txt
%doc README NEWS
%{_bindir}/parallel
%{_bindir}/parcat
%{_bindir}/parset
%{_bindir}/parsort
%{_bindir}/env_parallel*
%{_bindir}/sem
%{_bindir}/sql
%{_bindir}/niceload

%files doc
%defattr(-,root,root)
%{_docdir}/*
%{_mandir}/man1/*
%{_mandir}/man7/*

%changelog
* Tue Dec 13 2022 Gerrit Photon <photon-checkins@vmware.com> 20221122-1
- Automatic Version Bump
* Mon Apr 04 2022 Prashant S Chauhan <psinghchauha@vmware.com> 20220622-1
- parallel initial build
