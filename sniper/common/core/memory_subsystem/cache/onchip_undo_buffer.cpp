#include "onchip_undo_buffer.h"
#include <algorithm>

UndoEntry::UndoEntry(UInt64 system_eid, CacheBlockInfo *cache_block_info)
        : m_tag(cache_block_info->getTag()),
          m_valid_from_eid(cache_block_info->getEpochID()),
          m_valid_till_eid(system_eid) {}

UndoEntry::UndoEntry(const UndoEntry &orig)
        : m_tag(orig.m_tag),
          m_valid_from_eid(orig.m_valid_from_eid),
          m_valid_till_eid(orig.m_valid_till_eid) {}

UndoEntry::~UndoEntry() {}

OnChipUndoBuffer::OnChipUndoBuffer(UInt32 num_entries) : m_num_entries(num_entries), m_buffer()
{
    if (num_entries <= 1024)
        m_buffer.reserve(num_entries);
}

OnChipUndoBuffer::~OnChipUndoBuffer() {}

bool OnChipUndoBuffer::isFull()
{
    return m_buffer.size() == m_num_entries;
}

void OnChipUndoBuffer::insertUndoEntry(UInt64 system_eid, CacheBlockInfo *cache_block_info)
{
    assert(m_buffer.size() < m_num_entries);
    m_buffer.push_back(UndoEntry(system_eid, cache_block_info));
}

std::queue<UndoEntry> OnChipUndoBuffer::removeOldEntries(UInt64 acs_eid)
{
    std::queue<UndoEntry> old_entries;
    for (auto &entry : m_buffer)
    {
        if (entry.getValidTillEID() <= acs_eid)
            old_entries.push(std::move(entry));
    }
    m_buffer.erase(std::remove_if(m_buffer.begin(), m_buffer.end(), [&](const UndoEntry e)
                   { return e.getValidTillEID() <= acs_eid; }),
                   m_buffer.end());
    return old_entries;
}

std::queue<UndoEntry> OnChipUndoBuffer::removeOldEntries()
{
    auto min = std::min_element(m_buffer.begin(), m_buffer.end(),
                                [](const UndoEntry &a, const UndoEntry &b)
                                { return a.getValidTillEID() < b.getValidTillEID(); });
    return removeOldEntries(min->getValidTillEID());
}

std::queue<UndoEntry> OnChipUndoBuffer::removeAllEntries()
{
    std::queue<UndoEntry> all_entries(std::deque<UndoEntry>(m_buffer.begin(), m_buffer.end()));
    m_buffer.clear();
    return all_entries;
}

void OnChipUndoBuffer::print()
{
    printf("============================================================\n");
    printf("ON-CHIP UNDO BUFFER\n");
    printf("------------------------------------------------------------\n");
    printf("                TAG    FROM    TILL\n");
    for (std::size_t i = 0; i < m_buffer.size(); i++)
    {
        auto entry = m_buffer.at(i);
        printf("%3lu: [%13lu | %5lu | %5lu]\n", i, entry.getTag(), entry.getValidFromEID(), entry.getValidTillEID());
    }
    printf("============================================================\n");
}
