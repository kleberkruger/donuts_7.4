#ifndef CACHE_SET_LRUR_H
#define CACHE_SET_LRUR_H

#include "cache_set_lru.h"

class CacheSetLRUR : public CacheSetLRU
{
public:
   CacheSetLRUR(CacheBase::cache_t cache_type, UInt32 associativity, UInt32 blocksize,
                CacheSetInfoLRU *set_info, UInt8 num_attempts,
                float checkpoint_threshold = DEFAULT_CHECKPOINT_THRESHOLD);
   virtual ~CacheSetLRUR();

   virtual UInt32 getReplacementIndex(CacheCntlr *cntlr);

protected:
   static const constexpr float DEFAULT_CHECKPOINT_THRESHOLD = 1.0;
   float m_checkpoint_th;

   bool isValidReplacement(UInt32 index);
};

#endif /* CACHE_SET_LRUR_H */