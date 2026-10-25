/* SPDX-License-Identifier: GPL-2.0 */
/*
 * Kernel services the FIPS canister reaches through the wrapper.
 *
 * Copyright (C) 2020 - 2022 VMware, Inc.
 * Copyright (c) 2025 Broadcom. All Rights Reserved. The term "Broadcom"
 * refers to Broadcom Inc. and/or its subsidiaries.
 *
 * Linux 7.x port. Pointers to kernel structures that must stay out of the
 * canister's types (struct module, locks, task_struct, pages, iov_iter,
 * acomp) are passed as void *.
 */

#ifndef _FIPS_CANISTER_WRAPPER_H
#define _FIPS_CANISTER_WRAPPER_H

#include <linux/types.h>
#include <linux/gfp_types.h>
#include <linux/compiler.h>
#include <linux/crypto.h>

struct aead_request;
struct crypto_aead;
struct ahash_request;
struct crypto_ahash;
struct akcipher_request;
struct crypto_akcipher;
struct skcipher_request;
struct crypto_skcipher;
struct kpp_request;
struct crypto_kpp;
struct scatterlist;
struct kvec;

/* memory */
extern void *fcw_kmalloc(size_t size, gfp_t flags);
extern void *fcw_kzalloc(size_t size, gfp_t flags);
extern void *fcw_mem_alloc(size_t size);
extern void fcw_mem_free(void *p);

/* scheduling, threads, modules, locks */
extern int fcw_cond_resched(void);
extern bool fcw_need_resched(void);
extern int fcw_signal_pending(void);
extern void *fcw_kthread_run(int (*threadfn)(void *data), void *data, const char namefmt[]);
extern void __noreturn __fcw_module_put_and_kthread_exit(void *mod, long code);
extern bool fcw_try_module_get(void *module);
extern void fcw_module_put(void *module);
extern void *fcw_mutex_init(void);
extern void fcw_mutex_lock(void *m);
extern void fcw_mutex_unlock(void *m);
extern void fcw_kernel_fpu_begin(void);
extern void fcw_kernel_fpu_end(void);
extern void fcw_bug(void);

/* requests */
extern struct aead_request *fcw_aead_request_alloc(struct crypto_aead *tfm, gfp_t gfp);
extern struct ahash_request *fcw_ahash_request_alloc(struct crypto_ahash *tfm, gfp_t gfp);
extern struct akcipher_request *fcw_akcipher_request_alloc(struct crypto_akcipher *tfm,
							   gfp_t gfp);
extern struct skcipher_request *fcw_skcipher_request_alloc(struct crypto_skcipher *tfm,
							   gfp_t gfp);
extern struct kpp_request *fcw_kpp_request_alloc(struct crypto_kpp *tfm, gfp_t gfp);
extern void *fcw_crypto_alloc_acomp(const char *alg_name, u32 type, u32 mask);
extern void fcw_crypto_free_acomp(void *tfm);
extern const char *fcw_crypto_acomp_driver_name(void *tfm);
extern void *fcw_acomp_request_alloc(void *tfm, gfp_t gfp);
extern void fcw_acomp_request_free(void *req);
extern void fcw_acomp_request_set_params(void *req, struct scatterlist *src,
					 struct scatterlist *dst,
					 unsigned int slen, unsigned int dlen);
extern void fcw_acomp_request_set_callback(void *req, u32 flgs,
					   crypto_completion_t cmpl, void *data);
extern int fcw_crypto_acomp_compress(void *req);
extern int fcw_crypto_acomp_decompress(void *req);
extern unsigned int fcw_acomp_req_dlen(void *req);

/* scatterlists and iterators */
extern void fcw_sg_set_buf(struct scatterlist *sg, const void *buf, unsigned int buflen);
extern void *fcw_sg_page_address(struct scatterlist *sg);
extern void *fcw_iov_iter_kvec_new(const struct kvec *kvec, unsigned long nr_segs,
				   size_t count);
extern void fcw_iov_iter_free(void *i);
extern size_t fcw_iov_iter_count(void *i);
extern size_t fcw_copy_from_iter(void *addr, size_t bytes, void *i);

/* logging and policy */
extern __printf(1, 2) int fcw_printk(const char *format, ...);
extern bool fcw_ratelimit(void **rsp, const char *name);
extern int fcw_skip_tests(void);
extern __printf(4, 5) void fcw_warn_slowpath_fmt(const char *file, const int line,
						   unsigned int taint, const char *fmt, ...);
#ifndef CONFIG_FUNCTION_TRACER
void __fentry__(void);	/* no-op for flavours without the function tracer */
#endif

/*
 * Canister entry points the wrapper calls. The algorithms' own init functions
 * are called through generated trampolines (fips_canister_initcalls.c).
 */
int __init crypto_self_test_init(void);
int __init fips_integrity_init(void);
int __init fips_integrity_check(void);

#endif /* _FIPS_CANISTER_WRAPPER_H */
