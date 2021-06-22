#include "epoch_manager.h"
#include "hooks_manager.h"
#include "simulator.h"
#include "stats.h"
#include "checkpoint_info.h"

EpochManager::EpochManager() : m_system_eid(0), m_last_checkpoint(CheckpointInfo::TIMEOUT, 0, 0.0, 0, SubsecondTime::NS())
{
   Sim()->getHooksManager()->registerHook(HookType::HOOK_APPLICATION_START, __start, (UInt64)this);
   Sim()->getHooksManager()->registerHook(HookType::HOOK_APPLICATION_EXIT, __exit, (UInt64)this);

   registerStatsMetric("epoch", 0, "system_eid", &m_system_eid);
   // registerStatsMetric("epoch", 0, "persisted_eid", &m_last_checkpoint.getEpochID());
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

void EpochManager::registerCheckpoint(const CheckpointInfo &ckpt)
{
   fprintf(m_log_file, "%lu\n", ckpt.getTime().getNS());
   m_last_checkpoint = ckpt;
   m_system_eid++;
}

EpochManager *EpochManager::getInstance()
{
   return Sim()->getEpochManager();
}

UInt64 EpochManager::getGlobalSystemEID()
{
   return Sim()->getEpochManager()->getSystemEID();
}
