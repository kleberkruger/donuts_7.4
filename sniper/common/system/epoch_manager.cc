#include "epoch_manager.h"
#include "hooks_manager.h"
#include "simulator.h"
#include "subsecond_time.h"
#include "stats.h"

EpochManager::EpochManager() : m_system_eid(0), m_persisted_eid(0)
{
   Sim()->getHooksManager()->registerHook(HookType::HOOK_APPLICATION_START, __start, (UInt64)this);
   Sim()->getHooksManager()->registerHook(HookType::HOOK_APPLICATION_EXIT, __exit, (UInt64)this);
   // Sim()->getHooksManager()->registerHook(HookType::HOOK_PERIODIC, __timeout, (UInt64)this);

   registerStatsMetric("epoch", 0, "system_eid", &m_system_eid);
   registerStatsMetric("epoch", 0, "persisted_eid", &m_persisted_eid);
}

EpochManager::~EpochManager() {}

void EpochManager::start()
{
   String path = Sim()->getConfig()->getOutputDirectory() + "/checkpoints.csv";
   if ((m_log_file = fopen(path.c_str(), "w")) == NULL)
      fprintf(stderr, "Error on creating checkpoints.csv.\n");

   m_system_eid++;
   printf("STARTING EPOCH MANAGER %lu\n", m_system_eid);
}

void EpochManager::exit()
{
   fclose(m_log_file);
}

void EpochManager::timeout()
{
   // Descobrir se precisa ser feito checkpoint ou se o último commit foi feito dentro do intervalo...
   
   // SubsecondTime time = Sim()->getClockSkewMinimizationServer()->getGlobalTime();
   // printf("TIMEOUT | [%lu]\n", time.getNS());
}

void EpochManager::checkpoint(SubsecondTime now, std::queue<CacheBlockInfo *> dirty_blocks)
{
   fprintf(m_log_file, "%lu\n", now.getNS());
   m_last_commit = now;

   printf("Checkpointing... [%lu] = [%lu]\n", now.getNS(), Sim()->getClockSkewMinimizationServer()->getGlobalTime().getNS());

   // persisting data...
   m_system_eid++;
}

void EpochManager::globalCheckpoint(SubsecondTime now, std::queue<CacheBlockInfo *> dirty_blocks)
{
   return Sim()->getEpochManager()->checkpoint(now, dirty_blocks);
}

UInt64 EpochManager::getGlobalSystemEID()
{
   return Sim()->getEpochManager()->getSystemEID();
}
