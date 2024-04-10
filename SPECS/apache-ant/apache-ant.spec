%define _prefix %{_var}/opt/%{name}
%define _bindir %{_prefix}/bin
%define _libdir %{_prefix}/lib

%define hamcrest_ver    1.3
%define ant_tasks_ver   2.1.3

Summary:    Apache Ant
Name:       apache-ant
Version:    1.10.10
Release:    5%{?dist}
License:    Apache
URL:        http://ant.apache.org
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution:   Photon

BuildArch:      noarch

Source0: http://apache.mirrors.lucidnetworks.net//ant/source/%{name}-%{version}-src.tar.gz
%define sha512 %{name}=428eecbd38d975c705320c1e9ee0a069c6a9c80dc30e52ce03279f8e3816fc098ce6e6591831cdd398eabe444c837add1d26152ff2303470f63d8f0a45bd2ae1

Source1: http://hamcrest.googlecode.com/files/hamcrest-%{hamcrest_ver}.tar.gz
%define sha512 hamcrest=5672bc627bc71d6fd64b6f776b89ac16ed68819fa4a0748c1250b57f1065c1e7e18ba184d9fe3392e54000ddeb353d0d8d67f4eecdf464974563f05c6b226fc2

Source2: https://packages.vmware.com/photon/photon_sources/1.0//maven-ant-tasks-%{ant_tasks_ver}.tar.gz
%define sha512 maven-ant-tasks=4df5b96a11819f82732c54656db8b0e0f4697079113d644622b4f82dc218ac1829b97aa8dc2427d3903ebdb0eb82e2ee35f9d3160647edb09bb243d8ba266fd8

Patch0: %{name}-CVE-2021-36373-CVE-2021-36374.patch

BuildRequires: openjdk8

Requires: (openjdk8 or openjdk11 or openjdk17)

%description
The Ant package contains binaries for a build system

%package -n ant-scripts
Summary:        Additional scripts for ant
Requires:       %{name} = %{version}-%{release}
Requires:       python3

%description -n ant-scripts
Apache Ant is a Java-based build tool.

This package contains additional perl and python scripts for Apache
Ant.

%prep
%autosetup -p1 -a1 -b2

%build

%install
cp -v ./hamcrest-%{hamcrest_ver}/hamcrest-core-%{hamcrest_ver}.jar ./lib/optional

export JAVA_HOME=$(echo /usr/lib/jvm/OpenJDK-*)

ANT_DIST_DIR=%{buildroot}%{_prefix}
mkdir -p -m 700 $ANT_DIST_DIR

./bootstrap.sh
./build.sh -Ddist.dir=$ANT_DIST_DIR

mkdir -p %{buildroot}%{_datadir}/java/ant

for jar in %{buildroot}%{_libdir}/*.jar; do
  jarname=$(basename $jar .jar)
  ln -sfv %{_libdir}/${jarname}.jar %{buildroot}%{_datadir}/java/ant/${jarname}.jar
done

rm -rf %{buildroot}%{_bindir}/*.bat \
       %{buildroot}%{_bindir}/*.cmd

mkdir -p %{buildroot}/bin
for b in %{buildroot}%{_bindir}/*; do
    binaryname=$(basename $b)
    ln -sfv %{_bindir}/${binaryname} %{buildroot}/bin/${binaryname}
done

MAVEN_ANT_TASKS_DIR=%{buildroot}%{_prefix}/maven-ant-tasks

mkdir -p -m 700 $MAVEN_ANT_TASKS_DIR

pushd %{_builddir}/maven-ant-tasks-%{ant_tasks_ver}
cp maven-ant-tasks-%{ant_tasks_ver}.jar %{buildroot}%{_libdir}
cp LICENSE NOTICE README.txt $MAVEN_ANT_TASKS_DIR/
popd

chown -R root:root $MAVEN_ANT_TASKS_DIR
chmod 644 $MAVEN_ANT_TASKS_DIR/*

%check
# Disable following tests which are currently failing in chrooted environment -
#   - org.apache.tools.ant.types.selectors.OwnedBySelectorTest
#   - org.apache.tools.ant.types.selectors.PosixGroupSelectorTest
#   - org.apache.tools.mail.MailMessageTest
#   - org.apache.tools.ant.AntClassLoaderTest
#   - org.apache.tools.ant.taskdefs.optional.XsltTest
if [ "$(stat -c %d:%i /)" != "$(stat -c %d:%i /proc/1/root/.)" ]; then
  rm -f src/tests/junit/org/apache/tools/ant/types/selectors/OwnedBySelectorTest.java \
        src/tests/junit/org/apache/tools/ant/types/selectors/PosixGroupSelectorTest.java \
        src/tests/junit/org/apache/tools/mail/MailMessageTest.java \
        src/tests/junit/org/apache/tools/ant/AntClassLoaderTest.java \
        src/tests/junit/org/apache/tools/ant/taskdefs/optional/XsltTest.java
fi
export JAVA_HOME=$(echo /usr/lib/jvm/OpenJDK-*)
bootstrap/bin/ant -v run-tests

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir %{_bindir}
%dir %{_libdir}
%dir %{_datadir}/java/ant
%dir %{_prefix}/maven-ant-tasks
/bin/ant
/bin/antRun
%{_bindir}/ant
%{_bindir}/antRun
%{_libdir}/*
%{_datadir}/java/ant/*.jar
%{_prefix}/maven-ant-tasks/LICENSE
%{_prefix}/maven-ant-tasks/README.txt
%{_prefix}/maven-ant-tasks/NOTICE

%files -n ant-scripts
%defattr(-,root,root)
/bin/antRun.pl
/bin/complete-ant-cmd.pl
/bin/runant.pl
/bin/runant.py
%{_bindir}/antRun.pl
%{_bindir}/complete-ant-cmd.pl
%{_bindir}/runant.py
%{_bindir}/runant.pl

%changelog
* Tue Mar 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.10.10-5
- Bump version as a part of openjdk8 upgrade
* Fri Sep 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.10.10-4
- Require jre8 or jdk11-jre or jdk17-jre
* Sat Jun 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.10.10-3
- Bump version as a part of openjdk8 upgrade
* Tue Jul 20 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.10.10-2
- Fix CVE CVE-2021-36373, CVE-2021-36374
* Tue Jun 01 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.10.10-1
- Bump to version 1.10.10
* Mon Dec 14 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.10.8-3
- Fix build with new rpm
* Thu Nov 12 2020 Michelle Wang <michellew@vmware.com> 1.10.8-2
- Update Source0 with using https://packages.vmware.com/photon
* Mon Jul 27 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.10.8-1
- Bump to version 1.10.8
* Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 1.10.5-5
- Require python3
* Wed Sep 11 2019 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.10.5-4
- Fix Make check
* Tue Dec 04 2018 Dweep Advani <dadvani@vmware.com> 1.10.5-3
- Adding MakeCheck tests
* Mon Nov 05 2018 Alexey Makhalov <amakhalov@vmware.com> 1.10.5-2
- Removed dependency on JAVA8_VERSION macro
* Mon Sep 17 2018 Ankit Jain <ankitja@vmware.com> 1.10.5-1
- Updated Apache Ant to 1.10.5
* Wed Jun 28 2017 Kumar Kaushik <kaushikk@vmware.com> 1.10.1-5
- Base package does not require python2.
* Mon Jun 19 2017 Divya Thaluru <dthaluru@vmware.com> 1.10.1-4
- Removed dependency on ANT_HOME
- Moved perl and python scripts to ant-scripts package
* Mon Jun 05 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.10.1-3
- Fixed the profile.d/apache-ant.sh script to include ant in $PATH
* Thu May 18 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.10.1-2
- Renamed openjdk to openjdk8
* Mon Apr 17 2017 Chang Lee <changlee@vmware.com> 1.10.1-1
- Updated Apache Ant to 1.10.1
* Fri Mar 31 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9.6-6
- use java rpm macros to determine versions
* Wed Dec 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9.6-5
- Updated JAVA_HOME path to point to latest JDK.
* Tue Oct 04 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9.6-4
- Updated JAVA_HOME path to point to latest JDK.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9.6-3
- GA - Bump release of all rpms
* Fri May 20 2016 Divya Thaluru <dthaluru@vmware.com> 1.9.6-2
- Updated JAVA_HOME path to point to latest JDK.
* Mon Feb 29 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.9.6-1
- Updated to version 1.9.6
* Fri Feb 26 2016 Kumar Kaushik <kaushikk@vmware.com> 1.9.4-4
- Updated JAVA_HOME path to point to latest JDK.
* Mon Nov 16 2015 Sharath George <sharathg@vmware.com> 1.9.4-3
- Changed path to /var/opt.
* Wed Sep 16 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.9.4-2
- Updated dependencies after repackaging openjdk.
* Wed Aug 12 2015 Sriram Nambakam <snambakam@vmware.com> 1.9.4
- Added maven ant tasks
* Fri May 22 2015 Sriram Nambakam <snambakam@vmware.com> 1.9.4
- Initial build.  First version
