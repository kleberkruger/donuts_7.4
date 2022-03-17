#ifndef WRITE_BUFFER_H
#define WRITE_BUFFER_H

#include <queue>
#include <vector>
#include "cache_block_info.h"
#include "mem_component.h"

class WriteBuffer
{
public:
   WriteBuffer(UInt32 num_entries = 0);
   virtual ~WriteBuffer();

   bool isFull();
   void insertEntry(CacheBlockInfo *cache_block_info);

   UInt32 getNumEntries() const { return m_num_entries; }
   String getName() const { return "Write Buffer"; }

   void print();

private:
   const UInt32 m_num_entries; // Set 0 to an unlimited buffer
   std::vector<CacheBlockInfo *> m_buffer;
};

#endif /* WRITE_BUFFER_H */
