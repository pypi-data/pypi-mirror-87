/*===---- clflushoptintrin.h - CLFLUSHOPT intrinsic ------------------------===
 *
 * Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
 * See https://llvm.org/LICENSE.txt for license information.
 * SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
 *
 *===-----------------------------------------------------------------------===
 */

#ifndef __IMMINTRIN_H
#error "Never use <clflushoptintrin.h> directly; include <immintrin.h> instead."
#endif

#ifndef __CLFLUSHOPTINTRIN_H
#define __CLFLUSHOPTINTRIN_H

/* Define the default attributes for the functions in this file. */
#define __DEFAULT_FN_ATTRS __attribute__((__always_inline__, __nodebug__,  __target__("clflushopt")))

static __inline__ void __DEFAULT_FN_ATTRS
_mm_clflushopt(void const * __m) {
  __builtin_ia32_clflushopt(__m);
}

#undef __DEFAULT_FN_ATTRS

#endif
