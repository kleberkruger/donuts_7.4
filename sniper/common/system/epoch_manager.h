#ifndef EPOCH_MANAGER_H
#define EPOCH_MANAGER_H

#include "cache_block_info.h"
#include "subsecond_time.h"

#include <queue>

class EpochManager
{
public:
   EpochManager();
   ~EpochManager();

   UInt64 getSystemEID() const { return m_system_eid; }
   UInt64 getPersistedEID() const { return m_persisted_eid; }

   static void globalCheckpoint(SubsecondTime now, std::queue<CacheBlockInfo *> dirty_blocks);

   static UInt64 getGlobalSystemEID();

private:
   static SInt64 __start(UInt64 arg, UInt64 val)
   {
      ((EpochManager *)arg)->start();
      return 0;
   }
   void start();

   static SInt64 __exit(UInt64 arg, UInt64 val)
   {
      ((EpochManager *)arg)->exit();
      return 0;
   }
   void exit();

   static SInt64 __timeout(UInt64 arg, UInt64 val)
   {
      ((EpochManager *)arg)->timeout();
      return 0;
   }
   void timeout();

   void checkpoint(SubsecondTime now, std::queue<CacheBlockInfo *> dirty_blocks);

   UInt64 m_system_eid;
   UInt64 m_persisted_eid;
   SubsecondTime m_last_commit;

   FILE *m_log_file;
};

#endif