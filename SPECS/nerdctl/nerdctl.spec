%define debug_package %{nil}
# git tag commit hash
# update commit id upon every new version release
%define commit_hash 7e8114a82da342cdbec9a518c5c6a1cce58105e9

Summary:        Docker-compatible CLI for containerd
Name:           nerdctl
Version:        1.4.0
Release:        5%{?dist}
License:        Apache 2.0
URL:            https://github.com/containerd/nerdctl
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/containerd/nerdctl/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=b14cd92b76d9699b4042fcd7a6906b1c714221b30cff1074a1d59ea038cf74ea6437d4a4d9a265e7b0f4c96397c82d53856f9e43d08aa8abcb98af5e9fb6e8dc

BuildRequires:  go
BuildRequires:  build-essential
BuildRequires:  ca-certificates

Requires: cni >= 1.1.1
Requires: containerd
Requires: slirp4netns
Requires: libslirp
Requires: rootlesskit
Requires: fuse-overlayfs
Requires: fuse-overlayfs-snapshotter

%description
%{summary}
contaiNERD CTL - Docker-compatible CLI for containerd, with support for
Compose, Rootless, eStargz, OCIcrypt, IPFS, ...
This package also provides containerd-rootless scripts.

%prep
%autosetup -p1

%build
export VERSION="%{version}-%{release}"
export REVISION=%{commit_hash}

%make_build

%install
export BINDIR="%{_bindir}"
%make_install %{?_smp_mflags}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_bindir}/containerd-rootless.sh
%{_bindir}/containerd-rootless-setuptool.sh

%changelog
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.4.0-5
- Bump up version to compile with new go
* Tue Sep 26 2023 Piyush Gupta <gpiyush@vmware.com> 1.4.0-4
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.4.0-3
- Bump up version to compile with new go
* Thu Jul 13 2023 Prashant S Chauhan <psinghchauha@vmware.com> 1.4.0-2
- Version bump up to use fuse-overlayfs-snapshotter v1.0.6
* Tue Jul 04 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.4.0-1
- Upgrade to v1.4.0
* Mon Jul 03 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.1.0-1
- Upgrade to v1.1.0
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 0.23.0-4
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 0.23.0-3
- Bump up version to compile with new go
* Tue Apr 04 2023 Piyush Gupta <gpiyush@vmware.com> 0.23.0-2
- Bump up version to compile with new go
* Fri Sep 30 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.23.0-1
- First build.
