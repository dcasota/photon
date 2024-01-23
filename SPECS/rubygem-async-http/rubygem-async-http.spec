%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name async-http

Name: rubygem-async-http
Version:        0.52.5
Release:        2%{?dist}
Summary:        A HTTP client and server library.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512  async-http=3b05bce79fad475d94e552d45e47180d196f4640b36915253cd2f2872b291213f4573083e443bd47da3c972d13bef9c68e308e73b92a392df4eca58b33a32911

BuildRequires:  ruby

Requires: rubygem-async >= 1.19.0, rubygem-async < 2.0.0
Requires: rubygem-async-io >= 1.25.0, rubygem-async-io < 2.0.0
Requires: rubygem-protocol-http >= 0.20.1
Requires: rubygem-protocol-http1 >= 0.13.1
Requires: rubygem-protocol-http2 >= 0.14.1
Requires: rubygem-fiber-local
Requires: rubygem-traces
Requires: rubygem-async-pool
Requires: ruby

BuildArch: noarch

%description
An asynchronous client and server implementation of HTTP/1.0, HTTP/1.1 and HTTP/2
including TLS. Support for streaming requests and responses. Built on top of async
and async-io. falcon provides a rack-compatible server.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Fri Dec 15 2023 Shivani Agarwal <shivania2@vmware.com> 0.52.5-2
-   Fix requires
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 0.52.5-1
-   Automatic Version Bump
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 0.52.4-1
-   Automatic Version Bump
*   Wed Aug 21 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 0.48.2-1
-   Initial build
