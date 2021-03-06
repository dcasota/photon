%define debug_package %{nil}
Summary:        Microsoft .NET Core SDK
Name:           dotnet-sdk
Version:        5.0.103
Release:        1%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
Url:            https://github.com/dotnet/core
Group:          Development/Tools
Source0:        %{name}-%{version}-linux-x64.tar.gz
%define sha1    dotnet-sdk=896579b12be0c8508525bf11d96946c60080ac73
BuildArch:      x86_64
Requires:       dotnet-runtime icu

%description
.NET Core is a development platform that you can use to build command-line
applications, microservices and modern websites.

%prep
%setup -c dotnet-sdk-%{version}

%build
%install
mkdir -p %{buildroot}%{_libdir}/dotnet/sdk
mkdir -p %{buildroot}%{_docdir}/dotnet-sdk-%{version}
cp -r sdk/%{version} %{buildroot}%{_libdir}/dotnet/sdk
cp LICENSE.txt ThirdPartyNotices.txt %{buildroot}%{_docdir}/dotnet-sdk-%{version}

%files
    %defattr(-,root,root,0755)
    %{_libdir}/*
    %{_docdir}/*

%changelog
*   Tue Mar 9 2021 Shreyas B. <shreyasb@vmware.com> 5.0.103-1
-   upgrade to version 5.0.103
*   Thu Jun 25 2020 Gerrit Photon <photon-checkins@vmware.com> 3.1.201-1
-   Automatic Version Bump
*   Thu Nov 07 2019 Shreyas B. <shreyasb@vmware.com> 2.1.509-1
-   upgraded to version 2.1.509
*   Wed Dec 05 2018 Ajay Kaher <akaher@vmware.com> 2.1.403-1
-   upgraded to version 2.1.403
*   Wed Jan 31 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.4-1
-   Initial build for photon
