#ifndef CHECKPOINT_EVENT_H
#define CHECKPOINT_EVENT_H

#include "subsecond_time.h"

class CheckpointEvent
{
public:
    enum type_t
    {
        CACHE_SET_THRESHOLD = 1,
        CACHE_THRESHOLD,
        TIMEOUT,
        NUM_CHECKPOINT_EVENTS = TIMEOUT
    };

    CheckpointEvent(type_t type) : m_type(type) {}
    ~CheckpointEvent() {}

    type_t getType() const { return m_type; }
    SubsecondTime getTime() const { return m_time; }

private:
    type_t m_type;
    SubsecondTime m_time;
};

#endif /* CHECKPOINT_EVENT_H */