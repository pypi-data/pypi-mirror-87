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
#include "oneapi/ccl/config.h"

#ifdef CCL_ENABLE_SYCL
#ifdef MULTI_GPU_SUPPORT
#include "sycl_l0/export.hpp"
/*
        #include "oneapi/ccl/native_device_api/l0/base.hpp"
        #include "oneapi/ccl/native_device_api/l0/base_impl.hpp"

        #include "oneapi/ccl/native_device_api/l0/primitives.hpp"
        #include "oneapi/ccl/native_device_api/l0/primitives_impl.hpp"

        #include "oneapi/ccl/native_device_api/l0/context.hpp"
        #include "oneapi/ccl/native_device_api/l0/device.hpp"
        #include "oneapi/ccl/native_device_api/l0/subdevice.hpp"
        #include "oneapi/ccl/native_device_api/l0/driver.hpp"
        #include "oneapi/ccl/native_device_api/l0/platform.hpp"
        */
#else
#include "sycl/export.hpp"
#endif
#else
#ifdef MULTI_GPU_SUPPORT
#include "l0/export.hpp"
#else
#include "empty/export.hpp"
#endif
#endif

#ifndef CL_BACKEND_TYPE
#error "Unsupported CL_BACKEND_TYPE. Available backends are: dpcpp_sycl, l0 "
#endif
namespace ccl {
using backend_traits = backend_info<CL_BACKEND_TYPE>;
using unified_device_type = generic_device_type<CL_BACKEND_TYPE>;
using unified_context_type = generic_context_type<CL_BACKEND_TYPE>;
using unified_platform_type = generic_platform_type<CL_BACKEND_TYPE>;
using unified_stream_type = generic_stream_type<CL_BACKEND_TYPE>;
using unified_event_type = generic_event_type<CL_BACKEND_TYPE>;
} // namespace ccl

#include "interop_utils.hpp"
