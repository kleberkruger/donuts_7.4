#include "epoch_manager.h"
#include "hooks_manager.h"
#include "simulator.h"
#include "subsecond_time.h"
#include "stats.h"

#include "core_manager.h"
#include "shmem_perf_model.h"

EpochManager::EpochManager() : m_system_eid(0), m_persisted_eid(0)
{
   Sim()->getHooksManager()->registerHook(HookType::HOOK_APPLICATION_START, __start, (UInt64)this);
   Sim()->getHooksManager()->registerHook(HookType::HOOK_APPLICATION_EXIT, __exit, (UInt64)this);
   Sim()->getHooksManager()->registerHook(HookType::HOOK_PERIODIC, __timeout, (UInt64)this);

   registerStatsMetric("epoch", 0, "system_eid", &m_system_eid);
   registerStatsMetric("epoch", 0, "persisted_eid", &m_persisted_eid);
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

void EpochManager::timeout()
{
   // Descobrir se precisa ser feito checkpoint ou se o último commit foi feito dentro do intervalo...

   // SubsecondTime time = Sim()->getClockSkewMinimizationServer()->getGlobalTime();
   // printf("TIMEOUT | [%lu]\n", time.getNS());
}

void EpochManager::checkpoint(std::queue<CacheBlockInfo *> dirty_blocks)
{
   SubsecondTime now = Sim()->getCoreManager()->getCurrentCore()->getShmemPerfModel()->getElapsedTime(ShmemPerfModel::_SIM_THREAD);
   fprintf(m_log_file, "%lu\n", now.getNS());
   m_last_commit = now;

   printf("Checkpointing in time: [%lu]...\n", now.getNS());

   // persisting data...
   m_system_eid++;
}

void EpochManager::globalCheckpoint(std::queue<CacheBlockInfo *> dirty_blocks)
{
   return Sim()->getEpochManager()->checkpoint(dirty_blocks);
}

UInt64 EpochManager::getGlobalSystemEID()
{
   return Sim()->getEpochManager()->getSystemEID();
}
