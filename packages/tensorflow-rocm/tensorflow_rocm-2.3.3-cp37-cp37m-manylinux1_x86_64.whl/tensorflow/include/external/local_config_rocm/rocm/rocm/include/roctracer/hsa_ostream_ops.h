// automatically generated
/*
Copyright (c) 2018 Advanced Micro Devices, Inc. All rights reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
*/

#ifndef INC_HSA_OSTREAM_OPS_H_
#define INC_HSA_OSTREAM_OPS_H_
#ifdef __cplusplus
#include <iostream>

#include "roctracer.h"

namespace roctracer {
namespace hsa_support {
static int HSA_depth_max = 0;
// begin ostream ops for HSA 
// basic ostream ops
template <typename T>
  inline static std::ostream& operator<<(std::ostream& out, const T& v) {
     using std::operator<<;
     static bool recursion = false;
     if (recursion == false) { recursion = true; out << v; recursion = false; }
     return out; }
// End of basic ostream ops

inline static std::ostream& operator<<(std::ostream& out, const hsa_queue_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max++;
  if (HSA_depth_max <= 0) {
    roctracer::hsa_support::operator<<(out, "id = ");
    roctracer::hsa_support::operator<<(out, v.id);
    roctracer::hsa_support::operator<<(out, ", ");
    roctracer::hsa_support::operator<<(out, "reserved1 = ");
    roctracer::hsa_support::operator<<(out, v.reserved1);
    roctracer::hsa_support::operator<<(out, ", ");
    roctracer::hsa_support::operator<<(out, "size = ");
    roctracer::hsa_support::operator<<(out, v.size);
    roctracer::hsa_support::operator<<(out, ", ");
    roctracer::hsa_support::operator<<(out, "doorbell_signal = ");
    roctracer::hsa_support::operator<<(out, v.doorbell_signal);
    roctracer::hsa_support::operator<<(out, ", ");
    roctracer::hsa_support::operator<<(out, "features = ");
    roctracer::hsa_support::operator<<(out, v.features);
    roctracer::hsa_support::operator<<(out, ", ");
    roctracer::hsa_support::operator<<(out, "type = ");
    roctracer::hsa_support::operator<<(out, v.type);
  };
  HSA_depth_max--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_executable_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max++;
  if (HSA_depth_max <= 0) {
    roctracer::hsa_support::operator<<(out, "handle = ");
    roctracer::hsa_support::operator<<(out, v.handle);
  };
  HSA_depth_max--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_code_object_reader_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max++;
  if (HSA_depth_max <= 0) {
    roctracer::hsa_support::operator<<(out, "handle = ");
    roctracer::hsa_support::operator<<(out, v.handle);
  };
  HSA_depth_max--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_kernel_dispatch_packet_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max++;
  if (HSA_depth_max <= 0) {
    roctracer::hsa_support::operator<<(out, "completion_signal = ");
    roctracer::hsa_support::operator<<(out, v.completion_signal);
    roctracer::hsa_support::operator<<(out, ", ");
    roctracer::hsa_support::operator<<(out, "reserved2 = ");
    roctracer::hsa_support::operator<<(out, v.reserved2);
    roctracer::hsa_support::operator<<(out, ", ");
    roctracer::hsa_support::operator<<(out, "kernel_object = ");
    roctracer::hsa_support::operator<<(out, v.kernel_object);
    roctracer::hsa_support::operator<<(out, ", ");
    roctracer::hsa_support::operator<<(out, "group_segment_size = ");
    roctracer::hsa_support::operator<<(out, v.group_segment_size);
    roctracer::hsa_support::operator<<(out, ", ");
    roctracer::hsa_support::operator<<(out, "private_segment_size = ");
    roctracer::hsa_support::operator<<(out, v.private_segment_size);
    roctracer::hsa_support::operator<<(out, ", ");
    roctracer::hsa_support::operator<<(out, "grid_size_z = ");
    roctracer::hsa_support::operator<<(out, v.grid_size_z);
    roctracer::hsa_support::operator<<(out, ", ");
    roctracer::hsa_support::operator<<(out, "grid_size_y = ");
    roctracer::hsa_support::operator<<(out, v.grid_size_y);
    roctracer::hsa_support::operator<<(out, ", ");
    roctracer::hsa_support::operator<<(out, "grid_size_x = ");
    roctracer::hsa_support::operator<<(out, v.grid_size_x);
    roctracer::hsa_support::operator<<(out, ", ");
    roctracer::hsa_support::operator<<(out, "reserved0 = ");
    roctracer::hsa_support::operator<<(out, v.reserved0);
    roctracer::hsa_support::operator<<(out, ", ");
    roctracer::hsa_support::operator<<(out, "workgroup_size_z = ");
    roctracer::hsa_support::operator<<(out, v.workgroup_size_z);
    roctracer::hsa_support::operator<<(out, ", ");
    roctracer::hsa_support::operator<<(out, "workgroup_size_y = ");
    roctracer::hsa_support::operator<<(out, v.workgroup_size_y);
    roctracer::hsa_support::operator<<(out, ", ");
    roctracer::hsa_support::operator<<(out, "workgroup_size_x = ");
    roctracer::hsa_support::operator<<(out, v.workgroup_size_x);
    roctracer::hsa_support::operator<<(out, ", ");
    roctracer::hsa_support::operator<<(out, "setup = ");
    roctracer::hsa_support::operator<<(out, v.setup);
    roctracer::hsa_support::operator<<(out, ", ");
    roctracer::hsa_support::operator<<(out, "header = ");
    roctracer::hsa_support::operator<<(out, v.header);
  };
  HSA_depth_max--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_region_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max++;
  if (HSA_depth_max <= 0) {
    roctracer::hsa_support::operator<<(out, "handle = ");
    roctracer::hsa_support::operator<<(out, v.handle);
  };
  HSA_depth_max--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_executable_symbol_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max++;
  if (HSA_depth_max <= 0) {
    roctracer::hsa_support::operator<<(out, "handle = ");
    roctracer::hsa_support::operator<<(out, v.handle);
  };
  HSA_depth_max--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_loaded_code_object_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max++;
  if (HSA_depth_max <= 0) {
    roctracer::hsa_support::operator<<(out, "handle = ");
    roctracer::hsa_support::operator<<(out, v.handle);
  };
  HSA_depth_max--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_dim3_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max++;
  if (HSA_depth_max <= 0) {
    roctracer::hsa_support::operator<<(out, "z = ");
    roctracer::hsa_support::operator<<(out, v.z);
    roctracer::hsa_support::operator<<(out, ", ");
    roctracer::hsa_support::operator<<(out, "y = ");
    roctracer::hsa_support::operator<<(out, v.y);
    roctracer::hsa_support::operator<<(out, ", ");
    roctracer::hsa_support::operator<<(out, "x = ");
    roctracer::hsa_support::operator<<(out, v.x);
  };
  HSA_depth_max--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_isa_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max++;
  if (HSA_depth_max <= 0) {
    roctracer::hsa_support::operator<<(out, "handle = ");
    roctracer::hsa_support::operator<<(out, v.handle);
  };
  HSA_depth_max--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_signal_group_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max++;
  if (HSA_depth_max <= 0) {
    roctracer::hsa_support::operator<<(out, "handle = ");
    roctracer::hsa_support::operator<<(out, v.handle);
  };
  HSA_depth_max--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_code_symbol_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max++;
  if (HSA_depth_max <= 0) {
    roctracer::hsa_support::operator<<(out, "handle = ");
    roctracer::hsa_support::operator<<(out, v.handle);
  };
  HSA_depth_max--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_barrier_and_packet_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max++;
  if (HSA_depth_max <= 0) {
    roctracer::hsa_support::operator<<(out, "completion_signal = ");
    roctracer::hsa_support::operator<<(out, v.completion_signal);
    roctracer::hsa_support::operator<<(out, ", ");
    roctracer::hsa_support::operator<<(out, "reserved2 = ");
    roctracer::hsa_support::operator<<(out, v.reserved2);
    roctracer::hsa_support::operator<<(out, ", ");
    roctracer::hsa_support::operator<<(out, "dep_signal = ");
    roctracer::hsa_support::operator<<(out, v.dep_signal);
    roctracer::hsa_support::operator<<(out, ", ");
    roctracer::hsa_support::operator<<(out, "reserved1 = ");
    roctracer::hsa_support::operator<<(out, v.reserved1);
    roctracer::hsa_support::operator<<(out, ", ");
    roctracer::hsa_support::operator<<(out, "reserved0 = ");
    roctracer::hsa_support::operator<<(out, v.reserved0);
    roctracer::hsa_support::operator<<(out, ", ");
    roctracer::hsa_support::operator<<(out, "header = ");
    roctracer::hsa_support::operator<<(out, v.header);
  };
  HSA_depth_max--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_callback_data_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max++;
  if (HSA_depth_max <= 0) {
    roctracer::hsa_support::operator<<(out, "handle = ");
    roctracer::hsa_support::operator<<(out, v.handle);
  };
  HSA_depth_max--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_agent_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max++;
  if (HSA_depth_max <= 0) {
    roctracer::hsa_support::operator<<(out, "handle = ");
    roctracer::hsa_support::operator<<(out, v.handle);
  };
  HSA_depth_max--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_agent_dispatch_packet_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max++;
  if (HSA_depth_max <= 0) {
    roctracer::hsa_support::operator<<(out, "completion_signal = ");
    roctracer::hsa_support::operator<<(out, v.completion_signal);
    roctracer::hsa_support::operator<<(out, ", ");
    roctracer::hsa_support::operator<<(out, "reserved2 = ");
    roctracer::hsa_support::operator<<(out, v.reserved2);
    roctracer::hsa_support::operator<<(out, ", ");
    roctracer::hsa_support::operator<<(out, "arg = ");
    roctracer::hsa_support::operator<<(out, v.arg);
    roctracer::hsa_support::operator<<(out, ", ");
    roctracer::hsa_support::operator<<(out, "reserved0 = ");
    roctracer::hsa_support::operator<<(out, v.reserved0);
    roctracer::hsa_support::operator<<(out, ", ");
    roctracer::hsa_support::operator<<(out, "type = ");
    roctracer::hsa_support::operator<<(out, v.type);
    roctracer::hsa_support::operator<<(out, ", ");
    roctracer::hsa_support::operator<<(out, "header = ");
    roctracer::hsa_support::operator<<(out, v.header);
  };
  HSA_depth_max--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_code_object_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max++;
  if (HSA_depth_max <= 0) {
    roctracer::hsa_support::operator<<(out, "handle = ");
    roctracer::hsa_support::operator<<(out, v.handle);
  };
  HSA_depth_max--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_signal_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max++;
  if (HSA_depth_max <= 0) {
    roctracer::hsa_support::operator<<(out, "handle = ");
    roctracer::hsa_support::operator<<(out, v.handle);
  };
  HSA_depth_max--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_barrier_or_packet_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max++;
  if (HSA_depth_max <= 0) {
    roctracer::hsa_support::operator<<(out, "completion_signal = ");
    roctracer::hsa_support::operator<<(out, v.completion_signal);
    roctracer::hsa_support::operator<<(out, ", ");
    roctracer::hsa_support::operator<<(out, "reserved2 = ");
    roctracer::hsa_support::operator<<(out, v.reserved2);
    roctracer::hsa_support::operator<<(out, ", ");
    roctracer::hsa_support::operator<<(out, "dep_signal = ");
    roctracer::hsa_support::operator<<(out, v.dep_signal);
    roctracer::hsa_support::operator<<(out, ", ");
    roctracer::hsa_support::operator<<(out, "reserved1 = ");
    roctracer::hsa_support::operator<<(out, v.reserved1);
    roctracer::hsa_support::operator<<(out, ", ");
    roctracer::hsa_support::operator<<(out, "reserved0 = ");
    roctracer::hsa_support::operator<<(out, v.reserved0);
    roctracer::hsa_support::operator<<(out, ", ");
    roctracer::hsa_support::operator<<(out, "header = ");
    roctracer::hsa_support::operator<<(out, v.header);
  };
  HSA_depth_max--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_wavefront_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max++;
  if (HSA_depth_max <= 0) {
    roctracer::hsa_support::operator<<(out, "handle = ");
    roctracer::hsa_support::operator<<(out, v.handle);
  };
  HSA_depth_max--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_cache_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max++;
  if (HSA_depth_max <= 0) {
    roctracer::hsa_support::operator<<(out, "handle = ");
    roctracer::hsa_support::operator<<(out, v.handle);
  };
  HSA_depth_max--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
// end ostream ops for HSA 
};};

inline static std::ostream& operator<<(std::ostream& out, const hsa_queue_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_executable_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_code_object_reader_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_kernel_dispatch_packet_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_region_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_executable_symbol_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_loaded_code_object_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_dim3_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_isa_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_signal_group_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_code_symbol_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_barrier_and_packet_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_callback_data_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_agent_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_agent_dispatch_packet_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_code_object_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_signal_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_barrier_or_packet_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_wavefront_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_cache_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

#endif //__cplusplus
#endif // INC_HSA_OSTREAM_OPS_H_
 
