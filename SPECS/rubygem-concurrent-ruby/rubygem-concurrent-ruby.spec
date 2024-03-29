%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name concurrent-ruby

Name: rubygem-concurrent-ruby
Version:        1.1.10
Release:        1%{?dist}
Summary:        Modern concurrency tools for Rails framework.
Group:          Development/Languages
License:        MIT
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/concurrent-ruby/versions/%{version}
Source0:        https://rubygems.org/downloads/concurrent-ruby-%{version}.gem
%define sha512    concurrent-ruby=ed01d65d79e6ed2987321f4665cb5f7c3fcd701029a33e68da0feb0cd6cb2682cef619566a3bd0996db207becb0425d77967b66ee66d775a489b1317e78807ab
BuildRequires:  ruby

%description
Modern concurrency tools including agents, futures, promises, thread pools, actors,
supervisors, and more. Inspired by Erlang, Clojure, Go, JavaScript, actors, and
classic concurrency patterns.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.1.10-1
-   Automatic Version Bump
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.1.7-1
-   Automatic Version Bump
*   Fri Aug 25 2017 Kumar Kaushik <kaushikk@vmware.com> 1.0.5-1
-   Initial build
