# experimental/linux-7.3

Photon 5.0 userland with the Linux **7.3** mainline release from kernel.org, on the
per-subrelease kernel layout of 5.0: the kernel of subrelease 92 lives in `SPECS/92/linux`.
Based on 5.0 `727909c4b8`; the kernel files of `experimental/linux-7.3-rc4` moved here and
ported to the final release.

| Field | Value |
|---|---|
| Base | 5.0 `727909c4b8` |
| Kernel | 7.3 (mainline release, 2026-10-18) |
| Tarball | https://cdn.kernel.org/pub/linux/kernel/v7.x/linux-7.3.tar.xz |
| sha512 | `14b99ea7cc2adc0798a183ac5f3e184587f2496c3b2d1d53b625574389891c69e8be375b5d03875fe859b09ac9314aa15da604087274ba815671135bd6a0e590` |
| Signature | `linux-7.3.tar.sign`, Greg Kroah-Hartman `647F28654894E3BD457199BE38DBBDC86092693E` |
| RPM version | `Version: 7.3.0`, `Release: 1%{?dist}` |
| uname -r | `7.3.0-1.ph5` (`linux`), `7.3.0-1.ph5-esx` (`linux-esx`) |
| Dist tag | `.ph5` (unchanged) |
| Patches | Patch0 + Patch1, RAP/KCFI Patch61 (`secure/0001-gcc-rap-plugin-with-kcfi-7.3.patch`) and Patch63 for `linux`, rdrand hwrng Patch6 and vmwgfx blend mode Patch7300 for both flavours; other 6.12 ranges and the CVE include skipped |
| FIPS / canister | for a canister build only: the series in `fips-7.3/` (`manifest.json`), LKCM 7.3 |

`runPh7-3.sh` in `dcasota/photonos-scripts` (or `sharukhan build-iso --kernel 7.3`) applies the
spec changes at build time, so the committed `linux.spec` / `linux-esx.spec` stay as on 5.0.
The kernel directory is read from the tree (the directory whose `linux.spec` builds the tree's
`photon-subrelease`), never assumed.

Every patch on this branch is judged at `--fuzz=0` on pristine 7.3 by an `rpmbuild -bp` replay
of the pinned specs, the FIPS series included (see the commit that ported each one).
