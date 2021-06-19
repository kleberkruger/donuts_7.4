#include "donuts_utils.h"
#include "cache.h"

char CStateString(CacheState::cstate_t cstate) {
   switch(cstate)
   {
      case CacheState::INVALID:           return 'I';
      case CacheState::SHARED:            return 'S';
      case CacheState::SHARED_UPGRADING:  return 'u';
      case CacheState::MODIFIED:          return 'M';
      case CacheState::EXCLUSIVE:         return 'E';
      case CacheState::OWNED:             return 'O';
      case CacheState::INVALID_COLD:      return '_';
      case CacheState::INVALID_EVICT:     return 'e';
      case CacheState::INVALID_COHERENCY: return 'c';
      default:                            return '?';
   }
}

void DonutsUtils::printCache(Cache *cache)
{
   printf("Cache %s\n--------------------------------------------------\n%5s", cache->getName().c_str(), "");
   for (UInt32 j = 0; j < cache->getAssociativity(); j++)
      printf("%2d  ", j);
   printf("\n--------------------------------------------------\n");

   for (UInt32 i = 0; i < cache->getNumSets(); i++)
   {
      printf("%4d ", i);
      for (UInt32 j = 0; j < cache->getAssociativity(); j++)
      {
         auto cache_block = cache->peekBlock(i, j);
         auto cstate = cache_block->getCState();
         printf("[%c %lu] ", cstate != CacheState::INVALID ? CStateString(cache_block->getCState()) : ' ', cache_block->getEpochID());
      }
      printf("\n");
   }
   printf("\n");
}