#ifndef DONUTS_WRITE_BUFFER_H
#define DONUTS_WRITE_BUFFER_H

#include "cache_block_info.h"
#include <vector>

class DonutsWriteBuffer
{
public:
   DonutsWriteBuffer(UInt32 num_entries = 0);
   virtual ~DonutsWriteBuffer();

private:
   const UInt32 m_num_entries; // Set 0 to an ilimited buffer
   std::vector<CacheBlockInfo *> m_buffer;
};

#endif /* DONUTS_WRITE_BUFFER_H */