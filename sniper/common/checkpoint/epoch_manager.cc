#include "epoch_manager.h"
#include "hooks_manager.h"
#include "checkpoint_event.h"
#include "simulator.h"
#include "stats.h"

EpochManager::EpochManager() : m_log_file(NULL), m_system_eid(0)
{
   Sim()->getHooksManager()->registerHook(HookType::HOOK_APPLICATION_START, __start, (UInt64)this);
   Sim()->getHooksManager()->registerHook(HookType::HOOK_APPLICATION_EXIT, __exit, (UInt64)this);

   registerStatsMetric("epoch", 0, "system_eid", &m_system_eid);
   registerStatsMetric("epoch", 0, "persisted_eid", &m_persisted.eid);
}

EpochManager::~EpochManager() {}

void EpochManager::start()
{
   String path = Sim()->getConfig()->getOutputDirectory() + "/sim.ckpts.csv";
   if ((m_log_file = fopen(path.c_str(), "w")) == NULL)
      fprintf(stderr, "Error on creating sim.ckpts.csv\n");

   m_system_eid++;
}

void EpochManager::exit()
{
   fclose(m_log_file);
}

void EpochManager::commitCheckpoint(const CheckpointEvent &ckpt)
{
   printf("Checkpoint by %s for Epoch %lu at time %lu | Logs: %lu, Full: %.2f%%\n", CheckpointEvent::TypeString(ckpt.getType()),
          ckpt.getEpochID(), ckpt.getTime().getNS(), ckpt.getNumLogs(), ckpt.getCacheStocking());
   
   fprintf(m_log_file, "%lu\n", ckpt.getTime().getNS());

   m_commited.eid = ckpt.getEpochID();
   m_commited.time = ckpt.getTime();
   m_system_eid++;
}

void EpochManager::registerPersistedEID(const UInt64 eid, const SubsecondTime &time)
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
