//#include "onchip_undo_buffer_cntlr.h"
//#include "onchip_undo_buffer.h"
//#include "epoch_manager.h"
//#include "hooks_manager.h"
//#include "magic_server.h"
//#include "memory_manager.h"
//#include "shmem_perf.h"
//#include "stats.h"
//#include "simulator.h"
//#include "config.hpp"
//#include <cstring>
//#include <cmath>
//
//namespace ParametricDramDirectoryMSI
//{
//    OnChipUndoBufferCntlr::OnChipUndoBufferCntlr(core_id_t core_id_master,
//                                                 MemoryManager *memory_manager,
//                                                 AddressHomeLookup *tag_directory_home_lookup,
//                                                 UInt32 cache_block_size,
//                                                 ShmemPerfModel *shmem_perf_model)
//            : m_core_id_master(core_id_master),
//              m_memory_manager(memory_manager),
//              m_tag_directory_home_lookup(tag_directory_home_lookup),
//              m_cache_block_size(cache_block_size),
//              m_shmem_perf_model(shmem_perf_model),
//              m_acs_gap(Sim()->getCfg()->hasKey("picl/acs_gap")
//                        ? Sim()->getCfg()->getInt("picl/acs_gap")
//                        : DEFAULT_ACS_GAP)
//    {
//        m_onchip_undo_buffer = new OnChipUndoBuffer(getNumEntries());
//
//        Sim()->getHooksManager()->registerHook(HookType::HOOK_PERIODIC_INS, __async_cache_scan, (UInt64)this);
//        Sim()->getHooksManager()->registerHook(HookType::HOOK_APPLICATION_EXIT, __persist_last_epochs, (UInt64)this);
//
//        memset(&stats, 0, sizeof(stats));
//        registerStatsMetric("onchip_undo_buffer", m_core_id_master, "log_writes", &stats.log_writes);
//        registerStatsMetric("onchip_undo_buffer", m_core_id_master, "avg_log_writes_by_epoch", &stats.avg_log_writes_by_epoch);
//        registerStatsMetric("onchip_undo_buffer", m_core_id_master, "overflow", &stats.overflow);
//    }
//
//    OnChipUndoBufferCntlr::~OnChipUndoBufferCntlr()
//    {
//        delete m_onchip_undo_buffer;
//    }
//
//    UInt32 OnChipUndoBufferCntlr::getNumEntries()
//    {
//        if (!Sim()->getCfg()->hasKey("picl/onchip_undo_buffer/num_entries"))
//            return DEFAULT_NUM_ENTRIES;
//
//        UInt32 num_entries = Sim()->getCfg()->getInt("picl/onchip_undo_buffer/num_entries");
//        return num_entries > 0 ? num_entries : UINT32_MAX;
//    }
//
//    void OnChipUndoBufferCntlr::insertUndoEntry(UInt64 system_eid, CacheBlockInfo *cache_block_info)
//    {
//        if (m_onchip_undo_buffer->isFull())
//        {
//            stats.overflow++;
//            UInt32 gap = system_eid > m_acs_gap ? m_acs_gap : system_eid;
//            do {
//                flush(system_eid - gap--);
//            } while (m_onchip_undo_buffer->isFull());
//        }
//        m_onchip_undo_buffer->insertUndoEntry(system_eid, cache_block_info);
//
//        // if (m_onchip_undo_buffer->isFull())
//        // {
//        //    stats.overflow++;
//        //    flush();
//        // }
//        // m_onchip_undo_buffer->insertUndoEntry(system_eid, cache_block_info);
//    }
//
//    void OnChipUndoBufferCntlr::flush(UInt64 persisted_eid)
//    {
//        auto log_entries = persisted_eid == EpochManager::getGlobalSystemEID()
//                           ? m_onchip_undo_buffer->removeAllEntries()
//                           : m_onchip_undo_buffer->removeOldEntries(persisted_eid);
//
//        while (!log_entries.empty())
//        {
//            auto entry = log_entries.front();
//            sendDataToNVM(entry);
//            log_entries.pop();
//            stats.log_writes++;
//        }
//        EpochManager::setGlobalPersistedEID(persisted_eid);
//    }
//
//    void OnChipUndoBufferCntlr::flush()
//    {
//        auto log_entries = m_onchip_undo_buffer->removeAllEntries();
//        while (!log_entries.empty())
//        {
//            auto entry = log_entries.front();
//            sendDataToNVM(entry);
//            log_entries.pop();
//            stats.log_writes++;
//        }
//    }
//
//    // TODO: Escrever uma classe para registar as métricas de cada ACS (quantas escritas por época?)
//    void OnChipUndoBufferCntlr::asyncCacheScan(UInt64 eid)
//    {
//        UInt64 system_eid = EpochManager::getGlobalSystemEID();
//        if (system_eid >= m_acs_gap)
//            flush(system_eid - m_acs_gap);
//    }
//
//    void OnChipUndoBufferCntlr::persistLastEpochs(UInt64 eid)
//    {
//        UInt64 system_eid = EpochManager::getGlobalSystemEID();
//        flush(system_eid);
//        stats.avg_log_writes_by_epoch = round(stats.log_writes / system_eid);
//
//        printf("[PiCL] Log writes: %lu\n[PiCL] Log writes (AVG by Epoch ID): %lu\n", stats.log_writes, stats.avg_log_writes_by_epoch);
//    }
//
//    void OnChipUndoBufferCntlr::sendDataToNVM(const UndoEntry &entry)
//    {
//        IntPtr address = getLogAddress();
//        Byte data_buf[getCacheBlockSize()];
//        getMemoryManager()->sendMsg(PrL1PrL2DramDirectoryMSI::ShmemMsg::CP_REP,
//                                    MemComponent::ONCHIP_UNDO_BUFFER, MemComponent::DRAM,
//                                    m_core_id_master, getHome(address), /* requester and receiver */
//                                    address, data_buf, getCacheBlockSize(),
//                                    HitWhere::UNKNOWN, &m_dummy_shmem_perf, ShmemPerfModel::_SIM_THREAD);
//    }
//
//}
