#include "simulator.h"
#include "nvm_perf_model.h"
#include "nvm_perf_model_constant.h"
#include "config.hpp"

NvmPerfModel* NvmPerfModel::createNvmPerfModel(core_id_t core_id, UInt32 cache_block_size)
{
   String type = Sim()->getCfg()->getString("perf_model/nvm/type");

   if (type == "constant")
   {
      return new NvmPerfModelConstant(core_id, cache_block_size);
   }
   else
   {
      LOG_PRINT_ERROR("Invalid NVM model type %s", type.c_str());
   }
}