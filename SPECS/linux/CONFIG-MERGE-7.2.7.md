# 7.2.7 kernel config merge (experimental/linux-7.2.7)

Photon's check_for_config_applicability.inc diffs olddefconfig against
the shipped 6.12 config_*. That diff is expected on 7.2.7.

## Strategy

1. Keep 6.12 config_x86_64 / config-esx_x86_64 as policy input.
2. In %prep, replace the applicability include with olddefconfig,
   enable DEBUG_INFO and DEBUG_INFO_BTF (bpftool BUILD_BPF_SKEL dumps
   BTF from vmlinux), try IO_URING_BPF_OPS=n, olddefconfig again.
3. After successful %prep, copy sandbox .config back to SPECS/linux/
   if the official check should be re-enabled.

Do not start from make defconfig.

## io_uring

- CONFIG_IO_URING: keep
- CONFIG_IO_URING_ZCRX: keep (def_bool y)
- CONFIG_IO_URING_BPF: accept default
- CONFIG_IO_URING_BPF_OPS: prefer off; accepted on if BTF requires it
- DEBUG_INFO_BTF: on (bpftool)

Runtime: sysctl kernel.io_uring_disabled=1

Wrapper exports LANG=C and injects it into rust.spec %build.
