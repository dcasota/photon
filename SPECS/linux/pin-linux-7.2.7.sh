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
}

inject_config_merge() {
  spec="$1"
  needle="$2"
  [ -f "$spec" ] || return 0
  python3 - "$spec" "$needle" << 'PY'
import re, sys
from pathlib import Path
spec, needle = Path(sys.argv[1]), sys.argv[2]
text = spec.read_text()
block = (
    "# 7.2.7 config merge: Photon policy kept, obsolete 6.12 symbols dropped.\n"
    "# bpftool BUILD_BPF_SKEL dumps BTF from vmlinux -- keep DEBUG_INFO_BTF.\n"
    "# IO_URING_ZCRX stays. IO_URING_BPF_OPS may follow BTF; accepted here.\n"
    "make ARCH=%{arch} LC_ALL= olddefconfig\n"
    "if [ -x scripts/config ]; then\n"
    "  scripts/config --enable DEBUG_INFO || :\n"
    "  scripts/config --enable DEBUG_INFO_BTF || :\n"
    "  scripts/config --disable IO_URING_BPF_OPS || :\n"
    "  make ARCH=%{arch} LC_ALL= olddefconfig\n"
    "fi"
)
new_text, n = re.subn(
    r"# 7\\.2\\.7 config merge:.*?\\n(?:# .*\\n)*make ARCH=%\\{arch\\} LC_ALL= olddefconfig\\n"
    r"if \\[ -x scripts/config \\\]; then\\n(?:  scripts/config .*\\n)*"
    r"  make ARCH=%\\{arch\\} LC_ALL= olddefconfig\\nfi",
    block, text, count=1, flags=re.S,
)
if n:
    spec.write_text(new_text)
    print(f"[runPh7-2-7] {spec}: refreshed 7.2.7 config merge")
    raise SystemExit(0)
old_inc = f"%include {needle}"
if old_inc in text:
    spec.write_text(text.replace(old_inc, block, 1))
    print(f"[runPh7-2-7] {spec}: injected 7.2.7 config merge")
    raise SystemExit(0)
simple = "make ARCH=%{arch} olddefconfig"
if simple in text and "7.2.7 config merge" not in text:
    spec.write_text(text.replace(simple, block, 1))
    print(f"[runPh7-2-7] {spec}: upgraded one-line olddefconfig to merge block")
    raise SystemExit(0)
print(f"[runPh7-2-7] WARNING: no config-check include in {spec}", file=sys.stderr)
PY
}

cd "$BASE_DIR/$RELEASE_BRANCH" || exit 1
pin_727 SPECS/linux/linux.spec SPECS/linux/linux.spec.7.2.7.patch
pin_727 SPECS/linux/linux-esx.spec SPECS/linux/linux-esx.spec.7.2.7.patch
sync_cve_include
disable_unrebased_ranges SPECS/linux/linux.spec
disable_unrebased_ranges SPECS/linux/linux-esx.spec
inject_config_merge SPECS/linux/linux.spec '%{SOURCE7}'
inject_config_merge SPECS/linux/linux-esx.spec '%{SOURCE4}'

pin_rust_locale() {
  spec="SPECS/rust/rust.spec"
  [ -f "$spec" ] || spec=$(find SPECS -name rust.spec 2>/dev/null | head -n1)
  [ -n "$spec" ] && [ -f "$spec" ] || return 0
  grep -q 'export LANG=C' "$spec" && return 0
  grep -q '^%build' "$spec" && sed -i '/^%build/a export LANG=C\nexport LC_ALL=C' "$spec"
}
pin_rust_locale
