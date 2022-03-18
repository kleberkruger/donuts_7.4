#ifndef WRITE_BUFFER_H
#define WRITE_BUFFER_H

#include <queue>
#include <vector>
#include "cache_block_info.h"
#include "mem_component.h"

class WriteBuffer
{
public:

   /**
    * Construct a write buffer with <num_entries> size.
    * @param num_entries Number of entries (set 0 to an unlimited buffer)
    */
   explicit WriteBuffer(UInt32 num_entries = 0);

   /**
    * Destroy the buffer.
    */
   virtual ~WriteBuffer();

   /**
    * Get the buffer capacity status.
    * @return true if the buffer is full, false in other case
    */
   bool isFull();

   /**
    * Insert a entry.
    * @param cache_block_info
    */
   void insertEntry(CacheBlockInfo *cache_block_info);

   /**
    * Clean the buffer.
    */
   void clear();

   /**
    * Get the buffer capacity.
    * @return the number of entries
    */
   UInt32 getNumEntries() const { return m_num_entries; }

   /**
    * (!DEBUGGER!)
    * Print elements in the buffer.
    */
   void print();

private:

   const UInt32 m_num_entries;
   std::vector<CacheBlockInfo *> m_buffer;
};

#endif /* WRITE_BUFFER_H */
