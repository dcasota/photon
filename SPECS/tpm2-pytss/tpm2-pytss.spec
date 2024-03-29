Name:       tpm2-pytss
Version:    1.2.0
Release:    2%{?dist}
Summary:    Python bindings for tpm2-tss
License:    BSD
URL:        https://github.com/tpm2-software/tpm2-pytss
Vendor:     VMware, Inc.
Group:      System Environment/Security
Distribution: Photon

Source0: https://github.com/tpm2-software/tpm2-pytss/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=9f317b2144e27ac0e6b876d1987cd5c64f4c1f70d1689cea3d926749d9778b2ad813335269cff70c8335f15b72b1233fffe062f4cb5791c5480c58119cf42db7

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pkgconfig
BuildRequires: python3-pycparser
BuildRequires: python3-pip
BuildRequires: git
BuildRequires: tpm2-tss-devel

%if 0%{?with_check}
BuildRequires: python3-pytest
BuildRequires: python3-cryptography
BuildRequires: python3-cffi
BuildRequires: python3-pip
BuildRequires: python3-PyYAML
%endif

Requires: tpm2-tss
Requires: python3

%description
TPM2 TSS Python bindings for Enhanced System API (ESYS).
This package primarily exposes the TPM 2.0 Enhanced System API.

%prep
%autosetup -p1 -Sgit

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
export PYTHONPATH=%{buildroot}%{python3_sitelib}
%pytest
%endif

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.2.0-2
- Update release to compile with python 3.11
* Wed Oct 05 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.2.0-1
- First build. Needed for tpm2-pkcs11.
