#!/usr/bin/env python

import os, sniper_lib
import pandas as pd


class ExecutionData:
  def __init__(self, exec_time, num_mem_access, mem_bandwidth_utilization, num_mem_writes, num_checkpoints = 0, num_mem_logs = 0, num_buffer_overflow = 0):
    self.exec_time = exec_time
    self.num_mem_access = num_mem_access
    self.num_mem_writes = num_mem_writes
    self.mem_bandwidth_utilization = mem_bandwidth_utilization
    self.num_checkpoints = num_checkpoints
    self.num_mem_logs = num_mem_logs
    self.num_buffer_overflow = num_buffer_overflow

  def __str__(self):
    return '[ ExecTime: {}, NumMemAccess: {}, NumMemWrites: {}, NumMemLogs: {} ]'.format(self.exec_time, self.num_mem_access, self.num_mem_writes, self.num_mem_logs)
    

class App:
  def __init__(self, name, baseline, picl, donuts):
    self.name = name
    self.baseline = baseline
    self.picl = picl
    self.donuts = donuts
  
  def __str__(self):
    return 'Name: {}\tBaseline: {}\tPiCL: {}\tDonuts: {}\n'.format(self.name, self.baseline, self.picl, self.donuts)


def get_exec_time(res):
  results = res['results']
  config = res['config']
  ncores = int(config['general/total_cores'])
  
  if 'barrier.global_time_begin' in results:
    time0_begin = results['barrier.global_time_begin']
    time0_end = results['barrier.global_time_end']
  
  if 'barrier.global_time' in results:
    time0 = results['barrier.global_time'][0]
  else:
    time0 = time0_begin - time0_end

  results['performance_model.elapsed_time_fixed'] = [
    time0
    for c in range(ncores)
  ]
  results['performance_model.cycle_count_fixed'] = [
    results['performance_model.elapsed_time_fixed'][c] * results['fs_to_cycles_cores'][c]
    for c in range(ncores)
  ]
  return long(results['performance_model.cycle_count_fixed'][0])


def get_num_mem_access(res):
  results = res['results']
  return map(sum, zip(results['dram.reads'], results['dram.writes']))[0]


def get_num_mem_writes(res):
  results = res['results']
  return results['dram.writes'][0]


def get_num_mem_checkpoints(res):
  results = res['results']
  return map(sum, zip(results['epoch'], results['system_eid']))[0]


def get_num_mem_logs(res):
  results = res['results']
  return results['onchip_undo_buffer.log_writes'][0]


def get_num_buffer_overflow(res):
  results = res['results']
  return results['onchip_undo_buffer.overflow'][0]


def get_avg_mem_bandwidth_utilization(res):
  results = res['results']
  config = res['config']
  ncores = int(config['general/total_cores'])
  
  if 'barrier.global_time_begin' in results:
    time0_begin = results['barrier.global_time_begin']
    time0_end = results['barrier.global_time_end']
  
  if 'barrier.global_time' in results:
    time0 = results['barrier.global_time'][0]
  else:
    time0 = time0_begin - time0_end

  return map(lambda a: 100*a/time0 if time0 else float('inf'), results['dram-queue.total-time-used'])[0]



def get_results_from_resultsdir(name, resultsdir):
  res = sniper_lib.get_results(0, resultsdir, None)
  return ExecutionData(get_exec_time(res), 
                       get_num_mem_access(res), 
                       get_avg_mem_bandwidth_utilization(res), 
                       get_num_mem_writes(res))


def get_exec_time_dataframe(apps):
  exec_time_df = pd.DataFrame({
    'Baseline': [ a.baseline.exec_time for a in apps ],
    'PiCL': [ a.picl.exec_time for a in apps ],
    'Donuts': [ a.donuts.exec_time for a in apps ],
    'Overhead PiCL': [ 0 for a in apps ],
    'Overhead Donuts': [ 0 for a in apps ]
  }, index = [ a.name for a in apps ])

  exec_time_df = exec_time_df.reindex(columns=['Baseline', 'PiCL', 'Donuts', 'Overhead PiCL', 'Overhead Donuts'])
  return pd.concat({"Execution Time": exec_time_df}, axis=1)


def get_mem_access_dataframe(apps):
  mem_access_df = pd.DataFrame({
    'Baseline': [ a.baseline.num_mem_access for a in apps ],
    'PiCL': [ a.picl.num_mem_access for a in apps ],
    'Donuts': [ a.donuts.num_mem_access for a in apps ],
    'Overhead PiCL': [ 0 for a in apps ],
    'Overhead Donuts': [ 0 for a in apps ]
  }, index = [ a.name for a in apps ])

  mem_access_df = mem_access_df.reindex(columns=['Baseline', 'PiCL', 'Donuts', 'Overhead PiCL', 'Overhead Donuts'])
  return pd.concat({"Memory Access": mem_access_df}, axis=1)


def get_mem_bandwidth_utilization_dataframe(apps):
  mem_bandwidth_utilization_df = pd.DataFrame({
    'Baseline': [ a.baseline.mem_bandwidth_utilization / 100.0 for a in apps ],
    'PiCL': [ a.picl.mem_bandwidth_utilization / 100.0 for a in apps ],
    'Donuts': [ a.donuts.mem_bandwidth_utilization / 100.0 for a in apps ],
    'Delta PiCL': [ 0 for a in apps ],
    'Delta Donuts': [ 0 for a in apps ]
  }, index = [ a.name for a in apps ])

  mem_bandwidth_utilization_df = mem_bandwidth_utilization_df.reindex(columns=[
    'Baseline', 'PiCL', 'Donuts', 'Delta PiCL', 'Delta Donuts'])
  return pd.concat({"Average DRAM Bandwidth Utilization": mem_bandwidth_utilization_df}, axis=1)


def get_mem_writes_dataframe(apps):
  mem_writes_df = pd.DataFrame({
    'Baseline': [ a.baseline.num_mem_writes for a in apps ],
    'PiCL': [ a.picl.num_mem_writes for a in apps ],
    'Donuts': [ a.donuts.num_mem_writes for a in apps ],
    # 'Logging': [ a.picl.num_mem_logs for a in apps ],
    # 'Buffer Overflow': [ a.picl.num_buffer_overflow for a in apps ],
    # '%% Logging': [ 0 for a in apps ],
    'Overhead PiCL': [ 0 for a in apps ],
    'Overhead Donuts': [ 0 for a in apps ]
  }, index = [ a.name for a in apps ])

  # mem_writes_df = mem_writes_df.reindex(columns=['Baseline', 'Donuts', 'Logging', 'Buffer Overflow', '% Logging', 'Overhead'])
  mem_writes_df = mem_writes_df.reindex(columns=['Baseline', 'PiCL', 'Donuts', 'Overhead PiCL', 'Overhead Donuts'])
  return pd.concat({"Memory Writes": mem_writes_df}, axis=1)


def get_checkpoints_dataframe(apps):
  checkpoints_df = pd.DataFrame({
    # 'PiCL': [ a.picl.num_checkpoints for a in apps ],
    'Donuts': [ a.donuts.num_checkpoints for a in apps ],
  }, index = [ a.name for a in apps ])
  # checkpoints_df = checkpoints_df.reindex(columns=['PiCL', 'Donuts'])
  return pd.concat({"Checkpoints": checkpoints_df}, axis=1)


def generate_results_dataframe(resultsrootdir):
  apps = []
  for app_dir in os.listdir(resultsrootdir):
    try:
      if os.path.isdir(app_dir) and app_dir != 'cpu2006':
        app = App(app_dir, get_results_from_resultsdir(app_dir, app_dir + '/base'), 
                           get_results_from_resultsdir(app_dir, app_dir + '/picl'),
                           get_results_from_resultsdir(app_dir, app_dir + '/donuts/1.0'))
        apps.append(app)
    except:
      print('An exception occurred in application: {}'.format(app_dir))

  df = pd.concat([get_exec_time_dataframe(apps), 
                  get_mem_access_dataframe(apps), 
                  get_mem_bandwidth_utilization_dataframe(apps), 
                  get_mem_writes_dataframe(apps), 
                  get_checkpoints_dataframe(apps)],
    axis=1, names=['Application'])
  
  # df.index.name = 'Application'
  return df.sort_index()


def generate_sheet(df, output):
  with pd.ExcelWriter('{}/results_cpu2006.xlsx'.format(output), engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name='SPEC CPU2006')

    # startrow, rowssize = 4, df.shape[0]
    # worksheet = writer.sheets['SPEC CPU2006']
    # for r in range(startrow, rowssize + startrow):
    #   worksheet.write_formula('D{}'.format(r), '(C{}-B{})/B{}'.format(r, r, r))
    #   worksheet.write_formula('G{}'.format(r), '(F{}-E{})/E{}'.format(r, r, r))
    #   worksheet.write_formula('J{}'.format(r), 'I{}-H{}'.format(r, r))
    #   worksheet.write_formula('O{}'.format(r), 'M{}/L{}'.format(r, r))
    #   worksheet.write_formula('P{}'.format(r), 'L{}/(L{}-K{})'.format(r, r, r))


def generate_results_cpu2006(resultsrootdir = '.', output = '.', silent = False):
  df = generate_results_dataframe(resultsrootdir)
  if (not silent): 
    print(df)
  generate_sheet(df, output)


if __name__ == '__main__': 
  generate_results_cpu2006()





# Implementation by classes...

# class ResultsReader:
#   def __init__(self, resultsdir) -> None:
#     res = sniper_lib.get_results(0, resultsdir, None)
#     self.results = res['results']
#     self.config = res['config']
#     self.ncores = int(self.config['general/total_cores'])


#   @classmethod
#   def get_execution_time(self):
#     if 'barrier.global_time_begin' in self.results:
#       time0_begin = self.results['barrier.global_time_begin']
#       time0_end = self.results['barrier.global_time_end']

#     time0 = self.results['barrier.global_time'][0] if 'barrier.global_time' in self.results else time0_begin - time0_end
    
#     self.results['performance_model.elapsed_time_fixed'] = [ time0 for c in range(self.ncores)]
#     self.results['performance_model.cycle_count_fixed'] = [
#       self.results['performance_model.elapsed_time_fixed'][c] * self.results['fs_to_cycles_cores'][c]
#       for c in range(self.ncores)
#     ]
#     return long(self.results['performance_model.cycle_count_fixed'][0])

  
#   @classmethod
#   def get_memory_access(self):
#     return map(sum, zip(self.results['dram.reads'], self.results['dram.writes']))[0]


#   @classmethod
#   def get_memory_writes(self):
#     return self.results['dram.writes'][0]


#   @classmethod
#   def get_memory_logs(self):
#     return self.results['onchip_undo_buffer.log_writes'][0]


#   @classmethod
#   def get_attributes(self):
#     return ExecutionData(self.get_exec_time(), self.get_memory_access(), self.get_memory_writes(), self.get_memory_logs())


# class ResultGenerator:
#   def __init__(self, root_dir = '.', output_dir = '.', silent = False):
#     self.root_dir = root_dir
#     self.output_dir = output_dir
#     self.silent = silent
#     self.apps = []

#   @classmethod
#   def start(self):
#     for app_dir in os.listdir(self.root_dir):
#       try:
#         if os.path.isdir(app_dir):
#           app = App(app_dir, ResultsReader('{}/base'.format(app_dir)).get_attributes(), ResultsReader('{}/pikl'.format(app_dir)).get_attributes())
#           self.apps.append(app)
#       except:
#         print('An exception occurred in application: {}'.format(app_dir))
#