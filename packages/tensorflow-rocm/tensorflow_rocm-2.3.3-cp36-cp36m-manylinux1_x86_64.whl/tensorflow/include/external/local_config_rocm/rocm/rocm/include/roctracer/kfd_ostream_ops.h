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

#ifndef INC_KFD_OSTREAM_OPS_H_
#define INC_KFD_OSTREAM_OPS_H_
#ifdef __cplusplus
#include <iostream>

#include "roctracer.h"

namespace roctracer {
namespace kfd_support {
static int KFD_depth_max = 0;
// begin ostream ops for KFD 
template <typename T>
struct output_streamer {
  inline static std::ostream& put(std::ostream& out, const T& v) { return out; }
};


template<>
struct output_streamer<HsaCounterBlockProperties&> {
  inline static std::ostream& put(std::ostream& out, HsaCounterBlockProperties& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "Counters = ");
    roctracer::kfd_support::output_streamer<HsaCounter[1]>::put(out, v.Counters);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "NumConcurrent = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.NumConcurrent);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "NumCounters = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.NumCounters);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "BlockId = ");
    roctracer::kfd_support::output_streamer<HSA_UUID>::put(out, v.BlockId);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HsaQueueReport&> {
  inline static std::ostream& put(std::ostream& out, HsaQueueReport& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "QueueSize = ");
    roctracer::kfd_support::output_streamer<HSAuint64>::put(out, v.QueueSize);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "VMID = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.VMID);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HSA_DEBUG_PROPERTIES&> {
  inline static std::ostream& put(std::ostream& out, HSA_DEBUG_PROPERTIES& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "Value = ");
    roctracer::kfd_support::output_streamer<HSAuint64>::put(out, v.Value);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HsaNodeChange&> {
  inline static std::ostream& put(std::ostream& out, HsaNodeChange& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "Flags = ");
    roctracer::kfd_support::output_streamer<HSA_EVENTTYPE_NODECHANGE_FLAGS>::put(out, v.Flags);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HsaDeviceStateChange&> {
  inline static std::ostream& put(std::ostream& out, HsaDeviceStateChange& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "Flags = ");
    roctracer::kfd_support::output_streamer<HSA_EVENTTYPE_DEVICESTATECHANGE_FLAGS>::put(out, v.Flags);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "Device = ");
    roctracer::kfd_support::output_streamer<HSA_DEVICE>::put(out, v.Device);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "NodeId = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.NodeId);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HSA_LINKPROPERTY&> {
  inline static std::ostream& put(std::ostream& out, HSA_LINKPROPERTY& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "LinkProperty = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.LinkProperty);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<__fsid_t&> {
  inline static std::ostream& put(std::ostream& out, __fsid_t& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "__val = ");
    roctracer::kfd_support::output_streamer<int[2]>::put(out, v.__val);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HsaMemoryRange&> {
  inline static std::ostream& put(std::ostream& out, HsaMemoryRange& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "SizeInBytes = ");
    roctracer::kfd_support::output_streamer<HSAuint64>::put(out, v.SizeInBytes);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HsaCounterProperties&> {
  inline static std::ostream& put(std::ostream& out, HsaCounterProperties& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "Blocks = ");
    roctracer::kfd_support::output_streamer<HsaCounterBlockProperties[1]>::put(out, v.Blocks);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "NumConcurrent = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.NumConcurrent);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "NumBlocks = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.NumBlocks);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HSA_ENGINE_VERSION&> {
  inline static std::ostream& put(std::ostream& out, HSA_ENGINE_VERSION& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "Value = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.Value);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HsaCComputeProperties&> {
  inline static std::ostream& put(std::ostream& out, HsaCComputeProperties& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "SiblingMap = ");
    roctracer::kfd_support::output_streamer<HSAuint32[256]>::put(out, v.SiblingMap);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HsaVersionInfo&> {
  inline static std::ostream& put(std::ostream& out, HsaVersionInfo& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "KernelInterfaceMinorVersion = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.KernelInterfaceMinorVersion);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "KernelInterfaceMajorVersion = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.KernelInterfaceMajorVersion);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HsaCacheType&> {
  inline static std::ostream& put(std::ostream& out, HsaCacheType& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "Value = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.Value);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HSA_MEMORYPROPERTY&> {
  inline static std::ostream& put(std::ostream& out, HSA_MEMORYPROPERTY& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "MemoryProperty = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.MemoryProperty);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HsaCounter&> {
  inline static std::ostream& put(std::ostream& out, HsaCounter& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "BlockIndex = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.BlockIndex);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "Flags = ");
    roctracer::kfd_support::output_streamer<HsaCounterFlags>::put(out, v.Flags);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "CounterMask = ");
    roctracer::kfd_support::output_streamer<HSAuint64>::put(out, v.CounterMask);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "CounterSizeInBits = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.CounterSizeInBits);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "CounterId = ");
    roctracer::kfd_support::output_streamer<HSAuint64>::put(out, v.CounterId);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "Type = ");
    roctracer::kfd_support::output_streamer<HSA_PROFILE_TYPE>::put(out, v.Type);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HsaNodeProperties&> {
  inline static std::ostream& put(std::ostream& out, HsaNodeProperties& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "Reserved = ");
    roctracer::kfd_support::output_streamer<HSAuint8[20]>::put(out, v.Reserved);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "UniqueID = ");
    roctracer::kfd_support::output_streamer<HSAuint64>::put(out, v.UniqueID);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "Domain = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.Domain);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "Reserved2 = ");
    roctracer::kfd_support::output_streamer<HSAuint8>::put(out, v.Reserved2);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "NumGws = ");
    roctracer::kfd_support::output_streamer<HSAuint8>::put(out, v.NumGws);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "NumCpQueues = ");
    roctracer::kfd_support::output_streamer<HSAuint8>::put(out, v.NumCpQueues);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "NumSdmaQueuesPerEngine = ");
    roctracer::kfd_support::output_streamer<HSAuint8>::put(out, v.NumSdmaQueuesPerEngine);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "NumSdmaXgmiEngines = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.NumSdmaXgmiEngines);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "NumSdmaEngines = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.NumSdmaEngines);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "HiveID = ");
    roctracer::kfd_support::output_streamer<HSAuint64>::put(out, v.HiveID);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "DebugProperties = ");
    roctracer::kfd_support::output_streamer<HSA_DEBUG_PROPERTIES>::put(out, v.DebugProperties);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "uCodeEngineVersions = ");
    roctracer::kfd_support::output_streamer<HSA_ENGINE_VERSION>::put(out, v.uCodeEngineVersions);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "AMDName = ");
    roctracer::kfd_support::output_streamer<HSAuint8[64]>::put(out, v.AMDName);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "MarketingName = ");
    roctracer::kfd_support::output_streamer<HSAuint16[64]>::put(out, v.MarketingName);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "DrmRenderMinor = ");
    roctracer::kfd_support::output_streamer<HSAint32>::put(out, v.DrmRenderMinor);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "MaxEngineClockMhzCCompute = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.MaxEngineClockMhzCCompute);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "MaxEngineClockMhzFCompute = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.MaxEngineClockMhzFCompute);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "LocalMemSize = ");
    roctracer::kfd_support::output_streamer<HSAuint64>::put(out, v.LocalMemSize);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "LocationId = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.LocationId);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "DeviceId = ");
    roctracer::kfd_support::output_streamer<HSAuint16>::put(out, v.DeviceId);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "VendorId = ");
    roctracer::kfd_support::output_streamer<HSAuint16>::put(out, v.VendorId);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "EngineId = ");
    roctracer::kfd_support::output_streamer<HSA_ENGINE_ID>::put(out, v.EngineId);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "MaxSlotsScratchCU = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.MaxSlotsScratchCU);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "NumSIMDPerCU = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.NumSIMDPerCU);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "NumCUPerArray = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.NumCUPerArray);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "NumArrays = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.NumArrays);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "NumShaderBanks = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.NumShaderBanks);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "WaveFrontSize = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.WaveFrontSize);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "GDSSizeInKB = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.GDSSizeInKB);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "LDSSizeInKB = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.LDSSizeInKB);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "MaxWavesPerSIMD = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.MaxWavesPerSIMD);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "Capability = ");
    roctracer::kfd_support::output_streamer<HSA_CAPABILITY>::put(out, v.Capability);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "FComputeIdLo = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.FComputeIdLo);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "CComputeIdLo = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.CComputeIdLo);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "NumIOLinks = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.NumIOLinks);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "NumCaches = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.NumCaches);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "NumMemoryBanks = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.NumMemoryBanks);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "NumFComputeCores = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.NumFComputeCores);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "NumCPUCores = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.NumCPUCores);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HsaSystemProperties&> {
  inline static std::ostream& put(std::ostream& out, HsaSystemProperties& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "PlatformRev = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.PlatformRev);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "PlatformId = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.PlatformId);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "PlatformOem = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.PlatformOem);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "NumNodes = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.NumNodes);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HsaMemoryProperties&> {
  inline static std::ostream& put(std::ostream& out, HsaMemoryProperties& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "VirtualBaseAddress = ");
    roctracer::kfd_support::output_streamer<HSAuint64>::put(out, v.VirtualBaseAddress);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "MemoryClockMax = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.MemoryClockMax);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "Width = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.Width);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "Flags = ");
    roctracer::kfd_support::output_streamer<HSA_MEMORYPROPERTY>::put(out, v.Flags);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "HeapType = ");
    roctracer::kfd_support::output_streamer<HSA_HEAPTYPE>::put(out, v.HeapType);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HSA_ENGINE_ID&> {
  inline static std::ostream& put(std::ostream& out, HSA_ENGINE_ID& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "Value = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.Value);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HSA_CAPABILITY&> {
  inline static std::ostream& put(std::ostream& out, HSA_CAPABILITY& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "Value = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.Value);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HsaQueueInfo&> {
  inline static std::ostream& put(std::ostream& out, HsaQueueInfo& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "Reserved2 = ");
    roctracer::kfd_support::output_streamer<HSAuint64>::put(out, v.Reserved2);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "SaveAreaHeader = ");
    roctracer::kfd_support::output_streamer<HsaUserContextSaveAreaHeader *>::put(out, v.SaveAreaHeader);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "ControlStackUsedInBytes = ");
    roctracer::kfd_support::output_streamer<HSAuint64>::put(out, v.ControlStackUsedInBytes);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "ControlStackTop = ");
    roctracer::kfd_support::output_streamer<HSAuint32 *>::put(out, v.ControlStackTop);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "SaveAreaSizeInBytes = ");
    roctracer::kfd_support::output_streamer<HSAuint64>::put(out, v.SaveAreaSizeInBytes);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "UserContextSaveArea = ");
    roctracer::kfd_support::output_streamer<HSAuint32 *>::put(out, v.UserContextSaveArea);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "CUMaskInfo = ");
    roctracer::kfd_support::output_streamer<HSAuint32 *>::put(out, v.CUMaskInfo);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "NumCUAssigned = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.NumCUAssigned);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "QueueTypeExtended = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.QueueTypeExtended);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "QueueDetailError = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.QueueDetailError);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HsaIoLinkProperties&> {
  inline static std::ostream& put(std::ostream& out, HsaIoLinkProperties& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "Flags = ");
    roctracer::kfd_support::output_streamer<HSA_LINKPROPERTY>::put(out, v.Flags);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "RecTransferSize = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.RecTransferSize);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "MaximumBandwidth = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.MaximumBandwidth);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "MinimumBandwidth = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.MinimumBandwidth);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "MaximumLatency = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.MaximumLatency);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "MinimumLatency = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.MinimumLatency);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "Weight = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.Weight);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "NodeTo = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.NodeTo);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "NodeFrom = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.NodeFrom);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "VersionMinor = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.VersionMinor);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "VersionMajor = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.VersionMajor);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "IoLinkType = ");
    roctracer::kfd_support::output_streamer<HSA_IOLINKTYPE>::put(out, v.IoLinkType);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HsaMemoryAccessFault&> {
  inline static std::ostream& put(std::ostream& out, HsaMemoryAccessFault& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "Flags = ");
    roctracer::kfd_support::output_streamer<HSA_EVENTID_MEMORYFLAGS>::put(out, v.Flags);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "Failure = ");
    roctracer::kfd_support::output_streamer<HsaAccessAttributeFailure>::put(out, v.Failure);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "VirtualAddress = ");
    roctracer::kfd_support::output_streamer<HSAuint64>::put(out, v.VirtualAddress);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "NodeId = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.NodeId);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HsaEvent&> {
  inline static std::ostream& put(std::ostream& out, HsaEvent& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "EventData = ");
    roctracer::kfd_support::output_streamer<HsaEventData>::put(out, v.EventData);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "EventId = ");
    roctracer::kfd_support::output_streamer<HSA_EVENTID>::put(out, v.EventId);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HsaMemMapFlags&> {
  inline static std::ostream& put(std::ostream& out, HsaMemMapFlags& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HsaDbgWaveMessage&> {
  inline static std::ostream& put(std::ostream& out, HsaDbgWaveMessage& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "DbgWaveMsg = ");
    roctracer::kfd_support::output_streamer<HsaDbgWaveMessageAMD>::put(out, v.DbgWaveMsg);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HsaGraphicsResourceInfo&> {
  inline static std::ostream& put(std::ostream& out, HsaGraphicsResourceInfo& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "Reserved = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.Reserved);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "MetadataSizeInBytes = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.MetadataSizeInBytes);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "SizeInBytes = ");
    roctracer::kfd_support::output_streamer<HSAuint64>::put(out, v.SizeInBytes);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HsaEventData&> {
  inline static std::ostream& put(std::ostream& out, HsaEventData& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "HWData3 = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.HWData3);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "HWData2 = ");
    roctracer::kfd_support::output_streamer<HSAuint64>::put(out, v.HWData2);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "HWData1 = ");
    roctracer::kfd_support::output_streamer<HSAuint64>::put(out, v.HWData1);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "EventData.MemoryAccessFault = ");
    roctracer::kfd_support::output_streamer<HsaMemoryAccessFault>::put(out, v.EventData.MemoryAccessFault);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "EventData.DeviceState = ");
    roctracer::kfd_support::output_streamer<HsaDeviceStateChange>::put(out, v.EventData.DeviceState);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "EventData.NodeChangeState = ");
    roctracer::kfd_support::output_streamer<HsaNodeChange>::put(out, v.EventData.NodeChangeState);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "EventData.SyncVar = ");
    roctracer::kfd_support::output_streamer<HsaSyncVar>::put(out, v.EventData.SyncVar);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "EventType = ");
    roctracer::kfd_support::output_streamer<HSA_EVENTTYPE>::put(out, v.EventType);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HsaDbgWaveMessageAMD&> {
  inline static std::ostream& put(std::ostream& out, HsaDbgWaveMessageAMD& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "WaveMsgInfoGen2 = ");
    roctracer::kfd_support::output_streamer<HsaDbgWaveMsgAMDGen2>::put(out, v.WaveMsgInfoGen2);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HsaPointerInfo&> {
  inline static std::ostream& put(std::ostream& out, HsaPointerInfo& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "MappedNodes = ");
    roctracer::kfd_support::output_streamer<const HSAuint32 *>::put(out, v.MappedNodes);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "RegisteredNodes = ");
    roctracer::kfd_support::output_streamer<const HSAuint32 *>::put(out, v.RegisteredNodes);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "NMappedNodes = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.NMappedNodes);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "NRegisteredNodes = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.NRegisteredNodes);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "SizeInBytes = ");
    roctracer::kfd_support::output_streamer<HSAuint64>::put(out, v.SizeInBytes);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "GPUAddress = ");
    roctracer::kfd_support::output_streamer<HSAuint64>::put(out, v.GPUAddress);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "MemFlags = ");
    roctracer::kfd_support::output_streamer<HsaMemFlags>::put(out, v.MemFlags);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "Node = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.Node);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "Type = ");
    roctracer::kfd_support::output_streamer<HSA_POINTER_TYPE>::put(out, v.Type);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HsaClockCounters&> {
  inline static std::ostream& put(std::ostream& out, HsaClockCounters& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "SystemClockFrequencyHz = ");
    roctracer::kfd_support::output_streamer<HSAuint64>::put(out, v.SystemClockFrequencyHz);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "SystemClockCounter = ");
    roctracer::kfd_support::output_streamer<HSAuint64>::put(out, v.SystemClockCounter);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "CPUClockCounter = ");
    roctracer::kfd_support::output_streamer<HSAuint64>::put(out, v.CPUClockCounter);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "GPUClockCounter = ");
    roctracer::kfd_support::output_streamer<HSAuint64>::put(out, v.GPUClockCounter);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HsaEventDescriptor&> {
  inline static std::ostream& put(std::ostream& out, HsaEventDescriptor& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "SyncVar = ");
    roctracer::kfd_support::output_streamer<HsaSyncVar>::put(out, v.SyncVar);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "NodeId = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.NodeId);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "EventType = ");
    roctracer::kfd_support::output_streamer<HSA_EVENTTYPE>::put(out, v.EventType);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HsaAccessAttributeFailure&> {
  inline static std::ostream& put(std::ostream& out, HsaAccessAttributeFailure& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "Reserved = ");
    roctracer::kfd_support::output_streamer<unsigned int>::put(out, v.Reserved);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "ErrorType = ");
    roctracer::kfd_support::output_streamer<unsigned int>::put(out, v.ErrorType);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "Imprecise = ");
    roctracer::kfd_support::output_streamer<unsigned int>::put(out, v.Imprecise);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "ECC = ");
    roctracer::kfd_support::output_streamer<unsigned int>::put(out, v.ECC);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "GpuAccess = ");
    roctracer::kfd_support::output_streamer<unsigned int>::put(out, v.GpuAccess);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "NoExecute = ");
    roctracer::kfd_support::output_streamer<unsigned int>::put(out, v.NoExecute);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "ReadOnly = ");
    roctracer::kfd_support::output_streamer<unsigned int>::put(out, v.ReadOnly);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "NotPresent = ");
    roctracer::kfd_support::output_streamer<unsigned int>::put(out, v.NotPresent);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HSA_UUID&> {
  inline static std::ostream& put(std::ostream& out, HSA_UUID& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "Data4 = ");
    roctracer::kfd_support::output_streamer<HSAuint8[8]>::put(out, v.Data4);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "Data3 = ");
    roctracer::kfd_support::output_streamer<HSAuint16>::put(out, v.Data3);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "Data2 = ");
    roctracer::kfd_support::output_streamer<HSAuint16>::put(out, v.Data2);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "Data1 = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.Data1);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HsaQueueResource&> {
  inline static std::ostream& put(std::ostream& out, HsaQueueResource& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "QueueId = ");
    roctracer::kfd_support::output_streamer<HSA_QUEUEID>::put(out, v.QueueId);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HsaCounterFlags&> {
  inline static std::ostream& put(std::ostream& out, HsaCounterFlags& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HsaUserContextSaveAreaHeader&> {
  inline static std::ostream& put(std::ostream& out, HsaUserContextSaveAreaHeader& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "DebugSize = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.DebugSize);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "DebugOffset = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.DebugOffset);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "WaveStateSize = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.WaveStateSize);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "WaveStateOffset = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.WaveStateOffset);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "ControlStackSize = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.ControlStackSize);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "ControlStackOffset = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.ControlStackOffset);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HsaCacheProperties&> {
  inline static std::ostream& put(std::ostream& out, HsaCacheProperties& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "SiblingMap = ");
    roctracer::kfd_support::output_streamer<HSAuint32[256]>::put(out, v.SiblingMap);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "CacheType = ");
    roctracer::kfd_support::output_streamer<HsaCacheType>::put(out, v.CacheType);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "CacheLatency = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.CacheLatency);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "CacheAssociativity = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.CacheAssociativity);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "CacheLinesPerTag = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.CacheLinesPerTag);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "CacheLineSize = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.CacheLineSize);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "CacheSize = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.CacheSize);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "CacheLevel = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.CacheLevel);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "ProcessorIdLow = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.ProcessorIdLow);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HsaMemFlags&> {
  inline static std::ostream& put(std::ostream& out, HsaMemFlags& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HsaPmcTraceRoot&> {
  inline static std::ostream& put(std::ostream& out, HsaPmcTraceRoot& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "TraceId = ");
    roctracer::kfd_support::output_streamer<HSATraceId>::put(out, v.TraceId);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "NumberOfPasses = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.NumberOfPasses);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "TraceBufferMinSizeBytes = ");
    roctracer::kfd_support::output_streamer<HSAuint64>::put(out, v.TraceBufferMinSizeBytes);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HsaGpuTileConfig&> {
  inline static std::ostream& put(std::ostream& out, HsaGpuTileConfig& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "Reserved = ");
    roctracer::kfd_support::output_streamer<HSAuint32[7]>::put(out, v.Reserved);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "NumRanks = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.NumRanks);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "NumBanks = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.NumBanks);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "GbAddrConfig = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.GbAddrConfig);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "NumMacroTileConfigs = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.NumMacroTileConfigs);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "NumTileConfigs = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.NumTileConfigs);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "MacroTileConfig = ");
    roctracer::kfd_support::output_streamer<HSAuint32 *>::put(out, v.MacroTileConfig);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "TileConfig = ");
    roctracer::kfd_support::output_streamer<HSAuint32 *>::put(out, v.TileConfig);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HsaSyncVar&> {
  inline static std::ostream& put(std::ostream& out, HsaSyncVar& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "SyncVarSize = ");
    roctracer::kfd_support::output_streamer<HSAuint64>::put(out, v.SyncVarSize);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "SyncVar.UserDataPtrValue = ");
    roctracer::kfd_support::output_streamer<HSAuint64>::put(out, v.SyncVar.UserDataPtrValue);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};

template<>
struct output_streamer<HsaDbgWaveMsgAMDGen2&> {
  inline static std::ostream& put(std::ostream& out, HsaDbgWaveMsgAMDGen2& v)
{
  roctracer::kfd_support::output_streamer<char>::put(out, '{');
KFD_depth_max++;
  if (KFD_depth_max <= 0) {
    roctracer::kfd_support::output_streamer<const char*>::put(out, "Reserved2 = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.Reserved2);
    roctracer::kfd_support::output_streamer<const char*>::put(out, ", ");
    roctracer::kfd_support::output_streamer<const char*>::put(out, "Value = ");
    roctracer::kfd_support::output_streamer<HSAuint32>::put(out, v.Value);
  };
  KFD_depth_max--;
  roctracer::kfd_support::output_streamer<char>::put(out, '}');
  return out;
}
};
// end ostream ops for KFD 
};};

#endif //__cplusplus
#endif // INC_KFD_OSTREAM_OPS_H_
 
