Summary:	Tool to analyze BIOS DMI data
Name:		dmidecode
Version:	3.2
Release:	1%{?dist}
License:	GPLv2+
URL:		http://www.nongnu.org/dmidecode/
Group:		System Environment/Base
Source0:	http://download.savannah.gnu.org/releases/dmidecode/%{name}-%{version}.tar.xz
%define sha1 dmidecode=acf4b5c6e757066453fd06aa9060fceb257849bf
Vendor:		VMware, Inc.
Distribution:	Photon
%description
Dmidecode reports information about your system's hardware as described in your system BIOS according to the SMBIOS/DMI standard. This information typically includes system manufacturer, model name, serial number, BIOS version, asset tag as well as a lot of other details of varying level of interest and reliability depending on the manufacturer. This will often include usage status for the CPU sockets, expansion slots (e.g. AGP, PCI, ISA) and memory module slots, and the list of I/O ports (e.g. serial, parallel, USB).

%prep
%setup -q
%build
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} prefix=%{_prefix} install
%files
%defattr(-,root,root)
%{_sbindir}/*
%{_docdir}/%{name}/*
%{_mandir}/man8/*

%changelog
*   Thu Jun 25 2020 Gerrit Photon <photon-checkins@vmware.com> 3.2-1
-   Automatic Version Bump
*   Mon Sep 10 2018 Ajay Kaher <akaher@vmware.com> 3.1-1
-   Upgraded to version 3.1
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.0-2
-   GA - Bump release of all rpms
*   Mon Nov 02 2015 Divya Thaluru <dthaluru@vmware.com> 3.0-1
-   Initial build. First version
