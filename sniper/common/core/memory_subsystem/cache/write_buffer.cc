#include "write_buffer.h"
#include <algorithm>

WriteBuffer::WriteBuffer(UInt32 num_entries) : m_num_entries(num_entries), m_buffer()
{
   if (num_entries <= 1024)
      m_buffer.reserve(num_entries);
}

WriteBuffer::~WriteBuffer() {}

bool WriteBuffer::isFull()
{
   return m_buffer.size() == m_num_entries;
}

void WriteBuffer::insertEntry(CacheBlockInfo *cache_block_info)
{
   assert(m_buffer.size() < m_num_entries);
   m_buffer.push_back(cache_block_info);
}

void WriteBuffer::print()
{
   printf("============================================================\n");
   printf("ON-CHIP UNDO BUFFER\n");
   printf("------------------------------------------------------------\n");
   printf("                TAG    FROM    TILL\n");
   for (std::size_t i = 0; i < m_buffer.size(); i++)
   {
//      auto entry = m_buffer.at(i);
//      printf("%3lu: [%13lu | %5lu | %5lu]\n", i, entry.getTag(), entry.getValidFromEID(), entry.getValidTillEID());
   }
   printf("============================================================\n");
}