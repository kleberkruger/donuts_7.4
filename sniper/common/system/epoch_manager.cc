#include "epoch_manager.h"
#include "hooks_manager.h"
#include "core_manager.h"
#include "cache_cntlr.h"
#include "shmem_perf_model.h"
#include "simulator.h"
#include "subsecond_time.h"
#include "config.hpp"
#include "stats.h"

const char *CheckpointEventString(CheckpointEvent::checkpoint_event_t event)
{
   switch (event)
   {
   case CheckpointEvent::CACHE_SET_THRESHOLD:
      return "SET";
   case CheckpointEvent::CACHE_THRESHOLD:
      return "CACHE";
   case CheckpointEvent::TIMEOUT:
      return "TIMEOUT";
   default:
      return "?";
   }
}

EpochManager::EpochManager()
    : m_system_eid(0),
      m_persisted_eid(0),
      m_timeout(SubsecondTime::NS(Sim()->getCfg()->hasKey("donuts/timeout")
                                      ? Sim()->getCfg()->getInt("donuts/timeout")
                                      : DEFAULT_TIMEOUT)),
      m_last_commit(SubsecondTime::NS(0))
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
   SubsecondTime now = Sim()->getCoreManager()->getCurrentCore()->getShmemPerfModel()->getElapsedTime(ShmemPerfModel::_SIM_THREAD);
   printf("TIMEOUT | Shmem [%lu] | Global [%lu]\n", now.getNS(), Sim()->getClockSkewMinimizationServer()->getGlobalTime().getNS());

   // if ((now - m_last_commit) >= m_timeout)
   // {
   //    printf("TIMEOUT | now = %lu | last = %lu\n", now.getNS(), m_last_commit.getNS());
   // }

   // SubsecondTime time = Sim()->getClockSkewMinimizationServer()->getGlobalTime();
   // printf("TIMEOUT | [%lu]\n", time.getNS());
}

void EpochManager::checkpoint(CheckpointEvent event)
{
   SubsecondTime now = Sim()->getCoreManager()->getCurrentCore()->getShmemPerfModel()->getElapsedTime(ShmemPerfModel::_SIM_THREAD);
   fprintf(m_log_file, "%lu\n", now.getNS());
   m_last_commit = now;

   // printf("Checkpoint by (%s) | Shmem [%lu] | Global [%lu]...\n", CheckpointEventString(event),
   //        now.getNS(), Sim()->getClockSkewMinimizationServer()->getGlobalTime().getNS());

   m_system_eid++;
}

void EpochManager::globalCheckpoint(CheckpointEvent event)
{
   return Sim()->getEpochManager()->checkpoint(event);
}

UInt64 EpochManager::getGlobalSystemEID()
{
   return Sim()->getEpochManager()->getSystemEID();
}
