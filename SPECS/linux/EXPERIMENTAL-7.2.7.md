# experimental/linux-7.2.7

Photon 5.0 userland with Linux **7.2.7** from kernel.org.

| Field | Value |
|---|---|
| Base branch | `5.0` (`c21dd8d0`) |
| Kernel | 7.2.7 |
| Tarball | https://cdn.kernel.org/pub/linux/kernel/v7.x/linux-7.2.7.tar.xz |
| sha512 | `9a7ee3e35e1e4eea44fd2fadce7b51deb9cae8b1e19ed4d8dc1e59d2e310ffa6dae508a9b0919d2d3cd29d00ca79fd473e7540a3cfb1124e56c4de091915a9d9` |
| git tag (peeled) | `f42acb3678424d1e08f6ed27c0d8ba8a125e14d6` |
| Dist tag | `.ph5` (unchanged) |
| FIPS / canister | **off** (`%global fips 0` on x86_64) |
| Patches | still the 6.12 Photon set — expect `%autopatch` failures |

`runPh7-2-7.sh` in `dcasota/photonos-scripts` re-pins `linux.spec` / `linux-esx.spec` after `downstream-fixes.patch` so a worktree restore cannot silently revert to 6.12.109.
