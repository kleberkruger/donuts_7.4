#ifndef EPOCH_MANAGER_H
#define EPOCH_MANAGER_H

#include "checkpoint_event.h"
#include "subsecond_time.h"

class EpochManager
{
public:
   EpochManager();
   ~EpochManager();

   UInt64 getSystemEID() const { return m_system_eid; }
   UInt64 getPersistedEID() const { return m_persisted_eid; }
   SubsecondTime getLast() const { return m_last_commit; }

   static void registerCheckpoint(const CheckpointEvent &event);

   static UInt64 getGlobalSystemEID();
   static SubsecondTime getLastCommit();

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

   void checkpoint(const CheckpointEvent &event);

   static const UInt32 DEFAULT_TIMEOUT = 25000;

   UInt64 m_system_eid;
   UInt64 m_persisted_eid;
   SubsecondTime m_timeout;
   SubsecondTime m_last_commit;

   FILE *m_log_file;
};

#endif /* EPOCH_MANAGER_H */