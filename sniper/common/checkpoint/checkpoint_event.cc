#include "checkpoint_event.h"
#include "epoch_manager.h"

CheckpointEvent::CheckpointEvent(const Type event_type,
                                 const UInt64 eid, const SubsecondTime &time,
                                 const UInt64 num_logs, const float cache_stocking)
    : m_type(event_type),
      m_eid(eid),
      m_time(time),
      m_num_logs(num_logs),
      m_cache_stocking(cache_stocking) {}

CheckpointEvent::CheckpointEvent(const CheckpointEvent &orig)
    : m_type(orig.m_type),
      m_eid(orig.m_eid),
      m_time(orig.m_time),
      m_num_logs(orig.m_num_logs),
      m_cache_stocking(orig.m_cache_stocking) {}

CheckpointEvent::~CheckpointEvent() {}

void CheckpointEvent::commit()
{
   EpochManager::getInstance()->commitCheckpoint(*this);
}

const char *CheckpointEvent::TypeString(const CheckpointEvent::Type type)
{
   switch (type)
   {
      case CACHE_SET_THRESHOLD:  return "CACHE_SET_THRESHOLD";
      case CACHE_THRESHOLD:      return "CACHE_THRESHOLD";
      case TIMEOUT:              return "TIMEOUT";
      default:                   return "?";
   }
}
