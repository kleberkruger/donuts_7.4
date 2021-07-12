#ifndef NVM_PERF_MODEL_CONSTANT_H
#define NVM_PERF_MODEL_CONSTANT_H

#include "dram_perf_model.h"
#include "queue_model.h"
#include "fixed_types.h"
#include "subsecond_time.h"
#include "dram_cntlr_interface.h"

class NvmPerfModelConstant : public DramPerfModel
{
private:
   QueueModel *m_queue_model;
   SubsecondTime m_nvm_read_cost;
   SubsecondTime m_nvm_write_cost;
   ComponentBandwidth m_nvm_bandwidth;

   SubsecondTime m_total_queueing_delay;
   SubsecondTime m_total_access_latency;

public:
   NvmPerfModelConstant(core_id_t core_id, UInt32 cache_block_size);
   ~NvmPerfModelConstant() override;

   SubsecondTime getAccessLatency(SubsecondTime pkt_time, UInt64 pkt_size, core_id_t requester, IntPtr address,
                                  DramCntlrInterface::access_t access_type, ShmemPerf *perf) override;
};

#endif // NVM_PERF_MODEL_CONSTANT_H
