#ifndef CHECKPOINT_INFO_H
#define CHECKPOINT_INFO_H

#include "subsecond_time.h"

class CheckpointEvent
{
public:
   typedef enum type_t
   {
      INSTRUCTION_RANGE = 0,
      CACHE_SET_THRESHOLD,
      CACHE_THRESHOLD,
      TIMEOUT,
      NUM_EVENT_TYPES
   } Type;

   static const char *TypeString(Type type);

   /**
    * @brief Construct a new Checkpoint Event object
    * 
    * @param event_type 
    * @param eid 
    * @param time 
    * @param num_logs 
    * @param cache_stocking 
    */
   CheckpointEvent(Type event_type, UInt64 eid, const SubsecondTime &time, UInt64 num_logs, float cache_stocking);

   void commit() const;

   void persist() const;

   /**
    * @brief Construct a new Checkpoint Event object
    * @param orig 
    */
   CheckpointEvent(const CheckpointEvent &orig);

   /**
    * @brief Destroy the Checkpoint Event object
    */
   ~CheckpointEvent();

   /**
    * @brief Get the Type object
    * @return Type 
    */
   Type getType() const { return m_type; }

   /**
    * @brief Get the Epoch I D object
    * @return UInt64 
    */
   UInt64 getEpochID() const { return m_eid; }

   /**
    * @brief Get the Time object
    * @return SubsecondTime
    */
   const SubsecondTime &getTime() const { return m_time; }
   
   /**
    * @brief Get the Num Logs object
    * @return UInt64 
    */
   UInt64 getNumLogs() const { return m_num_logs; }

   /**
    * @brief Get the Cache Stocking object
    * @return float 
    */
   float getCacheStocking() const { return m_cache_stocking; }

private:
   Type m_type;
   UInt64 m_eid;
   SubsecondTime m_time;

   // Statistics //
   UInt64 m_num_logs;
   float m_cache_stocking;
};

#endif /* CHECKPOINT_INFO_H */