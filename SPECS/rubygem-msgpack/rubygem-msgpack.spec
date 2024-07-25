%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name msgpack

Name: rubygem-msgpack
Version:        1.6.0
Release:        1%{?dist}
Summary:        A binary-based efficient object serialization library
Group:          Development/Languages
License:        Apache 2.0
Distribution:   Photon
Vendor:         VMware, Inc.
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/msgpack-%{version}.gem
%define sha512  msgpack=9aaa01a5ba3782cf8a6170b055c6d6914260ad4303a029d3fb0efe6a64eb415f3ff6bda34449444fe102c767ec892256fa9b568abc9c45f5713e94bbab86b92c
BuildRequires:  ruby
Requires:       ruby
Provides: rubygem-msgpack = %{version}

%description
MessagePack is a binary-based efficient object serialization library.
It enables to exchange structured objects between many languages like JSON.
But unlike JSON, it is very fast and small.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.6.0-1
-   Automatic Version Bump
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.3.3-1
-   Automatic Version Bump
*   Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 1.2.4-1
-   Initial build
