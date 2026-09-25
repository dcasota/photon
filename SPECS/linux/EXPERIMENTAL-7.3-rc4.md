# experimental/linux-7.3-rc4

Photon 5.0 userland with the Linux **7.3-rc4** mainline release candidate from kernel.org.
Branched from `experimental/linux-7.2.7`; same pin approach, different kernel source.

| Field | Value |
|---|---|
| Base branch | `experimental/linux-7.2.7` (`ecfa3898d`) |
| Kernel | 7.3-rc4 (mainline release candidate, 2026-09-20) |
| Tarball | https://git.kernel.org/torvalds/t/linux-7.3-rc4.tar.gz |
| sha512 | `7a4b9599c2c593131e150ae22030f643813b0fb3de2b479281ebb9a413e7928903adc748eb522e03fd39e9ca4991c12e4d0331718fff59a53fc6676b390c7945` |
| git tag v7.3-rc4 (peeled) | `93f51579e7df248780214094418f205253383cc5` |
| RPM version | `Version: 7.3.0`, `Release: 0.rc4.1%{?dist}` (sorts below a 7.3.0 final) |
| uname -r | `7.3.0-0.rc4.1.ph5` (`linux`), `7.3.0-0.rc4.1.ph5-esx` (`linux-esx`) |
| Dist tag | `.ph5` (unchanged) |
| FIPS / canister | **off** (`%global fips 0` on x86_64) |
| Patches | Patch0 + Patch1 only (both apply cleanly to 7.3-rc4); 6.12 ranges and CVE include skipped |
| Config | same olddefconfig merge as 7.2.7 (see `CONFIG-MERGE-7.2.7.md`) |

An RPM version cannot contain `-`, so the tarball directory `linux-7.3-rc4` is carried in
`%define kernel_src`, and `%prep` blanks the Makefile's `EXTRAVERSION = -rc4`. The kernel then
names itself `7.3.0` + `CONFIG_LOCALVERSION="-%{release}"`, which equals `uname_r`
(`%{version}-%{release}`).

`runPh7-3-RC4.sh` in `dcasota/photonos-scripts` applies these spec changes at build time, so
the committed `linux.spec` / `linux-esx.spec` stay as on the base branch.
