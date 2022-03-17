#ifndef ONCHIP_UNDO_BUFFER_H
#define ONCHIP_UNDO_BUFFER_H

#include <queue>
#include <vector>
#include "cache_block_info.h"
#include "mem_component.h"

class UndoEntry
{
public:
    UndoEntry(UInt64 system_eid, CacheBlockInfo *cache_block_info);
    UndoEntry(const UndoEntry &orig);

    virtual ~UndoEntry();

    IntPtr getTag() const { return m_tag; }
    UInt64 getValidFromEID() const { return m_valid_from_eid; }
    UInt64 getValidTillEID() const { return m_valid_till_eid; }

private:
    IntPtr m_tag;
    UInt64 m_valid_from_eid;
    UInt64 m_valid_till_eid;
    // UInt64 data;
};

class OnChipUndoBuffer
{
public:
    OnChipUndoBuffer(UInt32 num_entries = 0);
    virtual ~OnChipUndoBuffer();

    bool isFull();
    void insertUndoEntry(UInt64 system_eid, CacheBlockInfo *cache_block_info);
    std::queue<UndoEntry> removeOldEntries(UInt64 acs_eid);
    std::queue<UndoEntry> removeOldEntries();
    std::queue<UndoEntry> removeAllEntries();

    UInt32 getNumEntries() const { return m_num_entries; }
    String getName(void) const { return "On-Chip Undo Buffer"; }
    MemComponent::component_t getMemComponent() const { return MemComponent::ONCHIP_UNDO_BUFFER; }

    void print();

private:
    const UInt32 m_num_entries;      // Set 0 to an ilimited buffer
    std::vector<UndoEntry> m_buffer;
};

#endif /* ONCHIP_UNDO_BUFFER_H */
