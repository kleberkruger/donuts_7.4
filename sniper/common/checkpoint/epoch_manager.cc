#include "epoch_manager.h"
#include "hooks_manager.h"
#include "checkpoint_event.h"
#include "simulator.h"
#include "stats.h"

EpochManager::EpochManager() : m_log_file(nullptr), m_system_eid(0)
{
   Sim()->getHooksManager()->registerHook(HookType::HOOK_APPLICATION_START, _start, (UInt64)this);
   Sim()->getHooksManager()->registerHook(HookType::HOOK_APPLICATION_EXIT, _exit, (UInt64)this);

   registerStatsMetric("epoch", 0, "system_eid", &m_system_eid);
   registerStatsMetric("epoch", 0, "persisted_eid", &m_persisted.eid);
}

EpochManager::~EpochManager() = default;

void EpochManager::start()
{
   String path = Sim()->getConfig()->getOutputDirectory() + "/sim.ckpts.csv";
   if ((m_log_file = fopen(path.c_str(), "w")) == nullptr)
      fprintf(stderr, "Error on creating sim.ckpts.csv\n");

   m_system_eid++;
}

void EpochManager::exit()
{
   fclose(m_log_file);
}

void EpochManager::commitCheckpoint(const CheckpointEvent &checkpoint_event)
{
//   printf("Checkpoint by %s for Epoch %lu at time %lu | Logs: %lu, Full: %.2f%%\n", CheckpointEvent::TypeString(checkpoint_event.getType()),
//          checkpoint_event.getEpochID(), checkpoint_event.getTime().getNS(), checkpoint_event.getNumLogs(), checkpoint_event.getCacheStocking());
   
   fprintf(m_log_file, "%lu\n", checkpoint_event.getTime().getNS());

   m_commited.eid = checkpoint_event.getEpochID();
   m_commited.time = checkpoint_event.getTime();
   m_system_eid++;
}

void EpochManager::registerPersistedEID(UInt64 eid, const SubsecondTime &time)
{
   m_persisted.eid = eid;
   m_persisted.time = time;
}

EpochManager *EpochManager::getInstance()
{
   return Sim()->getEpochManager();
}

UInt64 EpochManager::getGlobalSystemEID()
{
   return Sim()->getEpochManager()->getSystemEID();
}
