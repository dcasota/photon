Summary:    ODBC driver manager
Name:       freetds
Version:    1.1.36
Release:    3%{?dist}
License:    GPLv2
URL:        http://www.unixodbc.org/
Group:      System Environment/Libraries
Vendor:     VMware, Inc.
Distribution: Photon
Source0:    ftp://ftp.%{name}.org/pub/%{name}/stable/%{name}-%{version}.tar.gz
%define sha512 %{name}=5f650760bc78d91e217042a8c7882ba38c552346901dd89b62d0166a8777fe64aec2e0246adbf52fede2e4e3d67f1542b5c2a5ad636014cde49eceeccceb2b3b

BuildRequires: unixODBC-devel
BuildRequires: gnutls-devel
BuildRequires: nettle-devel

Requires:      gnutls
Requires:      nettle
Requires:      unixODBC

%description
FreeTDS is a project to document and implement the TDS (Tabular DataStream)
protocol. TDS is used by Sybase and Microsoft for client to database server
communications. FreeTDS includes call level interfaces for DB-Lib, CT-Lib,
and ODBC.

%package devel
Summary: Development files for unixODBC library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The freetds-devel package contains the files necessary for development with
the FreeTDS libraries.

%package unixODBC
Summary: FreeTDS ODBC Driver for unixODBC
Group: System Environment/Libraries
Requires: unixODBC

%description unixODBC
The freetds-unixodbc package contains ODBC driver build for unixODBC.

%package doc
Summary: User documentation for FreeTDS
Group: Documentation

%description doc
The freetds-doc package contains the userguide and reference of FreeTDS
and can be installed even if FreeTDS main package is not installed

%prep

%autosetup -p1

%build
%configure \
    --enable-static=no \
    --with-tdsver=auto \
    --with-unixodbc \
    --with-gnutls
make %{?_smp_mflags}

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
find %{buildroot} -name '*.a'  -delete
find %{buildroot} -name '*.la' -delete

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post unixODBC
echo "[FreeTDS]
Description = FreeTDS unixODBC Driver
Driver = %{_libdir}/libtdsodbc.so.0
Setup = %{_libdir}/libtdsodbc.so.0" | odbcinst -i -d -r > /dev/null 2>&1 || true
echo "[SQL Server]
Description = FreeTDS unixODBC Driver
Driver = %{_libdir}/libtdsodbc.so.0
Setup = %{_libdir}/libtdsodbc.so.0" | odbcinst -i -d -r > /dev/null 2>&1 || true

%preun unixODBC
odbcinst -u -d -n 'FreeTDS' > /dev/null 2>&1 || true
odbcinst -u -d -n 'SQL Server' > /dev/null 2>&1 || true

%files
%defattr(-,root,root)
%doc AUTHORS BUGS COPYING* ChangeLog INSTALL NEWS README TODO
%{_bindir}/*
%{_mandir}/man?/*
%{_libdir}/libct.so.*
%{_libdir}/libsybdb.so.*
%config(noreplace) %{_sysconfdir}/locales.conf
%config(noreplace) %{_sysconfdir}/pool.conf
%config(noreplace) %{_sysconfdir}/freetds.conf

%files devel
%defattr (-,root,root)
%{_libdir}/*.so
%{_includedir}/*

%files unixODBC
%defattr(-,root,root)
%{_libdir}/libtdsodbc.so*

%files doc
%defattr (-,root,root)
%{_docdir}/%{name}/*

%changelog
*   Mon Apr 22 2024 Roye Eshed <roye.eshed@broadcom.com> 1.1.36-3
-   Bump version as a part of unixODBC upgrade
*   Mon May 31 2021 Shreenidhi Shedi <sshedi@vmware.com> 1.1.36-2
-   Bump version to fix nettle dependancy issue.
*   Fri May 15 2020 Dweep Advani <dadvani@vmware.com> 1.1.36-1
-   Adding package freetds.
