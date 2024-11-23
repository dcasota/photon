Name:       debugedit
Version:    5.0
Release:    9%{?dist}
Summary:    Tools for debuginfo creation
License:    GPLv3+ and GPLv2+ and LGPLv2+
URL:        https://sourceware.org/debugedit
Group:      System Environment/Base
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://sourceware.org/ftp/debugedit/%{version}/%{name}-%{version}.tar.xz
%define sha512 %{name}=7e7f529eafe41b53f0b5bfc58282fdbfa0dfa93ed7908b70e81942d6d2b6f80fc9c6bff2ed9674fd98947e5750b615f4c8b222544989e2900c5f8ff5ae0efb92

Patch0: 0001-tweak-find-debuginfo.patch
Patch1: 0002-do-not-check-for-exec-permission.patch
Patch2: 0003-tests-Handle-zero-directory-entry-in-.debug_line-DWA.patch
Patch4: 0004-scripts-find-debuginfo.in-retain-.note.GNU-stack-sec.patch

BuildRequires: make
BuildRequires: gcc
BuildRequires: help2man

# For the testsuite.
BuildRequires: autoconf
BuildRequires: automake

# The find-debuginfo.sh script has a couple of tools it needs at runtime.
# For strip_to_debug, eu-strip
Requires: elfutils
# For add_minidebug, readelf, awk, nm, sort, comm, objcopy, xz
Requires: gawk
Requires: xz
Requires: coreutils >= 9.1-7
# For do_file, gdb_add_index
# We only need gdb-add-index, so suggest gdb-minimal (full gdb is also ok)
Requires: (gdb or gdb-minimal)
# For dwz
Requires: dwz

%description
The debugedit project provides programs and scripts for creating
debuginfo and source file distributions, collect build-ids and rewrite
source paths in DWARF data for debugging, tracing and profiling.

It is based on code originally from the rpm project plus libiberty and
binutils.  It depends on the elfutils libelf and libdw libraries to
read and write ELF files, DWARF data and build-ids.

%prep
%autosetup -p1

%build
autoreconf -fvi
%configure
%make_build

%install
%make_install %{?_smp_mflags}
pushd %{buildroot}%{_bindir}
ln -srv find-debuginfo find-debuginfo.sh
popd

%check
sed -i 's/^\(C\|LD\)FLAGS=.*/\1FLAGS=""/' tests/atlocal
%make_build check

%files
%defattr(-,root,root)
%{_bindir}/debugedit
%{_bindir}/sepdebugcrcfix
%{_bindir}/find-debuginfo
%{_bindir}/find-debuginfo.sh
%{_mandir}/man1/debugedit.1*
%{_mandir}/man1/sepdebugcrcfix.1*
%{_mandir}/man1/find-debuginfo.1*

%changelog
* Wed Oct 16 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 5.0-9
- Require coreutils only
* Fri Aug 02 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 5.0-8
- Retain .note.GNU-stack while stripping object files
* Fri Jul 26 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 5.0-7
- Remove exec permission check during debuginfo generation
* Fri Jul 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.0-6
- Fix gdb requires
* Tue Jul 11 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.0-5
- Bump version as a part of elfutils upgrade
* Wed Jan 25 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.0-4
- Fix requires
* Fri Jan 06 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.0-3
- Bump up due to change in elfutils
* Fri Jan 06 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 5.0-2
- Version bump for dwz upgrade.
* Fri Dec 10 2021 Shreenidhi Shedi <sshedi@vmware.com> 5.0-1
- Intial version. Needed for rpm-4.17.0
