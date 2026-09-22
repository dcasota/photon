# Sourced by runPh7-2-7.sh after downstream-fixes.patch.
# Expects BASE_DIR, COMMON_BRANCH, RELEASE_BRANCH.
# See SPECS/linux/CONFIG-MERGE-7.2.7.md.

pin_727() {
  spec="$1"
  patch="$2"
  [ -f "$spec" ] || return 1
  if grep -q '^Version:[[:space:]]*7.2.7' "$spec"; then
    echo "[runPh7-2-7] $spec already Version 7.2.7"
  elif [ -f "$patch" ] && patch -p1 --forward --dry-run < "$patch" >/dev/null 2>&1; then
    patch -p1 --forward < "$patch" && echo "[runPh7-2-7] Applied $(basename "$patch")"
  else
    echo "[runPh7-2-7] WARNING: pin patch missed for $spec; forcing Version/Source0/fips with sed"
    sed -i 's/^Version:[[:space:]]*6\.12\.[0-9]\+/Version:        7.2.7/' "$spec"
    sed -i 's#pub/linux/kernel/v6.x/linux-#pub/linux/kernel/v7.x/linux-#' "$spec"
    awk 'BEGIN{done=0} /%global fips 1/ && !done {sub(/%global fips 1/,"%global fips 0"); done=1} {print}' \
      "$spec" > "$spec.pin" && mv "$spec.pin" "$spec"
  fi
}

write_empty_cve_inc() {
  cat > "$1" << 'CVEINC'
# CVE patch range 3000-3999 left empty on experimental linux 7.2.7.
# 6.12-stable backports do not apply to 7.2.7. Do not put percent-tokens
# or backticks in this file; rpm expands them even in comments.
CVEINC
}

sync_cve_include() {
  inc="SPECS/linux/kernel_cve_patches.inc"
  mkdir -p SPECS/linux
  if git remote get-url origin >/dev/null 2>&1; then
    git fetch origin "${RELEASE_BRANCH}" 2>/dev/null || git fetch origin 2>/dev/null || true
    if git show "origin/${RELEASE_BRANCH}:${inc}" >/dev/null 2>&1; then
      git checkout -f "origin/${RELEASE_BRANCH}" -- "$inc" 2>/dev/null || true
    fi
  fi
  if [ ! -f "$inc" ] || grep -qE '^[[:space:]]*Patch[0-9]+' "$inc"; then
    write_empty_cve_inc "$inc"
  fi
  echo "[runPh7-2-7] $inc has no Patch lines"
}

disable_unrebased_ranges() {
  spec="$1"
  [ -f "$spec" ] || return 0
  sed -i -E '/^%autopatch /{ /-m0 -M49/b; s/.*/# unrebased autopatch range skipped for 7.2.7/; }' "$spec"
  sed -i -E '/^Patch([2-9]|[1-4][0-9]):/d' "$spec"
  echo "[runPh7-2-7] $spec: only Patch0/1 + %autopatch 0-49 left"
}

inject_config_merge() {
  spec="$1"
  needle="$2"
  [ -f "$spec" ] || return 0
  python3 - "$spec" "$needle" << 'PY'
import sys
from pathlib import Path
spec, needle = Path(sys.argv[1]), sys.argv[2]
text = spec.read_text()
block = (
    "# 7.2.7 config merge: Photon policy kept, obsolete 6.12 symbols dropped.\n"
    "# IO_URING_ZCRX is def_bool y (zero-copy RX) -- leave it.\n"
    "# IO_URING_BPF is def_bool y if BPF+NET -- olddefconfig restores it.\n"
    "# IO_URING_BPF_OPS needs DEBUG_INFO_BTF; keep BTF off so bpf_io_reg\n"
    "# loop_step cannot attach to another task ring.\n"
    "make ARCH=%{arch} LC_ALL= olddefconfig\n"
    "if [ -x scripts/config ]; then\n"
    "  scripts/config --disable DEBUG_INFO_BTF || :\n"
    "  scripts/config --disable IO_URING_BPF_OPS || :\n"
    "  make ARCH=%{arch} LC_ALL= olddefconfig\n"
    "fi\n"
)
if "7.2.7 config merge" in text:
    print(f"[runPh7-2-7] {spec} already has config merge")
    raise SystemExit(0)
old_inc = f"%include {needle}"
old_simple = "make ARCH=%{arch} olddefconfig"
if old_inc in text:
    text = text.replace(old_inc, block.rstrip("\n"), 1)
elif old_simple in text:
    text = text.replace(old_simple, block.rstrip("\n"), 1)
else:
    print(f"[runPh7-2-7] WARNING: no config-check include in {spec}")
    raise SystemExit(0)
spec.write_text(text)
print(f"[runPh7-2-7] {spec}: injected 7.2.7 config merge")
PY
}
