#include "checkpoint_event.h"
#include "epoch_manager.h"

CheckpointEvent::CheckpointEvent(Type event_type,
                                 UInt64 eid, const SubsecondTime &time,
                                 UInt64 num_logs, float cache_stocking)
    : m_type(event_type),
      m_eid(eid),
      m_time(time),
      m_num_logs(num_logs),
      m_cache_stocking(cache_stocking) {}

CheckpointEvent::CheckpointEvent(const CheckpointEvent &orig) = default;

CheckpointEvent::~CheckpointEvent() = default;

void CheckpointEvent::commit() const
{
   EpochManager::getInstance()->commitCheckpoint(*this);
}

//void CheckpointEvent::persist()
//{
////   EpochManager::getInstance()->registerPersistedEID(m_eid, now);
//}

const char *CheckpointEvent::TypeString(CheckpointEvent::Type type)
{
   switch (type)
   {
      case INSTRUCTION_RANGE:    return "INSTRUCTION_RANGE";
      case CACHE_SET_THRESHOLD:  return "CACHE_SET_THRESHOLD";
      case CACHE_THRESHOLD:      return "CACHE_THRESHOLD";
      case TIMEOUT:              return "TIMEOUT";
      default:                   return "?";
   }
}
