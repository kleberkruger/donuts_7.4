#pragma once

// Define to re-enable DramAccessCount
//#define ENABLE_DRAM_ACCESS_COUNT

#include <unordered_map>

#include "dram_perf_model.h"
#include "shmem_msg.h"
#include "shmem_perf.h"
#include "fixed_types.h"
#include "memory_manager_base.h"
#include "dram_cntlr_interface.h"
#include "subsecond_time.h"
#include "dram_cntlr.h"

class FaultInjector;

namespace PrL1PrL2DramDirectoryMSI
{
   class NvmCntlr : public DramCntlr
   {
      private:
         UInt64 m_logs;
         UInt64 m_log_ends; 
         UInt32 m_log_buffer;
         UInt32 m_log_size;  
         bool m_log_enabled;
         bool m_log_type;

         SubsecondTime runDramPerfModel(core_id_t requester, SubsecondTime time, IntPtr address, DramCntlrInterface::access_t access_type, ShmemPerf *perf);

         void addToDramAccessCount(IntPtr address, access_t access_type);
         void printDramAccessCount(void);

         static bool getLogEnabled();
         static UInt32 getLogRowBufferSize();
         static bool getLogType();

         static void createLogEntry(IntPtr address, Byte* data_buf);

      public:
         NvmCntlr(MemoryManagerBase* memory_manager,
               ShmemPerfModel* shmem_perf_model,
               UInt32 cache_block_size);

         ~NvmCntlr() = default;

         // Run DRAM performance model. Pass in begin time, returns latency
         boost::tuple<SubsecondTime, HitWhere::where_t> getDataFromDram(IntPtr address, core_id_t requester, Byte* data_buf, SubsecondTime now, ShmemPerf *perf);
         boost::tuple<SubsecondTime, HitWhere::where_t> putDataToDram(IntPtr address, core_id_t requester, Byte* data_buf, SubsecondTime now);
         
         // For Donuts NVM model
         boost::tuple<SubsecondTime, HitWhere::where_t> logDataToDram(IntPtr address, core_id_t requester, Byte* data_buf, SubsecondTime now);

         // TODO: implement this method called on checkpoint events
         void checkpoint();
   };
}
