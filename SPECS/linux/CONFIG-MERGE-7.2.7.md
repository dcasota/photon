# 7.2.7 kernel config merge (experimental/linux-7.2.7)

Photon's check_for_config_applicability.inc runs make olddefconfig
and diffs the result against the shipped 6.12 config_*. That diff is
expected on 7.2.7.

## Strategy

1. Keep the 6.12 config_x86_64 / config-esx_x86_64 as policy input.
2. In %prep, replace the applicability include with olddefconfig,
   disable DEBUG_INFO_BTF and IO_URING_BPF_OPS, olddefconfig again.
3. After first successful %prep, copy sandbox .config back into SPECS/linux/
   if the official check should be re-enabled.

Do not start from make defconfig.

## io_uring

- CONFIG_IO_URING: keep (Photon 6.12 policy)
- CONFIG_IO_URING_ZCRX: keep (def_bool y, zero-copy RX)
- CONFIG_IO_URING_BPF: accept def_bool default
- CONFIG_IO_URING_BPF_OPS: off via DEBUG_INFO_BTF=n (bpf_io_reg loop_step)

Runtime: sysctl kernel.io_uring_disabled=1
