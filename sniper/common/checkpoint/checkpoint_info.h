#ifndef CHECKPOINT_INFO_H
#define CHECKPOINT_INFO_H

#include "subsecond_time.h"

class CheckpointInfo
{
public:
   typedef enum event_type_t
   {
      CACHE_SET_THRESHOLD = 1,
      CACHE_THRESHOLD,
      TIMEOUT,
      NUM_EVENT_TYPES = TIMEOUT
   } EventType;

   CheckpointInfo(const EventType event_type,
                  const UInt64 num_logs, const float cache_stocking,
                  UInt64 eid, const SubsecondTime &time)
       : m_event_type(event_type),
         m_num_logs(num_logs),
         m_cache_stocking(cache_stocking),
         m_eid(eid),
         m_time(time) {}

   CheckpointInfo(const CheckpointInfo &orig)
       : m_event_type(orig.m_event_type),
         m_num_logs(orig.m_num_logs),
         m_cache_stocking(orig.m_cache_stocking),
         m_eid(orig.m_eid),
         m_time(orig.m_time) {}

   ~CheckpointInfo() {}

   UInt64 getEpochID() const { return m_eid; }
   EventType getEventType() const { return m_event_type; }
   UInt64 getNumLogs() const { return m_num_logs; }
   float getCacheStocking() const { return m_cache_stocking; }
   SubsecondTime getTime() const { return m_time; }

private:
   EventType m_event_type;
   UInt64 m_num_logs;
   float m_cache_stocking;
   UInt64 m_eid;
   SubsecondTime m_time;
   // SubsecondTime m_gap; // store time between now and the last checkpoint?
};

#endif /* CHECKPOINT_INFO_H */