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
#include "oneapi/ccl/types.hpp"
#include "oneapi/ccl/type_traits.hpp"
#ifdef CCL_ENABLE_SYCL
#include <CL/sycl.hpp>
#endif

namespace native {
namespace detail {

#ifdef CCL_ENABLE_SYCL
size_t get_sycl_device_id(const cl::sycl::device& dev);
std::string usm_to_string(cl::sycl::usm::alloc val);
#endif

enum usm_support_mode { prohibited = 0, direct, shared, need_conversion, last_value };
std::string to_string(usm_support_mode val);

using assoc_result = std::tuple<usm_support_mode, const void*, std::string>;
enum assoc_result_index { SUPPORT_MODE = 0, POINTER_VALUE, ERROR_CAUSE };

#if defined(MULTI_GPU_SUPPORT) || defined(CCL_ENABLE_SYCL)
assoc_result check_assoc_device_memory(const void* mem,
                                       const ccl::unified_device_type::ccl_native_t& device,
                                       const ccl::unified_context_type::ccl_native_t& ctx);

usm_support_mode check_assoc_device_memory(const std::vector<void*>& mems,
                                           const ccl::unified_device_type::ccl_native_t& device,
                                           const ccl::unified_context_type::ccl_native_t& ctx);

#endif //defined(MULTI_GPU_SUPPORT) || defined(CCL_ENABLE_SYCL)
std::string to_string(const assoc_result& res);

#if defined(MULTI_GPU_SUPPORT) || defined(CCL_ENABLE_SYCL)
template <size_t N>
using multiple_assoc_result = std::array<assoc_result, N>;

template <class... mem_type>
auto check_multiple_assoc_device_memory(const ccl::unified_device_type::ccl_native_t& device,
                                        const ccl::unified_context_type::ccl_native_t& ctx,
                                        const mem_type*... mem)
    -> multiple_assoc_result<sizeof...(mem)> {
    multiple_assoc_result<sizeof...(mem)> ret{ check_assoc_device_memory(mem, device, ctx)... };
    return ret;
}

template <size_t N>
std::string to_string(const multiple_assoc_result<N>& res) {
    std::stringstream ss;
    for (size_t i = 0; i < N; i++) {
        ss << "Arg: " << std::to_string(i) << to_string(res[i]) << std::endl;
    }
    return ss.str();
}
#endif //defined(MULTI_GPU_SUPPORT) || defined(CCL_ENABLE_SYCL)
} // namespace detail
} // namespace native
