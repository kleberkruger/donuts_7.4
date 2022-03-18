//#ifndef WRITE_BUFFER_CNTLR_H
//#define WRITE_BUFFER_CNTLR_H
//
//#include "write_buffer.h"
//#include "cache_block_info.h"
//#include "address_home_lookup.h"
//#include "shmem_perf.h"
//#include "shmem_perf_model.h"
//
//// Forward declarations
//namespace ParametricDramDirectoryMSI
//{
//   class MemoryManager;
//}
//// class ShmemPerf;
//
//namespace ParametricDramDirectoryMSI
//{
//class WriteBufferCntlr
//{
//public:
//
//   /**
//    * Construct a WriteBufferCntlr.
//    *
//    * @param core_id
//    * @param memory_manager
//    * @param tag_directory_home_lookup
//    * @param cache_block_size
//    * @param shmem_perf_model
//    */
//   WriteBufferCntlr(core_id_t core_id,
//                    MemoryManager *memory_manager,
//                    AddressHomeLookup *tag_directory_home_lookup,
//                    UInt32 cache_block_size,
//                    ShmemPerfModel *shmem_perf_model);
//
//   /**
//    * Destruct the WriteBufferCntlr with it WriteBuffer.
//    */
//   ~WriteBufferCntlr();
//
//   /**
//    * Insert a new entry.
//    * @param cache_block_info
//    */
//   void insertEntry(CacheBlockInfo *cache_block_info);
//
//   /**
//    * Flushes all entries to NVM.
//    */
//   void flush();
//
//   /**
//    * Get the write buffer component.
//    * @return the WriteBuffer
//    */
//   WriteBuffer *getWriteBuffer() { return m_write_buffer; }
//
//   friend class MemoryManager;
//
//private:
//   struct
//   {
//      UInt64 log_writes;
//      UInt64 avg_log_writes_by_epoch;
//      UInt64 overflow;
//   } stats;
//
//   static const UInt32 DEFAULT_NUM_ENTRIES = 32;
//
//   core_id_t m_core_id_master;
//   MemoryManager *m_memory_manager;
//   AddressHomeLookup *m_tag_directory_home_lookup;
//   UInt32 m_cache_block_size;
//   ShmemPerf m_dummy_shmem_perf;
//   ShmemPerfModel *m_shmem_perf_model;
//   WriteBuffer *m_write_buffer;
//
//   // Dram Directory Home Lookup
//   core_id_t getHome(IntPtr address) { return m_tag_directory_home_lookup->getHome(address); }
//   UInt32 getCacheBlockSize() const { return m_cache_block_size; }
//   MemoryManager *getMemoryManager() { return m_memory_manager; }
//   ShmemPerfModel *getShmemPerfModel() { return m_shmem_perf_model; }
//
//   void sendDataToNVM(const CacheBlockInfo *cache_block);
//
//   static UInt32 getNumEntries();
//};
//}
//
//#endif /* WRITE_BUFFER_CNTLR_H */
