%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name tzinfo

Name:           rubygem-tzinfo
Version:        2.0.5
Release:        2%{?dist}
Summary:        Timezone related support for Ruby.
Group:          Development/Languages
License:        MIT
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/tzinfo/versions/%{version}

Source0: https://rubygems.org/downloads/tzinfo-%{version}.gem
%define sha512 %{gem_name}=d3248d9226b974095392c17916701c7318df895fb1d5581d3bafd73672fbb1ec30f4c1bac690379c714df66856558011c27bcedf2d53beb51031441f7bfee0ae

BuildRequires: ruby

Requires: ruby
Requires: rubygem-concurrent-ruby

%description
TZInfo provides daylight savings aware transformations between times in different time zones.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%check
cd %{buildroot}%{gemdir}/gems/tzinfo-%{version}
gem install thread_safe
rake test

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Tue Oct 24 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.0.5-2
- Fix requires
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 2.0.5-1
- Automatic Version Bump
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 2.0.2-1
- Automatic Version Bump
* Tue Nov 27 2018 Sujay G <gsujay@vmware.com> 1.2.5-2
- Added %check section
* Tue Aug 14 2018 Srinidhi Rao <srinidhir@vmware.com> 1.2.5-1
- Upgraded to 1.2.5
* Fri Aug 25 2017 Kumar Kaushik <kaushikk@vmware.com> 1.2.3-1
- Initial build
