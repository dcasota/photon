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
| Patches | Patch0 + Patch1, plus the RAP/KCFI "Secure" patches Patch61 (rebased: `secure/0001-gcc-rap-plugin-with-kcfi-7.3.patch`) and Patch63 (PAX tasklet fix) for `linux`; other 6.12 ranges and the CVE include skipped |
| Config | same olddefconfig merge as 7.2.7 (see `CONFIG-MERGE-7.2.7.md`) |

An RPM version cannot contain `-`, so the tarball directory `linux-7.3-rc4` is carried in
`%define kernel_src`, and `%prep` blanks the Makefile's `EXTRAVERSION = -rc4`. The kernel then
names itself `7.3.0` + `CONFIG_LOCALVERSION="-%{release}"`, which equals `uname_r`
(`%{version}-%{release}`).

`runPh7-3-RC4.sh` in `dcasota/photonos-scripts` applies these spec changes at build time, so
the committed `linux.spec` / `linux-esx.spec` stay as on the base branch.

## RAP/KCFI on 7.3-rc4

`secure/0001-gcc-rap-plugin-with-kcfi-7.3.patch` (sha256 `267919b18c6ba595a012ba8b3e49e2ae54e5f9f81153c76e2004708d0d3d8fdc`)
replaces the 6.12 `0001-gcc-rap-plugin-with-kcfi.patch` for this branch. Changes against the 6.12 patch:

1. `arch/x86/include/asm/vermagic.h` hunk rebased: Linux 7.1 removed `CONFIG_M486` / `M486SX` / `MELAN`.
2. `CFI_CLANG` to `CFI` rename followed in `Makefile`, `arch/Kconfig`, `arch/x86/Kconfig`, `security/Kconfig`.
3. STRUCTLEAK block, `modpost.c` and obsolete `vmware.c` io_delay hunks rebased or dropped.
4. `rap_plugin` objects built from `$(src)` with `-I $(src)` (7.3 Kbuild).
5. `__nocfi` emits no kCFI attribute under `CONFIG_PAX_RAP` (gcc has no kcfi sanitizer).
6. RAP hashes `gimple_call_fntype()`, and RAP builds use `-fno-tree-tail-merge`, so union-based
   indirect calls (7.x `kernel/sysctl.c` `proc_vec_conv`) keep one check per target type.

Tested: clean `patch --dry-run` on pristine 7.3-rc4; full `bzImage modules` build (949 modules,
vermagic `... RAP`); QEMU/KVM boot of Photon 5.0 to the login prompt without PAX/RAP violations.
Patch62 (`objtool: Return error in case of failures`) stays off: it no longer applies, and RAP
builds emit objtool `no-cfi indirect call!` notes that it would turn into errors.
