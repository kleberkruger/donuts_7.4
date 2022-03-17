#ifndef ONCHIP_UNDO_BUFFER_CNTLR_H
#define ONCHIP_UNDO_BUFFER_CNTLR_H

#include "onchip_undo_buffer.h"
#include "address_home_lookup.h"
#include "shmem_perf.h"
#include "shmem_perf_model.h"

// Forward declarations
namespace ParametricDramDirectoryMSI
{
    class MemoryManager;
}
// class ShmemPerf;

namespace ParametricDramDirectoryMSI
{

    class OnChipUndoBufferCntlr
    {
    public:
        OnChipUndoBufferCntlr(
                core_id_t core_id,
                MemoryManager *memory_manager,
                AddressHomeLookup *tag_directory_home_lookup,
                UInt32 cache_block_size,
                ShmemPerfModel *shmem_perf_model);
        ~OnChipUndoBufferCntlr();

        void insertUndoEntry(UInt64 system_eid, CacheBlockInfo *cache_block_info);

        // to new version...
        bool isPresent(CacheBlockInfo *cache_block_info) { return false; }
        void flush();

        OnChipUndoBuffer *getOnChipUndoBuffer() { return m_onchip_undo_buffer; }

        friend class MemoryManager;

    private:
        struct
        {
            UInt64 log_writes;
            UInt64 avg_log_writes_by_epoch;
            UInt64 overflow;
        } stats;

        static const UInt32 DEFAULT_ACS_GAP = 3;
        static const UInt32 DEFAULT_NUM_ENTRIES = 32;

        core_id_t m_core_id_master;
        MemoryManager *m_memory_manager;
        AddressHomeLookup *m_tag_directory_home_lookup;
        UInt32 m_cache_block_size;
        ShmemPerf m_dummy_shmem_perf;
        ShmemPerfModel *m_shmem_perf_model;
        OnChipUndoBuffer *m_onchip_undo_buffer;
        UInt32 m_acs_gap;

        // Dram Directory Home Lookup
        core_id_t getHome(IntPtr address) { return m_tag_directory_home_lookup->getHome(address); }

        UInt32 getCacheBlockSize() { return m_cache_block_size; }
        IntPtr getLogAddress() { return UINT32_MAX; }
        MemoryManager *getMemoryManager() { return m_memory_manager; }
        ShmemPerfModel *getShmemPerfModel() { return m_shmem_perf_model; }

        UInt32 getNumEntries();

        void flush(UInt64 eid);

        void sendDataToNVM(const UndoEntry &undo_entry);

        static SInt64 __async_cache_scan(UInt64 arg, UInt64 val)
        {
            ((OnChipUndoBufferCntlr *)arg)->asyncCacheScan(val);
            return 0;
        }
        void asyncCacheScan(UInt64 eid);

        static SInt64 __persist_last_epochs(UInt64 arg, UInt64 val)
        {
            ((OnChipUndoBufferCntlr *)arg)->persistLastEpochs(val);
            return 0;
        }
        void persistLastEpochs(UInt64 eid);
    };

}

#endif /* ONCHIP_UNDO_BUFFER_CNTLR_H */
