#include "donuts_write_buffer.h"

DonutsWriteBuffer::DonutsWriteBuffer(UInt32 num_entries) : m_num_entries(num_entries), m_buffer()
{
   if (num_entries <= 1024)
      m_buffer.reserve(num_entries);
}

DonutsWriteBuffer::~DonutsWriteBuffer() {}

bool DonutsWriteBuffer::isFull()
{
   return m_buffer.size() == m_num_entries;
}

void DonutsWriteBuffer::insertEntry(CacheBlockInfo *cache_block_info)
{
   assert(m_buffer.size() < m_num_entries);
   m_buffer.push_back(cache_block_info);
}
