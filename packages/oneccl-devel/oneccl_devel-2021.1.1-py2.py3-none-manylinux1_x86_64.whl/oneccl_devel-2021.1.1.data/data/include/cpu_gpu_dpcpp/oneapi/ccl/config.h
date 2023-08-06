/*
    Copyright 2016-2020 Intel Corporation.
    
    This software and the related documents are Intel copyrighted materials, and
    your use of them is governed by the express license under which they were
    provided to you (License). Unless the License provides otherwise, you may
    not use, modify, copy, publish, distribute, disclose or transmit this
    software or the related documents without Intel's prior written permission.
    
    This software and the related documents are provided as is, with no express
    or implied warranties, other than those that are expressly stated in the
    License.
*/
#pragma once

/* All symbols shall be internal unless marked as CCL_API */
#ifdef __linux__
#   if __GNUC__ >= 4
#       define CCL_HELPER_DLL_EXPORT __attribute__ ((visibility ("default")))
#   else
#       define CCL_HELPER_DLL_EXPORT
#   endif
#else
#error "unexpected OS"
#endif

#define CCL_API CCL_HELPER_DLL_EXPORT

#define ONECCL_SPEC_VERSION "1.0"

#define CCL_MAJOR_VERSION                   2021
#define CCL_MINOR_VERSION                   1
#define CCL_UPDATE_VERSION                  0
#define CCL_PRODUCT_STATUS             "Gold"
#define CCL_PRODUCT_BUILD_DATE         "2020-11-05T 22:45:02Z"
#define CCL_PRODUCT_FULL               "Gold-2021.1.0 2020-11-05T 22:45:02Z (HEAD/a346a692)"

/* Auto-generated configuration settings for SYCL support */
#define CCL_ENABLE_SYCL

#ifdef CCL_ENABLE_SYCL
#if defined(__cplusplus)
#if !defined(__clang__) || __clang_major__ < 9 || !defined(SYCL_LANGUAGE_VERSION)
#error This version of CCL configured only for oneAPI DPC++ Compiler
#endif
#endif
#endif

/* Auto-generated configuration settings for multi GPU support*/
/* #undef MULTI_GPU_SUPPORT */
