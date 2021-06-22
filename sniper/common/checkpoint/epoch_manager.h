#ifndef EPOCH_MANAGER_H
#define EPOCH_MANAGER_H

#include "checkpoint_info.h"

class EpochManager
{
public:
   EpochManager();
   ~EpochManager();

   void registerCheckpoint(const CheckpointInfo &ckpt);

   UInt64 getSystemEID() const { return m_system_eid; }
   UInt64 getPersistedEID() const { return m_last_checkpoint.getEpochID(); }
   SubsecondTime getPersistedTime() const { return m_last_checkpoint.getTime(); }

   static EpochManager *getInstance();
   static UInt64 getGlobalSystemEID();

private:
   UInt64 m_system_eid;
   CheckpointInfo m_last_checkpoint;
   FILE *m_log_file;

   void start();
   void exit();

   static SInt64 __start(UInt64 arg, UInt64 val) { ((EpochManager *)arg)->start(); return 0; }
   static SInt64 __exit(UInt64 arg, UInt64 val) { ((EpochManager *)arg)->exit(); return 0; }
};

#endif /* EPOCH_MANAGER_H */