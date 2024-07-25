%define srcname tomcat-native

Summary:        Apache Tomcat Native
Name:           apache-tomcat-native
Version:        2.0.3
Release:        4%{?dist}
License:        Apache 2.0
URL:            https://tomcat.apache.org/native-doc/
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

BuildArch: x86_64

Source0: https://dlcdn.apache.org/tomcat/tomcat-connectors/native/%{version}/source/%{srcname}-%{version}-src.tar.gz
%define sha512 %{srcname}=d80e6b76295bb253eaf6eab4d722f3ba2f683f33a96310838b4c44b99f0b47a49ed9c09bb53ed23698db057ce765e3fcbfcd4ac4b75d2bdbe691f916be3be339

Patch0: openssl_3_0_7_compatibility.patch

BuildRequires:  (openjdk11 or openjdk117)
BuildRequires:  openssl-devel
BuildRequires:  apr-devel

Requires:       apr
Requires:       openssl

%description
The Apache Tomcat Native Library is an optional component for use with Apache Tomcat
that allows Tomcat to use certain native resources for performance, compatibility, etc.

%package        devel
Summary:        Apache Tomcat Native development package
Requires:       %{name} = %{version}-%{release}

Conflicts:      %{name} < 2.0.3-3%{?dist}

%description    devel
Apache Tomcat Native development package

%prep
%autosetup -p1 -n %{srcname}-%{version}-src

%build
export JAVA_HOME=$(echo %{_libdir}/jvm/OpenJDK*)

cd native
%configure --with-apr=%{_prefix} \
           --with-java-home=$JAVA_HOME \
           --with-ssl=%{_prefix}

%make_build

%install
cd native
%make_install %{?_smp_mflags}

%clean
rm -rf %{buildroot}/*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libtcnative*.so.*
%exclude %{_libdir}/libtcnative-2.a

%files devel
%defattr(-,root,root,-)
%{_libdir}/libtcnative*.so

%changelog
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.0.3-4
- Bump version as a part of openssl upgrade
* Sat Aug 26 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.0.3-3
- Require jdk11 or jdk17
* Sat Jun 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.0.3-2
- Bump version as a part of openjdk11 upgrade
* Fri Mar 03 2023 Srish Srinivasan <ssrish@vmware.com> 2.0.3-1
- Update to v2.0.3
* Wed Sep 21 2022 Vamsi Krishna Brahmajosuyula <vbrahmajosyula@vmware.com> 1.2.24-4
- Use openjdk11
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.2.24-3
- Bump up release for openssl
* Thu Sep 10 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.2.24-2
- Openssl 1.1.1 compatibility
* Wed Jun 17 2020 Tapas Kundu <tkundu@vmware.com> 1.2.24-1
- Initial build.  First version
