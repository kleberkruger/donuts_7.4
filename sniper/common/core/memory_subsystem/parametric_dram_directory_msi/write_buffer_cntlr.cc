//#include "write_buffer_cntlr.h"
//#include "write_buffer.h"
//#include "cache_block_info.h"
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
//
//WriteBufferCntlr::WriteBufferCntlr(core_id_t core_id_master,
//                                   MemoryManager *memory_manager,
//                                   AddressHomeLookup *tag_directory_home_lookup,
//                                   UInt32 cache_block_size,
//                                   ShmemPerfModel *shmem_perf_model)
//      : m_core_id_master(core_id_master),
//        m_memory_manager(memory_manager),
//        m_tag_directory_home_lookup(tag_directory_home_lookup),
//        m_cache_block_size(cache_block_size),
//        m_shmem_perf_model(shmem_perf_model)
//{
//   m_write_buffer = new WriteBuffer(getNumEntries());
//
//   memset(&stats, 0, sizeof(stats));
//   registerStatsMetric("write_buffer", m_core_id_master, "log_writes", &stats.log_writes);
//   registerStatsMetric("write_buffer", m_core_id_master, "avg_log_writes_by_epoch", &stats.avg_log_writes_by_epoch);
//   registerStatsMetric("write_buffer", m_core_id_master, "overflow", &stats.overflow);
//}
//
//WriteBufferCntlr::~WriteBufferCntlr()
//{
//   delete m_write_buffer;
//}
//
//void WriteBufferCntlr::insertEntry(CacheBlockInfo *cache_block_info)
//{
////   if (m_write_buffer->isFull())
////   {
////      stats.overflow++;
////      UInt32 gap = system_eid > m_acs_gap ? m_acs_gap : system_eid;
////      do {
////         flush(system_eid - gap--);
////      } while (m_onchip_undo_buffer->isFull());
////   }
////   m_write_buffer->insertEntry(system_eid, cache_block_info);
////
////   // if (m_onchip_undo_buffer->isFull())
////   // {
////   //    stats.overflow++;
////   //    flush();
////   // }
////   // m_onchip_undo_buffer->insertUndoEntry(system_eid, cache_block_info);
//}
//
//
//void WriteBufferCntlr::flush()
//{
////   auto log_entries = m_write_buffer->removeAllEntries();
////   while (!log_entries.empty())
////   {
////      auto entry = log_entries.front();
////      sendDataToNVM(entry);
////      log_entries.pop();
////      stats.log_writes++;
////   }
//}
//
//void WriteBufferCntlr::sendDataToNVM(const CacheBlockInfo *cache_block)
//{
////   IntPtr address = nullptr; // FIXME: Ajustar o endereço
////   Byte data_buf[getCacheBlockSize()];
////   getMemoryManager()->sendMsg(PrL1PrL2DramDirectoryMSI::ShmemMsg::CP_REP,
////                               MemComponent::LAST_LEVEL_CACHE, MemComponent::NVM,
////                               m_core_id_master, getHome(address), /* requester and receiver */
////                               address, data_buf, getCacheBlockSize(),
////                               HitWhere::UNKNOWN, &m_dummy_shmem_perf, ShmemPerfModel::_SIM_THREAD);
//}
//
//UInt32 WriteBufferCntlr::getNumEntries()
//{
//   if (!Sim()->getCfg()->hasKey("donuts/write_buffer/num_entries"))
//      return DEFAULT_NUM_ENTRIES;
//
//   UInt32 num_entries = Sim()->getCfg()->getInt("donuts/write_buffer/num_entries");
//   return num_entries > 0 ? num_entries : UINT32_MAX;
//}
//
//}
