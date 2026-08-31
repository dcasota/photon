#!/usr/bin/env python3

import calendar
import json
import os
import re
import sys
import license_expression
import operator

from datetime import datetime

sys.path.append(
    f"{os.path.dirname(os.path.realpath(__file__))}/../package-builder"
)
from CommandUtils import CommandUtils

from pyrpm.spec import Spec, replace_macros
from source_archive_validator import SourceArchiveChecker

cfg_dict = {}
cfg_fn = "check-spec-cfg.json"

specPaths = []
distTag = ""

source_regex = re.compile(r"^(Source\d*\s*):\s*(.+)", re.IGNORECASE)
patch_regex = re.compile(r"^([#]*Patch\d*\s*):\s*(\S+)", re.IGNORECASE)

scriptPath = os.path.dirname(os.path.realpath(__file__))
with open(f"{scriptPath}/{cfg_fn}", "r") as f:
    cfg_dict = json.load(f)

g_ignore_list = []
g_mainline = ""

# ---------------------------------------------------------------------------
# Build toggle parse matrix
#
# A spec is normally parsed exactly once, in whatever single configuration its
# own defaults select. Conditional code behind a build toggle is therefore
# never parsed and silently rots (dangling patches, duplicate Patch indices,
# ...). The matrix re-parses each spec with every toggle it actually reads
# forced to each of its meaningful values.
#
# The table is data driven on purpose: to cover a new toggle add one entry
# here, or override/extend it from check-spec-cfg.json with a
# "parse_matrix_toggles" object of the same shape. No code change needed.
#
# Note: only toggles the spec really reads are swept, and only toggles listed
# here - sweeping every %{?foo} in the tree would multiply the runtime for no
# benefit.
# ---------------------------------------------------------------------------
parse_matrix_toggles = {
    "STIG_HARDEN": ["0", "1"],
    "fips": ["0", "1"],
    "canister_build": ["0", "1"],
    "acvp_build": ["0", "1"],
    "kat_build": ["0", "1"],
}
parse_matrix_toggles.update(cfg_dict.get("parse_matrix_toggles", {}))

# "<pkgdir>/<spec>.spec" entries whose unconditional pin of a build toggle is
# deliberate, e.g. a flavour that must never select the other branch. Prefer
# fixing the spec with "%{!?NAME: %global NAME <default>}", which keeps the
# default and still lets -D reach the other branch.
parse_matrix_ignore_pinned = cfg_dict.get("parse_matrix_ignore_pinned", [])

# %{NAME} / %{?NAME} / %{!?NAME: ...} / %if 0%{?NAME}  -> a toggle the spec reads
toggle_ref_regex = re.compile(r"%\{[!?]*([A-Za-z_][A-Za-z0-9_]*)[:}]")
# %define NAME <value> / %global NAME <value>
toggle_def_regex = re.compile(r"^\s*%(?:define|global)\s+([A-Za-z_][A-Za-z0-9_]*)\s+(.*?)\s*$")
# %if 0%{photon_subrelease} >= 91  -> the spec varies with the subrelease
subrel_cond_regex = re.compile(r"^\s*%if.*%\{\??photon_subrelease\}\s*(>=|<=|==|>|<)\s*(\d+)")
# %global build_if %{photon_subrelease} >= 91  -> subreleases the spec supports
build_if_regex = re.compile(r"^\s*%global\s+build_if\s+%\{\??photon_subrelease\}\s*(>=|<=|==|>|<)\s*(\d+)")
# conditional nesting, so that a %define inside %if is not mistaken for a pin
cond_open_regex = re.compile(r"^\s*%if(arch|narch|os|nos|\b)")
cond_close_regex = re.compile(r"^\s*%endif\b")
# Source<N>:/Patch<N>: lines of a parsed spec
parsed_src_regex = re.compile(r"^(?:Source|Patch)\d*\s*:\s*(\S+)", re.IGNORECASE)

cmp_ops = {
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
    "==": operator.eq,
}


def pr_err(msg):
    print(msg, file=sys.stderr)


"""
Error Dictionary:
    - Stores all error messages in a dictionary
    - Prints all error messages section by section
    - Errors will be printed only after parsing whole spec
"""


class ErrorDict:
    def __init__(self, spec_fn):
        self.spec_fn = spec_fn
        self.err_dict = {
            "hdr_check": ["Spec header errors"],
            "version_check": ["Version check errros"],
            "dist_tag": ["Dist tag error"],
            "unallowed_usages": ["Trailing spaces & empty line errors"],
            "bogus_date": ["Bogus date errors"],
            "changelog": ["Changelog erros"],
            "sub_pkg": ["Sub package errors"],
            "configure": ["Configure erros"],
            "setup": ["Setup errors"],
            "_smp_mflags": ["_smp_mflags errors"],
            "unused_files": ["List of unused files"],
            "license": ["License errors"],
            "cfgYml": ["Config Yaml errors"],
            "parse_matrix": ["Build toggle parse matrix errors"],
            "others": ["Other errors"],
        }

    # keep err message in a given section
    # if section not found, put it in others
    def update_err_dict(self, sec, err_msg):
        sec = sec if sec in self.err_dict else "others"

        if sec in self.err_dict:
            self.err_dict[sec].append(err_msg)
            # this removes duplicates from list
            self.err_dict[sec] = list(dict.fromkeys(self.err_dict[sec]))

    def print_err_dict(self):
        pr_flg = False

        for k, v in self.err_dict.items():
            # proceed if error list has more than 1 item
            try:
                v[1]
            except IndexError:
                continue

            if not pr_flg:
                pr_err(
                    f"--- List of errors in {self.spec_fn} ---"
                )
                pr_flg = True

            print("\n --- %s ---" % (v[0]))

            for msg in v[1:]:
                if k == "unused_files":
                    pr_err(msg)
                else:
                    pr_err(f"ERROR in {self.spec_fn}: {msg}")

        pr_err("\n")


def check_spec_header(spec, err_dict):
    ret = False
    sec = "hdr_check"

    # items in the following dict are mandatory part of spec header
    header = {
        "Name": spec.name,
        "Version": spec.version,
        "Release": spec.release,
        "License": spec.license,
        "Vendor": spec.vendor,
        "Summary": spec.summary,
        "Group": spec.group,
        "Distribution": spec.distribution,
        "URL": spec.url,
    }

    for key, val in header.items():
        err_msg = None

        if not val:
            err_msg = f"{key} must be present in the spec header"
        elif key == "Distribution" and val and val != "Photon":
            err_msg = f"{key} name must be Photon (Given: {val})"
        elif key == "Vendor" and spec.vendor and spec.vendor != "VMware, Inc.":
            err_msg = f"{key} name must be VMware, Inc. (Given: {val})"

        if err_msg:
            ret = True
            err_dict.update_err_dict(sec, err_msg)

    return ret


# check for version in spec header against latest changelog entry
def check_for_version(spec, err_dict):
    ret = False
    sec = "version_check"

    clog = spec.changelog.splitlines()
    changelog_ver = clog[0].split()[-1]

    # combine Release & Version from header, without the %{?...} part
    release_ver = f"{spec.version}-" + spec.release.split("%{?", maxsplit=1)[0]

    if changelog_ver != release_ver:
        err_msg = ("Changelog & Release version mismatch " "%s != %s") % (
            changelog_ver,
            release_ver,
        )
        err_dict.update_err_dict(sec, err_msg)
        ret = True

    return ret


def check_for_dist_tag(spec, err_dict):
    ret = False
    sec = "dist_tag"

    if "%{?dist}" not in spec.release:
        err_msg = "%%{?dist} tag not found in Release: %s" % (spec.release)
        err_dict.update_err_dict(sec, err_msg)
        ret = True

    return ret


def check_for_unallowed_usages(spec_fn, err_dict):
    ret = False
    ret_dict = {}
    sec = "unallowed_usages"

    with open(spec_fn, "r") as fp:
        lines = fp.read().splitlines()

    if lines[-1].isspace():
        err_msg = "empty last line found, not needed"
        err_dict.update_err_dict(sec, err_msg)
        ret = True

    key_found = False
    empty_line_count = 0
    for line_num, line in enumerate(lines):
        if "\t" in line:
            err_msg = f"TAB character(s) found in line {line_num + 1}"
            err_dict.update_err_dict(sec, err_msg)
            ret = True

        if not line or line.isspace():
            empty_line_count += 1
        else:
            empty_line_count = 0

        if empty_line_count >= 2:
            err_msg = (
                f"multiple empty lines found at line number {line_num + 1}"
            )
            err_dict.update_err_dict(sec, err_msg)
            empty_line_count = 0
            ret = True

        if line.endswith((" ", "\t")):
            err_msg = (
                "trailing space(s) found at line number: %s:\n" "%s"
            ) % (
                line_num + 1,
                line,
            )
            err_dict.update_err_dict(sec, err_msg)
            ret = True

        if not line.startswith("#") and "RPM_BUILD_ROOT" in line:
            err_msg = (
                "legacy $RPM_BUILD_ROOT found at line: %s\n%s - "
                "use %%{buildroot} instead"
            ) % (line_num + 1, line)
            err_dict.update_err_dict("others", err_msg)
            ret = True

        if line.startswith("%prep"):
            key_found = True
        elif line.startswith("%files"):
            key_found = False

        if key_found:
            ret_dict.update({line_num: line})

    return ret, ret_dict


# check against weekday abbreviation for the given date in changelog
def check_for_bogus_date(line, cur_date, err_dict):
    ret = False
    sec = "bogus_date"

    day_abbr = calendar.day_abbr[cur_date.weekday()]
    if day_abbr != line[1]:
        err_msg = f"bogus date found at:\n{line}"
        err_dict.update_err_dict(sec, err_msg)
        ret = True

    return ret


# No empty lines allowed in changelog
# Changelog lines should start with '*', '-' or ' '
# '-' & ' ' should not be present before '*'
# Successive lines starting with '*' not allowed
def check_changelog(spec, err_dict):
    ret = False
    hyphen = True
    asterisk = False
    sec = "changelog"
    date_format = "%a-%b-%d-%Y"
    prev_date = {"date": None, "entry": None}

    changelog = spec.changelog.splitlines()

    for line in changelog:
        err_msg = None
        if not line:
            err_msg = "empty line in changelog"
            err_dict.update_err_dict(sec, err_msg)
            ret = True
            continue

        if line.startswith("*"):
            asterisk = True
            if not hyphen:
                err_msg = f"Successive author & version info at:\n{line}"
                err_dict.update_err_dict(sec, err_msg)
                ret = True
            hyphen = False
        elif line.startswith("-"):
            hyphen = True
            if not asterisk:
                err_msg = (
                    "description given before author & version info at:" "\n%s"
                ) % (line)
                err_dict.update_err_dict(sec, err_msg)
                ret = True
            continue
        elif line.startswith(" ") and asterisk and hyphen:
            continue
        else:
            err_msg = f"invalid entry in changelog at: {line}"
            err_dict.update_err_dict(sec, err_msg)
            ret = True
            continue

        line_str = line
        line = line.split()

        # line[1] is week name, line[2] is month name
        d, m = line[1], line[2]
        if not (d.istitle() and m.istitle()):
            err_msg = (
                f"Day-'{d}' or Month-'{m}' name is improper, use proper case"
            )
            err_dict.update_err_dict(sec, err_msg)
            ret = True

        date_text = "-".join(line[1:5])
        try:
            cur_date = datetime.strptime(date_text, date_format)
        except ValueError:
            err_msg = f"-{date_text}-"
            err_dict.update_err_dict(sec, err_msg)
            ret = True
            continue

        if check_for_bogus_date(line, cur_date, err_dict):
            ret = True

        # dates should be in chronological order
        if prev_date["date"] and cur_date > prev_date["date"]:
            err_msg = (
                "dates not in chronological order in between:\n" "%s and\n%s"
            ) % (line_str, prev_date["entry"])
            err_dict.update_err_dict(sec, err_msg)
            ret = True

        prev_date["date"] = cur_date
        prev_date["entry"] = line_str

    return ret


def check_sub_pkg(spec, err_dict):
    ret = False
    sec = "sub_pkg"

    for pkg in spec.packages:
        err_msg = ""
        if pkg.is_subpackage:
            if pkg.build_requires:
                err_msg = f"BuildRequires found in sub package {pkg}\n"

            subpkg_hdr = [pkg.name, pkg.summary, pkg.description]
            if "" in subpkg_hdr or None in subpkg_hdr:
                err_msg += (
                    "One of Name/Summary/Description is missing in sub"
                    " package %s"
                ) % (pkg)

            if err_msg:
                ret = True
                err_dict.update_err_dict(sec, err_msg)

    return ret


def check_for_configure(lines_dict, err_dict):
    ret = False
    sec = "configure"

    opt_list = ["prefix", "exec-prefix", "bindir" "sbindir" "libdir"]
    opt_list += ["includedir", "sysconfdir", "datadir", "libexecdir"]
    opt_list += ["sharedstatedir", "mandir", "infodir", "localstatedir"]

    lines = list(lines_dict.values())

    def check_for_opt(line):
        ret = False

        for opt in opt_list:
            opt = f"--{opt}"
            if line.find(opt) >= 0:
                err_msg = f"{opt} can be omitted when using %%configure"
                err_dict.update_err_dict(sec, err_msg)
                ret = True

        return ret

    # options in opt_list can be in same line or in continued line
    for idx, line in enumerate(lines):
        err_msg = None
        if line.startswith("./configure") or line.startswith("%configure"):
            if line.startswith("./configure"):
                err_msg = "Use %%configure instead of ./configure"
                err_dict.update_err_dict(sec, err_msg)
                ret = True

            prev_line = lines[idx - 1]
            if prev_line.endswith("\\"):
                err_msg = (
                    "Trailing backslash before configure found."
                    " Use export instead"
                )

                err_dict.update_err_dict(sec, err_msg)
                ret = True

            _ret = check_for_opt(line)
            ret = True if ret else _ret
            # if configure is multi lined
            while line.endswith("\\"):
                idx += 1
                line = lines[idx]
                _ret = check_for_opt(line)
                ret = True if ret else _ret

    return ret


def check_setup(lines_dict, err_dict):
    ret = False
    sec = "setup"
    bypass_str = "# Using autosetup is not feasible"

    lines = list(lines_dict.values())

    for idx, line in enumerate(lines):
        if line.startswith("%autosetup"):
            continue

        if line.startswith("%setup"):
            if lines[idx - 1] == bypass_str:
                continue
            err_msg = (
                "\nUse %%autosetup instead of %%setup\n"
                "If using %%autosetup is not feasible, "
                "put the following comment '%s' right "
                "above your every %%setup command"
            ) % (bypass_str)
            err_dict.update_err_dict(sec, err_msg)
            ret = True

    return ret


def check_make_smp_flags(lines_dict, err_dict):
    ret = False
    sec = "_smp_mflags"
    bypass_str = "# make doesn't support _smp_mflags"

    err_msg = (
        "(at line number {line}): Use _smp_mflags with make\n"
        "If using _smp_mflags is not feasible, put the following "
        "comment '{bstr}' right above your every make "
        "command"
    )

    lines = list(lines_dict.values())
    line_nums = list(lines_dict.keys())

    for idx, line in enumerate(lines):

        if (
            (not line.startswith("make"))
            or (lines[lines.index(line) - 1] == bypass_str)
            or (sec in line)
        ):
            continue

        if re.split("[^a-z]", line)[0] != "make":
            continue

        flag_found = False
        while lines[idx] and lines[idx].endswith("\\"):
            idx += 1
            if sec in lines[idx]:
                flag_found = True
                break

        if not flag_found:
            e_msg = err_msg.format(line=line_nums[idx] + 1, bstr=bypass_str)
            err_dict.update_err_dict(sec, e_msg)
            ret = True

    return ret


def check_mentioned_but_unused_files(spec_fn, dirname, subrelease):
    parsed_spec, _, _ = CommandUtils.runCmd(
        ["rpmspec", "-D", f"_sourcedir {dirname}", "-D", f"photon_subrelease {subrelease}", "-P", spec_fn],
        capture=True,
    )

    parsed_spec = parsed_spec.split("\n")

    # ignore everything after %changelog
    # patch & sources get used much earlier
    idx = parsed_spec.index("%changelog")
    parsed_spec = parsed_spec[:idx]

    source_patch_list = []
    for line in parsed_spec:
        if re.search(source_regex, line) or re.search(patch_regex, line):
            fn = os.path.basename(line.split()[1])
            source_patch_list.append(fn)
        elif source_patch_list:
            for fn in source_patch_list[:]:
                # there can be multiple sources mentioned in same line
                # so don't break after first hit
                if f"{dirname}/{fn}" in line:
                    source_patch_list.remove(fn)

    return source_patch_list


def get_source_patches_from_all_specs(spec_fn, dirname):
    sources = []
    patches = []
    other_files = []

    for _, _, fns in os.walk(dirname):
        for fn in fns:
            if not fn.endswith(".spec"):
                fn = os.path.basename(fn)
                other_files.append(fn)
                continue

            if fn == os.path.basename(spec_fn):
                fn = spec_fn
            else:
                fn = create_altered_spec(f"{dirname}/{fn}")

            tmp = getSpecObj(fn)
            if fn != spec_fn:
                os.remove(fn)

            sources.extend(tmp.sources)
            patches.extend(tmp.patches)

    other_files = [f for f in other_files if f not in sources + patches]

    return sources, patches, other_files


def check_for_unused_files(spec_fn, err_dict, dirname, subrelease):
    global g_ignore_list

    g_ignore_list += cfg_dict["ignore_unused_files"].get(dirname, [])
    g_ignore_list += cfg_dict["global_ignore_list"]

    ret = False
    sec = "unused_files"

    if not hasattr(check_for_unused_files, "prev_dir"):
        check_for_unused_files.prev_dir = None

    if not hasattr(check_for_unused_files, "prev_ret"):
        check_for_unused_files.prev_ret = None

    if dirname == check_for_unused_files.prev_dir:
        return check_for_unused_files.prev_ret

    check_for_unused_files.prev_dir = dirname

    sources, patches, other_files = get_source_patches_from_all_specs(
        spec_fn, dirname
    )

    ret = check_spec_cfg_yml(sources, dirname, err_dict)

    source_patch_list = sources + patches

    # keep only basenames in source list
    source_patch_list = [os.path.basename(s) for s in source_patch_list]

    mentioned_but_unused = check_mentioned_but_unused_files(spec_fn, dirname, subrelease)
    for fn in mentioned_but_unused[:]:
        if fn in g_ignore_list:
            mentioned_but_unused.remove(fn)

    if mentioned_but_unused:
        msg = (
            "\nSome mentioned but unused files found in the spec.\n"
            "If you think it's a false positive, try the following methods:\n"
            "- If you are using Photon OS, update rpm version to latest using tdnf and retry\n"
            "- If you are using any other distro, contact - 'shreenidhi.shedi@broadcom.com'\n"
        )
        pr_err(msg)

    fns = list(set(other_files) - set(source_patch_list))
    for fn in fns[:]:
        if fn in g_ignore_list:
            fns.remove(fn)

    if not fns and not mentioned_but_unused:
        check_for_unused_files.prev_ret = ret
        return ret

    ret = True
    err_msg = f"List of unused files in: {dirname}"
    err_dict.update_err_dict(sec, err_msg)
    for r, _, _fns in os.walk(dirname):
        for _fn in _fns:
            if _fn in fns or _fn in mentioned_but_unused:
                # needed for Source0 unused type of errors
                if _fn in mentioned_but_unused:
                    mentioned_but_unused.remove(_fn)
                _fn = os.path.join(r, _fn)
                err_dict.update_err_dict(sec, _fn)

    # needed for Source0 unused type of errors
    for item in mentioned_but_unused:
        err_dict.update_err_dict(sec, item)

    check_for_unused_files.prev_ret = ret

    return ret


def check_spec_cfg_yml(srcs, specDir, err_dict):
    checker = SourceArchiveChecker()
    checker.scanDirectory(specDir)
    archiveMap = checker.getArchiveMap()

    def get_non_local_files(rootDir, fList):
        foundFiles = []
        for _, _, fns in os.walk(rootDir):
            foundFiles.extend(fns)

        ret = []
        for f in fList:
            f = os.path.basename(f)
            if f in foundFiles:
                continue
            ret.append(f)

        return ret

    nonLocalsSrcs = set(get_non_local_files(specDir, srcs))
    archives = set(archiveMap.keys())

    only_in_nonlocals = nonLocalsSrcs - archives
    only_in_archives = archives - nonLocalsSrcs

    if only_in_nonlocals or only_in_archives:
        final_msg = "Mismatch between sources in config.yaml and spec:"
        if only_in_nonlocals:
            final_msg += f"\nOnly in spec file: {only_in_nonlocals}"
        if only_in_archives:
            final_msg += f"\nOnly in config.yaml: {only_in_archives}"

        err_dict.update_err_dict("cfgYml", final_msg)
        return True

    return False


def check_proper_spdx_license(spec, err_dict):
    sec = "license"
    bad_ids = ["unknown-spdx", "LicenseRef", "scancode"]
    spdx_licensing = license_expression.get_spdx_licensing()

    # for some reason, the license_expression package, which is used by the official spdx-tools
    # package, returns/uses the same database for both spdx and scancode licenses. So let's
    # do our own filtering here.
    for lic_sym in spdx_licensing.license_symbols(spec.license):
        for bad_id in bad_ids:
            if bad_id in lic_sym.key:
                err_dict.update_err_dict(
                    sec, f"Bad SPDX identifier {bad_id} in license expression!"
                )
                return True

    try:
        # create license expression object - throws an exception for any validation errors
        spdx_licensing.parse(spec.license, validate=True, strict=True)
    except Exception as e:
        err_dict.update_err_dict(
            sec, f"Caught exception while attempting to validate license: {e}"
        )
        return True

    return False


def check_subrelease_specs(specsList, mainline):
    # TODO: revisit this
    return False

    ret = False

    if not specsList:
        return ret

    pattern = re.compile(r'^\s*%global\s+build_if\s+%\{photon_subrelease\}\s+(.*)')
    cond_pattern = re.compile(r'(>=|<=|>|<|==)\s*(\d+)')

    ops = {
        ">": operator.gt,
        ">=": operator.ge,
        "<": operator.lt,
        "<=": operator.le,
        "==": operator.eq
    }

    def comparator(match, subrel, spec):
        expr = match.group(1).strip()

        m = cond_pattern.search(expr)
        if not m:
            return None

        op, val = m.groups()
        val = int(val)
        assert val >= 90, f"photon_subrelease should be >= 90 - {spec}"
        assert val <= mainline, f"photon_subrelease should be <= {mainline}: {spec}"
        return ops[op](subrel, int(val))

    def build_if_check(path):
        with open(path) as f:
            for line in f:
                m = pattern.search(line)
                if m:
                    return False, m
        return True, None

    for rel in range(90, mainline):
        for specDir in specPaths:
            rel_dir = f"{specDir}/{rel}"
            for specFile in specsList:
                branched = False
                v1 = False
                v2 = False

                subRelSpec = f"{rel_dir}/{specFile}"
                mainSpec = f"{specDir}/{specFile}"

                spec_base_name = os.path.basename(mainSpec)

                if os.path.isfile(subRelSpec):
                    branched = True
                    r, m = build_if_check(subRelSpec)
                    if r:
                        pr_err(f"ERROR: subrel: {spec_base_name} does not contain %global build_if")
                        ret = True
                    else:
                        cmp_rel = comparator(m, mainline, subRelSpec)
                        if cmp_rel:
                            pr_err(f"ERROR1: subrel: {m.group(1)} in {spec_base_name} is wrong")
                            ret = True

                        v1 = comparator(m, rel, subRelSpec)
                        if not v1:
                            pr_err(f"ERROR2: subrel: {m.group(1)} in {spec_base_name} is wrong")
                            ret = True

                if os.path.isfile(mainSpec):
                    r, m = build_if_check(mainSpec)
                    if r and branched:
                        pr_err(f"ERROR: main: {spec_base_name} does not contain %global build_if")
                        ret = True
                        continue

                    if not m:
                        continue

                    cmp_main = comparator(m, mainline, mainSpec)
                    if not cmp_main:
                        if "SPECS/linux/" not in mainSpec:
                            pr_err(f"ERROR1: main: {m.group(1)} in {spec_base_name} is wrong")
                            ret = True
                        else:
                            pr_err(f"WARNING1: main: {m.group(1)} in {spec_base_name} is wrong")
                            pr_err("This will soon be treated as hard error, please fix it")

                    v2 = comparator(m, rel, mainSpec)
                    if v2:
                        if "SPECS/linux/" not in mainSpec:
                            pr_err(f"ERROR2: main: {m.group(1)} in {spec_base_name} is wrong")
                            ret = True
                        else:
                            pr_err(f"WARNING2: main: {m.group(1)} in {spec_base_name} is wrong")
                            pr_err("This will soon be treated as hard error, please fix it")

                if v1 and v2:
                    pr_err(f"ERROR: {spec_base_name} has wrong photon_subrelease condition")
                    ret = True

    return ret


def find_file_in_dir(fn, path):
    for root_d, dirs, files in os.walk(path):
        if fn in files:
            return f"{root_d}/{fn}"


def create_altered_spec(spec_fn):
    global g_ignore_list

    lines = []

    with open(spec_fn, "r") as fp:
        lines = fp.readlines()

    sources = {}
    output = []
    dirname = os.path.dirname(spec_fn)

    # find the included files, add the file name to g_ignore_list
    # replace %include <file> with actual content of <file>
    for line in lines:
        if line.lower().startswith("buildarch"):
            line = f"#{line}"

        if not line.startswith("%include"):
            if re.search(source_regex, line):
                k, v = line.split()
                sources[k] = v
            output.append(f"{line}")
            continue

        _, included_fn = line.split()
        # %{SOURCEX} --> SOURCEX
        for c in {"{", "}", "%"}:
            included_fn = included_fn.replace(c, "")

        for k, v in sources.items():
            if k.replace(":", "").lower() == included_fn.lower():
                included_fn = v
                break

        included_fn = replace_macros(included_fn, getSpecObj(spec_fn))

        g_ignore_list.append(included_fn)
        included_fn = find_file_in_dir(included_fn, dirname)
        with open(included_fn, "r") as fp:
            for ln in fp.readlines():
                ln = ln.strip()
                if ln:
                    output.append(f"{ln}\n")

    altered_spec = f"/tmp/{os.path.basename(spec_fn)}"
    with open(f"{altered_spec}", "w") as fp:
        for ln in output:
            fp.write(ln)

    return altered_spec


def getSpecObj(spec_fn):
    macros = {"dist": distTag}
    spec = Spec.from_file(spec_fn, macros)
    return spec


def setSpecPaths():
    global specPaths
    global distTag

    topDir = os.path.realpath(f"{scriptPath}/../..")

    specPaths = [f"{topDir}/SPECS"]
    phCfgJson = f"{topDir}/build-config.json"

    with open(phCfgJson, "r") as f:
        data = json.load(f)

    distTag = data["photon-build-param"]["photon-dist-tag"]


def pm_scan_spec(spec_fn):
    """
    Scan a spec for the build toggles it actually reads and for the values of
    photon_subrelease it distinguishes.

    Returns (toggles, pinned, subrel_thresholds, build_if):
      toggles           - names from parse_matrix_toggles the spec refers to
      pinned            - {name: (lineno, text)} for toggles the spec %defines
                          unconditionally. rpm lets a spec body %define beat a
                          command line -D, so such a toggle cannot be forced.
      subrel_thresholds - integers the spec compares photon_subrelease against
                          in an %if
      build_if          - (op, value) of "%global build_if %{photon_subrelease}
                          <op> <value>", the subreleases the spec supports
    """
    toggles = set()
    pinned = {}
    subrel_thresholds = set()
    build_if = None
    depth = 0

    with open(spec_fn, "r") as fp:
        lines = fp.readlines()

    for idx, line in enumerate(lines):
        line = line.rstrip("\n")

        if line.lstrip().startswith("#"):
            continue

        m = build_if_regex.match(line)
        if m:
            build_if = (m.group(1), int(m.group(2)))
            # build_if is a plain %global, it never varies the parse itself
            continue

        m = subrel_cond_regex.match(line)
        if m:
            subrel_thresholds.add(int(m.group(2)))

        for name in toggle_ref_regex.findall(line):
            if name in parse_matrix_toggles:
                toggles.add(name)

        m = toggle_def_regex.match(line)
        if m and m.group(1) in parse_matrix_toggles:
            toggles.add(m.group(1))
            # A %define nested in %if/%ifarch is a legitimate derived value,
            # not a pin - only an unconditional one shadows -D for every cell.
            if depth == 0:
                pinned.setdefault(m.group(1), (idx + 1, line.strip()))

        if cond_open_regex.match(line):
            depth += 1
        elif cond_close_regex.match(line):
            depth = max(0, depth - 1)

    return toggles, pinned, subrel_thresholds, build_if


def pm_probe_spec(spec_fn, neutralize):
    """
    A spec body %define/%global wins over a command line -D, so for a toggle
    the spec pins unconditionally, forcing it does nothing at all. To still
    parse the code behind such a toggle, write a probe copy with those pins
    blanked out. Line count is preserved so that rpmspec diagnostics keep
    pointing at the line numbers of the real spec.

    Returns the original spec when there is nothing to neutralize.
    """
    if not neutralize:
        return spec_fn, False

    with open(spec_fn, "r") as fp:
        lines = fp.readlines()

    out = []
    for line in lines:
        line = line.rstrip("\n")
        m = toggle_def_regex.match(line)
        out.append("" if m and m.group(1) in neutralize else line)

    probe_fn = f"/tmp/parse-matrix-{os.getpid()}-{os.path.basename(spec_fn)}"
    with open(probe_fn, "w") as fp:
        fp.write("\n".join(out) + "\n")

    return probe_fn, True


def pm_parse_cell(probe_fn, dirname, macros):
    cmd = ["rpmspec", "-D", f"_sourcedir {dirname}"]
    for k, v in macros.items():
        cmd += ["-D", f"{k} {v}"]
    cmd += ["-P", probe_fn]

    out, err, rc = CommandUtils.runCmd(cmd, capture=True, ignore_rc=True)

    return out, err, rc


def pm_collect(parsed_spec):
    """
    Basenames of every Source/Patch the parsed cell selects. Remote sources are
    skipped, they are fetched and never expected to sit next to the spec.
    """
    files = set()

    for line in parsed_spec.split("\n"):
        if line.startswith("%changelog"):
            break

        m = parsed_src_regex.match(line)
        if m and "://" not in m.group(1):
            files.add(os.path.basename(m.group(1)))

    return files


def pm_subrelease_values(subrel_thresholds, build_if, subrelease, mainline):
    """
    Values of photon_subrelease worth parsing with: for every threshold the
    spec branches on, the value just below it and the value itself, restricted
    to the range the spec declares it supports via build_if.
    """
    values = set()

    for n in subrel_thresholds:
        values.update([n - 1, n])

    values = {v for v in values if 90 <= v <= int(mainline)}

    if build_if:
        op, val = build_if
        values = {v for v in values if cmp_ops[op](v, val)}

    values.discard(int(subrelease))

    return sorted(values)


def check_parse_matrix(spec_fn, err_dict, dirname, subrelease, mainline):
    """
    Parse the spec once per meaningful build configuration instead of only in
    the one its own defaults select, and report anything that only the other
    configurations reveal.
    """
    ret = False
    sec = "parse_matrix"

    toggles, pinned, subrel_thresholds, build_if = pm_scan_spec(spec_fn)

    # a deliberate pin is still neutralized, so its branch keeps being parsed,
    # only the finding is suppressed
    report_pinned = (
        "/".join(spec_fn.split("/")[-2:]) not in parse_matrix_ignore_pinned
    )

    cells = [("default", {}, frozenset())]

    for name in sorted(toggles):
        for val in parse_matrix_toggles[name]:
            neutralize = frozenset([name]) if name in pinned else frozenset()
            cells.append((f"{name}={val}", {name: val}, neutralize))

    for val in pm_subrelease_values(
        subrel_thresholds, build_if, subrelease, mainline
    ):
        cells.append((f"photon_subrelease={val}",
                      {"photon_subrelease": val}, frozenset()))

    if len(cells) == 1:
        # nothing conditional to sweep, the default parse is the whole matrix
        return ret

    if report_pinned:
        for name, (lineno, text) in sorted(pinned.items()):
            err_dict.update_err_dict(
                sec,
                f"build toggle {name} is declared but unreachable: '{text}' "
                f"at line {lineno} shadows -D {name} <value>, so the "
                f"conditional code behind {name} is never validated by a "
                f"normal build",
            )
            ret = True

    probe_specs = {}
    default_files = set()

    try:
        for name, macros, neutralize in cells:
            if neutralize not in probe_specs:
                probe_specs[neutralize] = pm_probe_spec(spec_fn, neutralize)

            probe_fn, _ = probe_specs[neutralize]

            cell_macros = {"photon_subrelease": subrelease}
            cell_macros.update(macros)

            out, err, rc = pm_parse_cell(probe_fn, dirname, cell_macros)

            macro_str = " ".join(f"-D '{k} {v}'" for k, v in cell_macros.items())

            if rc:
                err_dict.update_err_dict(
                    sec,
                    f"rpmspec failed for cell [{name}] "
                    f"({macro_str}):\n{err.strip()}",
                )
                ret = True
                continue

            files = pm_collect(out)

            if name == "default":
                default_files = files
                continue

            # Only files this cell brings in on top of the default parse are
            # reported. Whatever the default configuration already references
            # is the existing checks' business, and specs whose patches come
            # from a source archive (glibc, linux, grub2, shim) legitimately
            # have no such file next to the spec - flagging those would be
            # noise, not a finding.
            #
            # rpm resolves a local Source/Patch by basename against a flat
            # _sourcedir, and the package builder stages a package's sources
            # into a flat SOURCES dir, so "Source1: pam.d/chage.stig" is
            # satisfied by <specdir>/pam.d/chage.stig. Hence basename plus a
            # recursive lookup below the package directory.
            for fn in sorted(files - default_files):
                if not find_file_in_dir(fn, dirname):
                    err_dict.update_err_dict(
                        sec,
                        f"cell [{name}] ({macro_str}) references {fn}, which "
                        f"does not exist in {dirname}",
                    )
                    ret = True
    finally:
        for probe_fn, is_temp in probe_specs.values():
            if is_temp and os.path.exists(probe_fn):
                os.remove(probe_fn)

    return ret


def check_specs(files_list, subrelease, mainline):
    ret = False
    global specPaths

    setSpecPaths()

    specsForSubrelCheck = []

    for spec_fn in files_list:
        if not spec_fn.endswith(".spec"):
            continue

        tmp = "/".join(spec_fn.split("/")[-2:])
        if tmp not in specsForSubrelCheck:
            specsForSubrelCheck.append(tmp)

        print(f"Checking spec file: {spec_fn}")

        if not os.path.isfile(spec_fn):
            print(f"WARNING: {spec_fn} has been deleted in this changeset")
            continue

        specTopDir = spec_fn.split("SPECS/", 1)[0] + "SPECS"
        specTopDir = os.path.realpath(specTopDir)
        if specTopDir not in specPaths:
            specPaths.append(specTopDir)

        err_dict = ErrorDict(spec_fn)

        altered_spec = create_altered_spec(spec_fn)

        spec = getSpecObj(altered_spec)

        err, lines_dict = check_for_unallowed_usages(altered_spec, err_dict)

        currSpecDir = os.path.dirname(spec_fn)

        if any(
            [
                check_spec_header(spec, err_dict),
                check_for_version(spec, err_dict),
                check_for_dist_tag(spec, err_dict),
                check_changelog(spec, err_dict),
                check_sub_pkg(spec, err_dict),
                check_for_configure(lines_dict, err_dict),
                check_setup(lines_dict, err_dict),
                check_make_smp_flags(lines_dict, err_dict),
                check_for_unused_files(altered_spec, err_dict, currSpecDir, subrelease),
                check_proper_spdx_license(spec, err_dict),
                check_parse_matrix(
                    spec_fn, err_dict, currSpecDir, subrelease, mainline
                ),
            ]
        ):
            err = True

        if err:
            ret = True
            err_dict.print_err_dict()

        if os.path.exists(altered_spec):
            os.remove(altered_spec)

    global g_mainline
    g_mainline = mainline
    n = int(mainline)
    assert n >= 90, f"mainline should be  90 >= mainline <= {n}"
    assert int(subrelease) >= 90, f"subrelease should be 90 >= subrelease <= {n}"
    assert int(subrelease) <= n, f"subrelease should be 90 >= subrelease <= {n}"

    if check_subrelease_specs(specsForSubrelCheck, n):
        ret = True

    return ret


def main():
    import argparse

    mainline = "92"
    subrelease = "91"

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "paths",
        nargs="+",
        help="spec files or directories"
    )

    parser.add_argument(
        "--mainline",
        type=int,
        default=int(mainline),
        help=f"mainline version (default: {mainline})"
    )

    parser.add_argument(
        "--subrelease",
        type=int,
        default=int(subrelease),
        help=f"subrelease version (default: {subrelease})"
    )

    args = parser.parse_args()

    paths = args.paths
    mainline = args.mainline
    subrelease = args.subrelease

    #print(f"Paths={paths}")
    print(f"Subrelease={subrelease}")
    print(f"Mainline={mainline}")

    files = []

    def get_specs_in_dir(dirname):
        spec_files = []
        for r, _, fns in os.walk(dirname):
            for fn in fns:
                if fn.endswith((".spec", ".spec.in")):
                    spec_files.append(os.path.join(r, fn))
        return spec_files

    for path in paths:
        if path.endswith((".spec", ".spec.in")):
            files.append(path)
        elif os.path.isdir(path):
            files += get_specs_in_dir(path)

    if not files:
        pr_err("spec-checker: No spec files found in the specified directory/directories.")
        return 0

    if check_specs(files, subrelease, mainline):
        pr_err("ERROR: spec check failed")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
