%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        A powerful, sanity-friendly HTTP client for Python.
Name:           python-urllib3
Version:        1.25.11
Release:        4%{?dist}
Url:            https://pypi.python.org/pypi/urllib3
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/shazow/urllib3/archive/urllib3-%{version}.tar.gz
%define sha512    urllib3=58f77edb9ced62cbac7b0baf2651c07f9f413267f103730ee25f08c5d4d0bf52a2ace02f58841bcd55652db677c7a1dc9a756681e7e32d590bc69d8b93e8f173

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  python-psutil
BuildRequires:  python3-pip
BuildRequires:  python-pip

Requires:       python2
Requires:       python2-libs
Requires:       ca-certificates
BuildArch:      noarch
Patch0:         CVE-2021-33503.patch
Patch1:         CVE-2023-43804.patch

%description
urllib3 is a powerful, sanity-friendly HTTP client for Python. Much of the Python ecosystem already uses urllib3 and you should too.

%package -n     python3-urllib3
Summary:        python-urllib3
Requires:       python3
Requires:       python3-libs
Requires:       ca-certificates

%description -n python3-urllib3
Python 3 version.

%prep
%autosetup -p1 -n urllib3-%{version}
# Dummyserver tests are failing when running in chroot. So disabling the tests.
rm -rf test/with_dummyserver/

%build
python2 setup.py build
python3 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check

nofiles=$(ulimit -n)
ulimit -n 5000
pip2 install -r dev-requirements.txt
pip3 install -r dev-requirements.txt

ignoretestslist='not test_select_interrupt_exception and not test_selector_error and not timeout and not test_request_host_header_ignores_fqdn_dot and not test_dotted_fqdn'
case $(uname -m) in
ppc*)
ignoretestslist="$ignoretestslist and not test_select_timing and not test_select_multiple_interrupts_with_event and not test_interrupt_wait_for_read_with_event and not test_select_interrupt_with_event";;
esac

PYTHONPATH="%{buildroot}%{$python2_sitelib}" pytest \
                --ignore=test/appengine \
                --ignore=test/with_dummyserver/test_proxy_poolmanager.py \
                --ignore=test/with_dummyserver/test_poolmanager.py \
                --ignore=test/contrib/test_pyopenssl.py \
                --ignore=test/contrib/test_securetransport.py \
                -k "${ignoretestslist}" \
                urllib3 test

PYTHONPATH="%{buildroot}%{$python3_sitelib}" pytest \
                --ignore=test/appengine \
                --ignore=test/with_dummyserver/test_proxy_poolmanager.py \
                --ignore=test/with_dummyserver/test_poolmanager.py \
                --ignore=test/contrib/test_pyopenssl.py \
                --ignore=test/contrib/test_securetransport.py \
                -k "${ignoretestslist}" \
                urllib3 test
ulimit -n $nofiles

%files
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-urllib3
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Mon Nov 20 2023 Mukul Sikka <msikka@vmware.com> 1.25.11-4
- Fix CVE-2023-43804
* Sat Jul 10 2021 Tapas Kundu <tkundu@vmware.com> 1.25.11-3
- Add ca-certificates in requires
* Wed Jul 07 2021 Sujay G <gsujay@vmware.com> 1.25.11-2
- Fix CVE-2021-33503
* Thu May 27 2021 Shreyas B <shreyasb@vmware.com> 1.25.11-1
- Update to version 1.25.11 to address
- CVE-2019-11324, CVE-2020-26137, CVE-2019-11236
* Mon Jan 14 2019 Tapas Kundu <tkundu@vmware.com> 1.23-2
- Fix make check
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 1.23-1
- Update to version 1.23
* Tue Aug 15 2017 Xiaolin Li <xiaolinl@vmware.com> 1.20-5
- Increased number of open files per process to 5000 before run make check.
* Wed Jul 26 2017 Divya Thaluru <dthaluru@vmware.com> 1.20-4
- Fixed rpm check errors
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.20-3
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.20-2
- Use python2 explicitly
* Thu Feb 02 2017 Xiaolin Li <xiaolinl@vmware.com> 1.20-1
- Initial packaging for Photon
