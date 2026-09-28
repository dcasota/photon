/*
 * FIPS Integrity check for Crypto API
 *
 * Copyright (C) 2020 - 2022 VMware, Inc.
 * Copyright (c) 2025 Broadcom. All Rights Reserved. The term "Broadcom"
 * refers to Broadcom Inc. and/or its subsidiaries.
 *
 * Author: Alexey Makhalov <ailexey.makhalov@broadcom.com>
 *
 */

/*
 * Bits can be moved around to satisfy current core canister.
 * TYPE_BITS can easily be 2 and 1 released bit can be added
 * to one of the other twos.
 */
#include <linux/types.h>

/*
 * Relocation type & Addend combinations for SREL instruction
 *
 *			imm		type	addend
 */
#define SREL_INSN_TA_0	0	/*	0	0	*/
#define SREL_INSN_TA_1	1	/*	0	5	*/
#define SREL_INSN_TA_2	2	/*	1	-5	*/
#define SREL_INSN_TA_3	3	/*	1	-4	*/
#define SREL_INSN_TA_4	4	/*	1	0	*/
#define SREL_INSN_TA_5	5	/*	1	4	*/
#define SREL_INSN_TA_6	6	/*	2	0	*/
/*
 * 7.x canisters also contain RIP-relative accesses whose displacement is not
 * the last field of the instruction (addends -1..-3, -6..-8); the old table
 * could not express them and the encoder silently dropped them.
 */
#define SREL_INSN_TA_7	7	/*	1	-3	*/
#define SREL_INSN_TA_8	8	/*	1	-2	*/
#define SREL_INSN_TA_9	9	/*	1	-1	*/
#define SREL_INSN_TA_10	10	/*	1	-6	*/
#define SREL_INSN_TA_11	11	/*	1	-7	*/
#define SREL_INSN_TA_12	12	/*	1	-8	*/

/* SREL code -> { rel type, addend }, indexed by SREL_INSN_TA_n. */
#define SREL_INSN_TABLE_INIT {						\
	{ 0, 0 }, { 0, 5 }, { 1, -5 }, { 1, -4 }, { 1, 0 }, { 1, 4 },	\
	{ 2, 0 }, { 1, -3 }, { 1, -2 }, { 1, -1 }, { 1, -6 }, { 1, -7 }, \
	{ 1, -8 },							\
}
struct srel_insn_ta {
	unsigned char type;
	signed char addend;
};

struct __attribute__((packed)) relocation {
	unsigned char section;
	unsigned char type;
	unsigned short symbol;
	unsigned int offset;
	int addend;
	bool insn_read_complete;
};

/* Generated data. */
extern const char canister_sections[];
extern const int canister_sections_size;
extern const char canister_strtab[];
extern const int canister_strtab_size;
extern const unsigned char canister_relocations_bytecode[];
extern const unsigned int canister_relocations_bytecode_size;

