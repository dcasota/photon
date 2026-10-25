/*
 * Kernel APIs wrapper for the canister.
 *
 * Copyright (C) 2020 - 2022 VMware, Inc.
 * Copyright (c) 2025 Broadcom. All Rights Reserved. The term "Broadcom"
 * refers to Broadcom Inc. and/or its subsidiaries.
 *
 * Author: Alexey Makhalov <alexey.makhalov@broadcom.com>
 *
 * Linux 7.x port: exactly the services the 7.x canister calls (nm -u of
 * canister.o), each a thin call into the kernel, so that no kernel structure
 * whose layout may change (locks, task_struct, struct page, struct module,
 * iov_iter, acomp requests) is part of the measured object. The 6.12 helpers
 * that 7.x no longer needs (copied testmgr sglist builders, cryptd/ghash,
 * old scatterwalk and CPU-match helpers, per-site BUG/WARN) are gone.
 */

#include <linux/kernel.h>
#include <linux/types.h>
#include <linux/gfp.h>
#include <linux/slab.h>
#include <linux/mutex.h>
#include <linux/printk.h>
#include <linux/sched.h>
#include <linux/sched/signal.h>
#include <linux/kthread.h>
#include <linux/memblock.h>
#include <linux/ratelimit.h>
#include <linux/notifier.h>
#include <linux/module.h>
#include <linux/fips.h>
#include <linux/uio.h>
#include <linux/scatterlist.h>
#include <linux/mm.h>
#include <linux/crypto.h>
#include <crypto/algapi.h>
#include <crypto/aead.h>
#include <crypto/hash.h>
#include <crypto/akcipher.h>
#include <crypto/skcipher.h>
#include <crypto/kpp.h>
#include <crypto/acompress.h>
#include <asm/fpu/api.h>
#include "internal.h"
#include "fips_canister_wrapper.h"

static __ro_after_init bool alg_request_report;

/* ---- memory ---------------------------------------------------------- */

void *fcw_kmalloc(size_t size, gfp_t flags)
{
	return kmalloc(size, flags);
}

void *fcw_kzalloc(size_t size, gfp_t flags)
{
	return kzalloc(size, flags);
}

/* Early (pre-slab) allocations of fips_integrity_init() come from memblock. */
void * __init fcw_mem_alloc(size_t size)
{
	if (!slab_is_available())
		return memblock_alloc(size, 8);

	return fcw_kmalloc(size, GFP_KERNEL);
}

void __init fcw_mem_free(void *p)
{
	if (p && slab_is_available() && PageSlab(virt_to_head_page(p)))
		kfree(p);
}

/* ---- scheduling, threads, modules ------------------------------------ */

int fcw_cond_resched(void)
{
	return cond_resched();
}

bool fcw_need_resched(void)
{
	return need_resched();
}

int fcw_signal_pending(void)
{
	return signal_pending(current);
}

void *fcw_kthread_run(int (*threadfn)(void *data), void *data, const char namefmt[])
{
	return kthread_run(threadfn, data, "%s", namefmt);
}

void __noreturn __fcw_module_put_and_kthread_exit(void *mod, long code)
{
	__module_put_and_kthread_exit(mod, code);
}

bool fcw_try_module_get(void *module)
{
	return try_module_get(module);
}

void fcw_module_put(void *module)
{
	module_put(module);
}

void *fcw_mutex_init(void)
{
	struct mutex *m = kzalloc(sizeof(*m), GFP_KERNEL);

	if (m)
		mutex_init(m);
	return m;
}

void fcw_mutex_lock(void *m)
{
	mutex_lock((struct mutex *)m);
}

void fcw_mutex_unlock(void *m)
{
	mutex_unlock((struct mutex *)m);
}

void fcw_kernel_fpu_begin(void)
{
	kernel_fpu_begin();
}

void fcw_kernel_fpu_end(void)
{
	kernel_fpu_end();
}

void fcw_bug(void)
{
	BUG();
}

/* ---- requests --------------------------------------------------------- */

struct aead_request *fcw_aead_request_alloc(struct crypto_aead *tfm, gfp_t gfp)
{
	return aead_request_alloc(tfm, gfp);
}

struct ahash_request *fcw_ahash_request_alloc(struct crypto_ahash *tfm, gfp_t gfp)
{
	return ahash_request_alloc(tfm, gfp);
}

struct akcipher_request *fcw_akcipher_request_alloc(struct crypto_akcipher *tfm,
						    gfp_t gfp)
{
	return akcipher_request_alloc(tfm, gfp);
}

struct skcipher_request *fcw_skcipher_request_alloc(struct crypto_skcipher *tfm,
						    gfp_t gfp)
{
	return skcipher_request_alloc(tfm, gfp);
}

struct kpp_request *fcw_kpp_request_alloc(struct crypto_kpp *tfm, gfp_t gfp)
{
	return kpp_request_alloc(tfm, gfp);
}

/* acomp tfm and request stay opaque inside the canister (testmgr only). */
void *fcw_crypto_alloc_acomp(const char *alg_name, u32 type, u32 mask)
{
	return crypto_alloc_acomp(alg_name, type, mask);
}

void fcw_crypto_free_acomp(void *tfm)
{
	crypto_free_acomp(tfm);
}

const char *fcw_crypto_acomp_driver_name(void *tfm)
{
	return crypto_tfm_alg_driver_name(crypto_acomp_tfm(tfm));
}

void *fcw_acomp_request_alloc(void *tfm, gfp_t gfp)
{
	return acomp_request_alloc((struct crypto_acomp *)tfm, gfp);
}

void fcw_acomp_request_free(void *req)
{
	acomp_request_free(req);
}

void fcw_acomp_request_set_params(void *req, struct scatterlist *src,
				  struct scatterlist *dst,
				  unsigned int slen, unsigned int dlen)
{
	acomp_request_set_params(req, src, dst, slen, dlen);
}

void fcw_acomp_request_set_callback(void *req, u32 flgs,
				    crypto_completion_t cmpl, void *data)
{
	acomp_request_set_callback(req, flgs, cmpl, data);
}

int fcw_crypto_acomp_compress(void *req)
{
	return crypto_acomp_compress(req);
}

int fcw_crypto_acomp_decompress(void *req)
{
	return crypto_acomp_decompress(req);
}

unsigned int fcw_acomp_req_dlen(void *req)
{
	return ((struct acomp_req *)req)->dlen;
}

/* ---- scatterlists and iterators --------------------------------------- */

void fcw_sg_set_buf(struct scatterlist *sg, const void *buf, unsigned int buflen)
{
	sg_set_buf(sg, buf, buflen);
}

void *fcw_sg_page_address(struct scatterlist *sg)
{
	return page_address(sg_page(sg));
}

/* A source iov_iter over @kvec for canister code, which may not hold one. */
void *fcw_iov_iter_kvec_new(const struct kvec *kvec, unsigned long nr_segs,
			    size_t count)
{
	struct iov_iter *i = kmalloc(sizeof(*i), GFP_KERNEL);

	if (i)
		iov_iter_kvec(i, ITER_SOURCE, kvec, nr_segs, count);
	return i;
}

void fcw_iov_iter_free(void *i)
{
	kfree(i);
}

size_t fcw_iov_iter_count(void *i)
{
	return iov_iter_count((struct iov_iter *)i);
}

size_t fcw_copy_from_iter(void *addr, size_t bytes, void *i)
{
	return copy_from_iter(addr, bytes, (struct iov_iter *)i);
}

/* ---- logging ---------------------------------------------------------- */

/*
 * Rate limiting for canister code (printk_ratelimited() inside FIPS_CANISTER
 * units): the struct ratelimit_state, which holds a raw spinlock, lives out
 * here. *rsp is the canister's per-call-site opaque slot, installed once.
 */
bool fcw_ratelimit(void **rsp, const char *name)
{
	struct ratelimit_state *rs = READ_ONCE(*rsp);

	if (!rs) {
		struct ratelimit_state *n = kzalloc(sizeof(*n), GFP_ATOMIC);

		if (!n)
			return true;	/* print rather than lose the message */
		ratelimit_state_init(n, DEFAULT_RATELIMIT_INTERVAL,
				     DEFAULT_RATELIMIT_BURST);
		if (cmpxchg(rsp, NULL, n) != NULL)
			kfree(n);
		rs = READ_ONCE(*rsp);
	}
	return ___ratelimit(rs, name);
}

/*
 * printk() is a macro that checks the log level at compile time, so canister
 * output is forwarded as a %pV argument.
 */
int fcw_printk(const char *format, ...)
{
	struct va_format vaf;
	va_list args;

	va_start(args, format);
	vaf.fmt = format;
	vaf.va = &args;
	_printk("%pV", &vaf);
	va_end(args);
	return 0;
}

/*
 * WARN*() inside the canister (see arch/x86/include/asm/bug.h): report the
 * canister's file and line through a regular WARN, which prints the
 * backtrace and taints like any other warning.
 */
void fcw_warn_slowpath_fmt(const char *file, const int line, unsigned int taint,
			   const char *fmt, ...)
{
	struct va_format vaf;
	va_list args;

	/* x86 WARN*() needs a constant taint; any other one is added here. */
	if (taint != TAINT_WARN)
		add_taint(taint, LOCKDEP_STILL_OK);
	if (!fmt) {
		WARN(1, "fips canister: WARNING at %s:%d\n", file, line);
		return;
	}
	va_start(args, fmt);
	vaf.fmt = fmt;
	vaf.va = &args;
	WARN(1, "fips canister: WARNING at %s:%d: %pV", file, line, &vaf);
	va_end(args);
}

/* ---- policy ----------------------------------------------------------- */

/* Outside FIPS mode the boot self-tests are skipped. */
int fcw_skip_tests(void)
{
	return !fips_enabled;
}

/*
 * Whether an algorithm belongs to the canister is derived, not listed: its
 * struct crypto_alg (or, for an instance, its template) lies in one of the
 * canister's data sections, whose bounds the canister marker linker script
 * defines. Weak so that a section the canister does not have compares empty.
 */
extern const char __canister_sdata[] __weak, __canister_edata[] __weak;
extern const char __canister_srodata[] __weak, __canister_erodata[] __weak;
extern const char __canister_sdataro_after_init[] __weak,
		  __canister_edataro_after_init[] __weak;

static bool fcw_in(const void *p, const char *s, const char *e)
{
	return s && e && (const char *)p >= s && (const char *)p < e;
}

static bool fcw_in_canister_data(const void *p)
{
	return fcw_in(p, __canister_sdata, __canister_edata) ||
	       fcw_in(p, __canister_srodata, __canister_erodata) ||
	       fcw_in(p, __canister_sdataro_after_init, __canister_edataro_after_init);
}

static bool fcw_alg_in_canister(struct crypto_alg *alg)
{
	if (alg->cra_flags & CRYPTO_ALG_INSTANCE) {
		struct crypto_instance *inst =
			container_of(alg, struct crypto_instance, alg);

		return inst->tmpl && fcw_in_canister_data(inst->tmpl);
	}
	return fcw_in_canister_data(alg);
}

bool alg_test_fips_allowed(const char *alg);

static int crypto_msg_notify(struct notifier_block *this, unsigned long msg,
			     void *data)
{
	struct crypto_alg *alg = data;

	/* A request carries a larval: it has a name but no driver name yet. */
	if (unlikely(!alg || !alg->cra_name[0] ||
		     (msg == CRYPTO_MSG_ALG_REGISTER && !alg->cra_driver_name[0]))) {
		pr_warn("%s: algorithm without a name (msg %lu)\n", __func__, msg);
		return NOTIFY_DONE;
	}
	if (msg == CRYPTO_MSG_ALG_REQUEST && alg_request_report)
		pr_notice("alg request: %s (%s) by %s(%d)\n",
			  alg->cra_driver_name, alg->cra_name,
			  current->comm, current->pid);
	/*
	 * In FIPS mode, an algorithm testmgr allows that is implemented outside
	 * the canister is usable but not part of the module boundary.
	 */
	if (msg == CRYPTO_MSG_ALG_REGISTER && fips_enabled &&
	    !fcw_alg_in_canister(alg) && alg_test_fips_allowed(alg->cra_name))
		pr_notice("alg: %s (%s) not certified\n",
			  alg->cra_driver_name, alg->cra_name);
	return NOTIFY_DONE;
}

static struct notifier_block crypto_msg_notifier = {
	.notifier_call = crypto_msg_notify,
};

static int __init wrapper_init(void)
{
	if (fcw_skip_tests())
		set_crypto_boot_test_finished();

	return crypto_register_notifier(&crypto_msg_notifier);
}
arch_initcall(wrapper_init);

static int __init alg_request_report_setup(char *__unused)
{
	alg_request_report = true;
	return 1;
}
__setup("alg_request_report", alg_request_report_setup);

/*
 * The canister is compiled once, by the flavour that builds it (linux, with
 * the function tracer: -pg -mfentry), and linked into every flavour. A
 * flavour without CONFIG_FUNCTION_TRACER (linux-esx) has no __fentry__, so
 * the canister's calls to it resolve to this no-op. Where the tracer is on,
 * the kernel's own __fentry__ is used and this is not built.
 */
#ifndef CONFIG_FUNCTION_TRACER
void __fentry__(void)
{
}
#endif
