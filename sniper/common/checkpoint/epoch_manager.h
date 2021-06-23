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
    * @param ckpt 
    */
   void commitCheckpoint(const CheckpointEvent &ckpt);

   /**
    * @brief Register an epoch ID with the last persisted data
    * @param 
    */
   void registerPersistedEID(const UInt64 persisted_eid, const SubsecondTime &time);

   /**
    * @brief Get the System EpochID object
    * @return UInt64 
    */
   UInt64 getSystemEID() const { return m_system_eid; }

   UInt64 getCommitedEID() const { return m_commited.eid; }
   SubsecondTime getCommitedTime() const { return m_commited.time; }
   UInt64 getPersistedEID() const { return m_persisted.eid; }
   SubsecondTime getPersistedTime() const { return m_persisted.time; }

   /**
    * @brief Get the Instance object
    * @return EpochManager* 
    */
   static EpochManager *getInstance();

   /**
    * @brief Get the Global System E I D object
    * @return UInt64 
    */
   static UInt64 getGlobalSystemEID();

private:
   FILE *m_log_file;
   UInt64 m_system_eid;
   
   struct 
   {
      UInt64 eid;
      SubsecondTime time;
   } m_commited;

   struct
   {
      UInt64 eid;
      SubsecondTime time;
   } m_persisted;

   void start();
   void exit();

   static SInt64 __start(UInt64 arg, UInt64 val) { ((EpochManager *)arg)->start(); return 0; }
   static SInt64 __exit(UInt64 arg, UInt64 val) { ((EpochManager *)arg)->exit(); return 0; }
};

#endif /* EPOCH_MANAGER_H */