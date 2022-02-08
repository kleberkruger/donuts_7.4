// #include "nvm_cntlr.h"
// #include "memory_manager.h"
// #include "core.h"
// #include "log.h"
// #include "subsecond_time.h"
// #include "stats.h"
// #include "fault_injection.h"
// #include "shmem_perf.h"
// #include "config.h"           // Added by Kleber Kruger
// #include "config.hpp"         // Added by Kleber Kruger
// #include "nvm_perf_model.h"   // Added by Kleber Kruger

// #if 0
//    extern Lock iolock;
// #  include "core_manager.h"
// #  include "simulator.h"
// #  define MYLOG(...) { ScopedLock l(iolock); fflush(stdout); printf("[%s] %d%cdr %-25s@%3u: ", itostr(getShmemPerfModel()->getElapsedTime()).c_str(), getMemoryManager()->getCore()->getId(), Sim()->getCoreManager()->amiUserThread() ? '^' : '_', __FUNCTION__, __LINE__); printf(__VA_ARGS__); printf("\n"); fflush(stdout); }
// #else
// #  define MYLOG(...) {}
// #endif

// class TimeDistribution;

// namespace PrL1PrL2DramDirectoryMSI
// {

// NvmCntlr::NvmCntlr(MemoryManagerBase* memory_manager,
//       ShmemPerfModel* shmem_perf_model,
//       UInt32 cache_block_size)
//    : DramCntlrInterface(memory_manager, shmem_perf_model, cache_block_size)
//    , m_reads(0)
//    , m_writes(0)
//    , m_logs(0)
//    , m_log_enabled(Sim()->getCfg()->getBool("perf_model/dram/log_enabled"))
// {
// //   m_dram_perf_model = DramPerfModel::createDramPerfModel(
// //         memory_manager->getCore()->getId(),
// //         cache_block_size);
//    m_dram_perf_model = createDramPerfModel(memory_manager->getCore()->getId(), cache_block_size); // Modified by Kleber Kruger (old implementation above)

//    m_fault_injector = Sim()->getFaultinjectionManager()
//       ? Sim()->getFaultinjectionManager()->getFaultInjector(memory_manager->getCore()->getId(), MemComponent::DRAM)
//       : NULL;

//    m_dram_access_count = new AccessCountMap[DramCntlrInterface::NUM_ACCESS_TYPES];
//    registerStatsMetric("dram", memory_manager->getCore()->getId(), "reads", &m_reads);
//    registerStatsMetric("dram", memory_manager->getCore()->getId(), "writes", &m_writes);
//    registerStatsMetric("dram", memory_manager->getCore()->getId(), "logs", &m_logs); // Added by Kleber Kruger
// }

// NvmCntlr::~NvmCntlr()
// {
//    printDramAccessCount();
//    delete [] m_dram_access_count;

//    delete m_dram_perf_model;
// }

// boost::tuple<SubsecondTime, HitWhere::where_t>
// NvmCntlr::getDataFromDram(IntPtr address, core_id_t requester, Byte* data_buf, SubsecondTime now, ShmemPerf *perf)
// {
//    if (Sim()->getFaultinjectionManager())
//    {
//       if (m_data_map.count(address) == 0)
//       {
//          m_data_map[address] = new Byte[getCacheBlockSize()];
//          memset((void*) m_data_map[address], 0x00, getCacheBlockSize());
//       }

//       // NOTE: assumes error occurs in memory. If we want to model bus errors, insert the error into data_buf instead
//       if (m_fault_injector)
//          m_fault_injector->preRead(address, address, getCacheBlockSize(), (Byte*)m_data_map[address], now);

//       memcpy((void*) data_buf, (void*) m_data_map[address], getCacheBlockSize());
//    }

//    // Added by Kleber Kruger
//    if (m_log_enabled) logDataToDram(address, requester, data_buf, now);

//    // printf("getDataFromDram (%lu)\n", address); // Added by Kleber Kruger
//    SubsecondTime dram_access_latency = runDramPerfModel(requester, now, address, READ, perf);

//    ++m_reads;
//    #ifdef ENABLE_DRAM_ACCESS_COUNT
//    addToDramAccessCount(address, READ);
//    #endif
//    MYLOG("R @ %08lx latency %s", address, itostr(dram_access_latency).c_str());

//    return boost::tuple<SubsecondTime, HitWhere::where_t>(dram_access_latency, HitWhere::DRAM);
// }

// boost::tuple<SubsecondTime, HitWhere::where_t>
// NvmCntlr::putDataToDram(IntPtr address, core_id_t requester, Byte* data_buf, SubsecondTime now)
// {
//    if (Sim()->getFaultinjectionManager())
//    {
//       if (m_data_map[address] == NULL)
//       {
//          LOG_PRINT_ERROR("Data Buffer does not exist");
//       }
//       memcpy((void*) m_data_map[address], (void*) data_buf, getCacheBlockSize());

//       // NOTE: assumes error occurs in memory. If we want to model bus errors, insert the error into data_buf instead
//       if (m_fault_injector)
//          m_fault_injector->postWrite(address, address, getCacheBlockSize(), (Byte*)m_data_map[address], now);
//    }

//    // Added by Kleber Kruger
//    if (m_log_enabled) logDataToDram(address, requester, data_buf, now);

//    // printf("putDataToDram (%lu)\n", address); // Added by Kleber Kruger
//    SubsecondTime dram_access_latency = runDramPerfModel(requester, now, address, WRITE, &m_dummy_shmem_perf);

//    ++m_writes;
//    #ifdef ENABLE_DRAM_ACCESS_COUNT
//    addToDramAccessCount(address, WRITE);
//    #endif
//    MYLOG("W @ %08lx", address);

//    return boost::tuple<SubsecondTime, HitWhere::where_t>(dram_access_latency, HitWhere::DRAM);
// }

// boost::tuple<SubsecondTime, HitWhere::where_t>
// NvmCntlr::logDataToDram(IntPtr address, core_id_t requester, Byte* data_buf, SubsecondTime now)
// {
//    // if (Sim()->getFaultinjectionManager())
//    // {
//    //    if (m_data_map[address] == NULL)
//    //    {
//    //       LOG_PRINT_ERROR("Data Buffer does not exist");
//    //    }
//    //    memcpy((void*) m_data_map[address], (void*) data_buf, getCacheBlockSize());

//    //    // NOTE: assumes error occurs in memory. If we want to model bus errors, insert the error into data_buf instead
//    //    if (m_fault_injector)
//    //       m_fault_injector->postWrite(address, address, getCacheBlockSize(), (Byte*)m_data_map[address], now);
//    // }

//    // printf("logDataToDram (%lu)\n", address); // Added by Kleber Kruger
//    createLogEntry(address, data_buf);
//    SubsecondTime dram_access_latency = runDramPerfModel(requester, now, address, LOG, &m_dummy_shmem_perf);

//    ++m_logs;
//    #ifdef ENABLE_DRAM_ACCESS_COUNT
//    addToDramAccessCount(address, LOG);
//    #endif
//    MYLOG("L @ %08lx", address);

//    return boost::tuple<SubsecondTime, HitWhere::where_t>(dram_access_latency, HitWhere::DRAM);
// }

// SubsecondTime
// NvmCntlr::runDramPerfModel(core_id_t requester, SubsecondTime time, IntPtr address, DramCntlrInterface::access_t access_type, ShmemPerf *perf)
// {
//    UInt64 pkt_size = getCacheBlockSize();
//    SubsecondTime dram_access_latency = m_dram_perf_model->getAccessLatency(time, pkt_size, requester, address, access_type, perf);

//    // Added by Kleber Kruger
//    printf("%5s | [%16lu] (%luns)\n", access_type == DramCntlrInterface::WRITE ? "WRITE" : 
//                                      access_type == DramCntlrInterface::READ ? "READ" : "LOG",
//                                      address, dram_access_latency.getNS());

//    return dram_access_latency;
// }

// void
// NvmCntlr::addToDramAccessCount(IntPtr address, DramCntlrInterface::access_t access_type)
// {
//    m_dram_access_count[access_type][address] = m_dram_access_count[access_type][address] + 1;
// }

// void
// NvmCntlr::printDramAccessCount()
// {
//    for (UInt32 k = 0; k < DramCntlrInterface::NUM_ACCESS_TYPES; k++)
//    {
//       for (AccessCountMap::iterator i = m_dram_access_count[k].begin(); i != m_dram_access_count[k].end(); i++)
//       {
//          if ((*i).second > 100)
//          {
//             LOG_PRINT("Dram Cntlr(%i), Address(0x%x), Access Count(%llu), Access Type(%s)",
//                   m_memory_manager->getCore()->getId(), (*i).first, (*i).second,
//                   (k == READ)? "READ" : "WRITE");
//          }
//       }
//    }
// }

// DramPerfModel*
// NvmCntlr::createDramPerfModel(core_id_t core_id, UInt32 cache_block_size)
// {
//    String param = "perf_model/dram/technology";
//    return Sim()->getCfg()->hasKey(param) && Sim()->getCfg()->getString(param) == "nvm" ?
//           NvmPerfModel::createNvmPerfModel(core_id, cache_block_size) :
//           DramPerfModel::createDramPerfModel(core_id, cache_block_size);
// }

// void
// NvmCntlr::createLogEntry(IntPtr address, Byte* data_buf)
// {
//    printf("Creating log entry { metadata: %lu, data: %u }\n", address, (unsigned int) *data_buf);
// }

// }