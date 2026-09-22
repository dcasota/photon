# CVE patches shared across all Linux kernel flavours
# Patch range reserved: 3000-3999
#
# experimental/linux-7.2.7: this series is the Photon 5 / 6.12.x stable
# backport set. It does not apply to Linux 7.2.7 (context moved or already
# upstream). Leave the range empty so `%autopatch -p1 -m3000 -M3999` is a
# no-op. Re-enable individual patches here only after they are rebased.
