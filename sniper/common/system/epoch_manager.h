#ifndef EPOCH_MANAGER_H
#define EPOCH_MANAGER_H

#include "subsecond_time.h"

// TODO: Move-me to a separated file???
class CheckpointEvent
{
public:
   enum checkpoint_event_t
   {
      CACHE_SET_THRESHOLD = 1,
      CACHE_THRESHOLD,
      TIMEOUT,
      NUM_CHECKPOINT_EVENTS = TIMEOUT
   };

   CheckpointEvent(checkpoint_event_t state) : state(state) {}
   ~CheckpointEvent() {}

private:
   checkpoint_event_t state;
   // SubsecondTime time;
};

class EpochManager
{
public:
   EpochManager();
   ~EpochManager();

   UInt64 getSystemEID() const { return m_system_eid; }
   UInt64 getPersistedEID() const { return m_persisted_eid; }

   static void globalCheckpoint(CheckpointEvent event);

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

   void checkpoint(CheckpointEvent event);

   static const UInt32 DEFAULT_TIMEOUT = 10000000;

   UInt64 m_system_eid;
   UInt64 m_persisted_eid;
   SubsecondTime m_timeout;
   SubsecondTime m_last_commit;

   FILE *m_log_file;
};

#endif /* EPOCH_MANAGER_H */