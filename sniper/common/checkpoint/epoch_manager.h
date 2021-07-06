#ifndef EPOCH_MANAGER_H
#define EPOCH_MANAGER_H

#include "checkpoint_event.h"

class EpochManager
{
public:

   /**
    * @brief Construct a new Epoch Manager object
    */
   EpochManager();

   /**
    * @brief Destroy the Epoch Manager object
    */
   ~EpochManager();

   /**
    * @brief Commit a checkpoint
    * @param checkpoint
    */
   void commitCheckpoint(const CheckpointEvent &checkpoint);

   /**
    * @brief Register an epoch ID with the last persisted data
    * @param 
    */
   void registerPersistedEID(UInt64 persisted_eid, const SubsecondTime &time);

   /**
    * @brief Get the System EpochID object
    * @return UInt64 
    */
   UInt64 getSystemEID() const { return m_system_eid; }

   /**
    * @brief Get the Commited EpochID object
    * @return UInt64
    */
   UInt64 getCommitedEID() const { return m_commited.eid; }

   /**
    * @brief Get the Commited Time object
    * @return SubsecondTime
    */
   SubsecondTime getCommitedTime() const { return m_commited.time; }

   /**
    * @brief Get the Persisted EpochID object
    * @return UInt64
    */
   UInt64 getPersistedEID() const { return m_persisted.eid; }

   /**
    * @brief Get the Persisted Time object
    * @return SubsecondTime
    */
   SubsecondTime getPersistedTime() const { return m_persisted.time; }

   /**
    * @brief Get the Instance object
    * @return EpochManager* 
    */
   static EpochManager *getInstance();

   /**
    * @brief Get the Global SystemEID object
    * @return UInt64 
    */
   static UInt64 getGlobalSystemEID();

private:
   struct epoch_instant_t
   {
      UInt64 eid;
      SubsecondTime time;
   };

   FILE *m_log_file;
   UInt64 m_system_eid;
   struct epoch_instant_t m_commited;
   struct epoch_instant_t m_persisted;

   void start();
   void exit();

   static SInt64 _start(UInt64 arg, UInt64 val) { ((EpochManager *)arg)->start(); return 0; }
   static SInt64 _exit(UInt64 arg, UInt64 val) { ((EpochManager *)arg)->exit(); return 0; }
};

#endif /* EPOCH_MANAGER_H */