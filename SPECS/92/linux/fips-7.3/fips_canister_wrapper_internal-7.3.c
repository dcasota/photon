/*
 * canister functions invoked from wrapper layer.
 *
 * Copyright (C) 2023 VMware, Inc.
 * Copyright (c) 2025 Broadcom. All Rights Reserved. The term "Broadcom"
 * refers to Broadcom Inc. and/or its subsidiaries.
 *
 * Author: Keerthana K <keerthana.kalyanasundaram@broadcom.com>
 *
 * 7.x: the algorithms' init functions run from generated initcalls at their
 * upstream levels (fips_canister_initcalls.c). What is left here is the
 * module-level check: once every algorithm is registered, verify the
 * integrity result and run the known-answer self-tests.
 */

#include <linux/init.h>
#include <linux/fips.h>
#include <linux/printk.h>
#include "fips_canister_wrapper_internal.h"

static int __init fcw_module_init(void)
{
	int err;

	err = fips_integrity_check();
	if (err)
		pr_err("fips canister: integrity check returned %d\n", err);
	err = crypto_self_test_init();
	if (err && fips_enabled)
		pr_err("fips canister: self-tests returned %d\n", err);
	return 0;
}
late_initcall_sync(fcw_module_init);
