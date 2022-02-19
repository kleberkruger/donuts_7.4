#!/usr/bin/env python3

import os, sniper_lib
import pandas as pd


class ExecutionData:
  def __init__(self, exec_time, num_mem_access, mem_bandwidth_utilization, num_mem_writes):
    self.exec_time = exec_time
    self.num_mem_access = num_mem_access
    self.num_mem_writes = num_mem_writes
    self.mem_bandwidth_utilization = mem_bandwidth_utilization

  def __str__(self):
    return '[ ExecTime: {}, NumMemAccess: {}, NumMemWrites: {}, NumMemLogs: {} ]'.format(self.exec_time, self.num_mem_access, self.num_mem_writes)
    

class App:
  def __init__(self, name, baseline, donuts_50, donuts_75, donuts_100):
    self.name = name
    self.baseline = baseline
    self.donuts_50 = donuts_50
    self.donuts_75 = donuts_75
    self.donuts_100 = donuts_100
  
  def __str__(self):
    return 'Name: {}\tBaseline: {}\tPiCL: {}'.format(self.name, self.baseline, self.donuts_50, self.donuts_75, self.donuts_100)


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
  return int(results['performance_model.cycle_count_fixed'][0])


def get_num_mem_access(res):
  results = res['results']
  return list(map(sum, list(zip(results['dram.reads'], results['dram.writes']))))[0]


def get_num_mem_writes(res):
  results = res['results']
  return results['dram.writes'][0]


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

  return [100*a/time0 if time0 else float('inf') for a in results['dram-queue.total-time-used']][0]



def get_results_from_resultsdir(name, resultsdir):
  res = sniper_lib.get_results(0, resultsdir, None)
  return ExecutionData(get_exec_time(res), get_num_mem_access(res), get_avg_mem_bandwidth_utilization(res), 
                       get_num_mem_writes(res))


def get_exec_time_dataframe(apps):
  exec_time_df = pd.DataFrame({
    'Baseline': [ a.baseline.exec_time for a in apps ],
    'Donuts 50%': [ a.donuts_50.exec_time for a in apps ],
    'Overhead 50%': [ 0 for a in apps ],
    'Donuts 75%': [ a.donuts_75.exec_time for a in apps ],
    'Overhead 75%': [ 0 for a in apps ],
    'Donuts 100%': [ a.donuts_100.exec_time for a in apps ],
    'Overhead 100%': [ 0 for a in apps ]
  }, index = [ a.name for a in apps ])

  exec_time_df = exec_time_df.reindex(columns=['Baseline', 
                                               'Donuts 50%', 'Overhead 50%', 
                                               'Donuts 75%', 'Overhead 75%', 
                                               'Donuts 100%', 'Overhead 100%'
                                              ])
  return pd.concat({"Execution Time": exec_time_df}, axis=1)


def get_mem_access_dataframe(apps):
  mem_access_df = pd.DataFrame({
    'Baseline': [ a.baseline.num_mem_access for a in apps ],
    'Donuts 50%': [ a.donuts_50.num_mem_access for a in apps ],
    'Overhead 50%': [ 0 for a in apps ],
    'Donuts 75%': [ a.donuts_75.num_mem_access for a in apps ],
    'Overhead 75%': [ 0 for a in apps ],
    'Donuts 100%': [ a.donuts_100.num_mem_access for a in apps ],
    'Overhead 100%': [ 0 for a in apps ]
  }, index = [ a.name for a in apps ])

  mem_access_df = mem_access_df.reindex(columns=['Baseline', 
                                                 'Donuts 50%', 'Overhead 50%', 
                                                 'Donuts 75%', 'Overhead 75%', 
                                                 'Donuts 100%', 'Overhead 100%'
                                                ])
  return pd.concat({"Memory Access": mem_access_df}, axis=1)


def get_mem_bandwidth_utilization_dataframe(apps):
  mem_bandwidth_utilization_df = pd.DataFrame({
    'Baseline': [ a.baseline.mem_bandwidth_utilization / 100.0 for a in apps ],
    'Donuts 50%': [ a.donuts_50.mem_bandwidth_utilization / 100.0 for a in apps ],
    'Delta 50%': [ 0 for a in apps ],
    'Donuts 75%': [ a.donuts_75.mem_bandwidth_utilization / 100.0 for a in apps ],
    'Delta 75%': [ 0 for a in apps ],
    'Donuts 100%': [ a.donuts_100.mem_bandwidth_utilization / 100.0 for a in apps ],
    'Delta 100%': [ 0 for a in apps ]
  }, index = [ a.name for a in apps ])

  mem_bandwidth_utilization_df = mem_bandwidth_utilization_df.reindex(columns=['Baseline', 
                                                                               'Donuts 50%', 'Delta 50%', 
                                                                               'Donuts 75%', 'Delta 75%', 
                                                                               'Donuts 100%', 'Delta 100%'
                                                                              ])
  return pd.concat({"Average DRAM Bandwidth Utilization": mem_bandwidth_utilization_df}, axis=1)


def get_mem_writes_dataframe(apps):
  mem_writes_df = pd.DataFrame({
    'Baseline': [ a.baseline.num_mem_writes for a in apps ],
    'Donuts 50%': [ a.donuts_50.num_mem_writes for a in apps ],
    'Overhead 50%': [ 0 for a in apps ],
    'Donuts 75%': [ a.donuts_75.num_mem_writes for a in apps ],
    'Overhead 75%': [ 0 for a in apps ],
    'Donuts 100%': [ a.donuts_100.num_mem_writes for a in apps ],
    'Overhead 100%': [ 0 for a in apps ]
  }, index = [ a.name for a in apps ])

  mem_writes_df = mem_writes_df.reindex(columns=['Baseline', 
                                                 'Donuts 50%', 'Delta 50%', 
                                                 'Donuts 75%', 'Delta 75%', 
                                                 'Donuts 100%', 'Delta 100%'
                                                 ])
  return pd.concat({"Memory Writes": mem_writes_df}, axis=1)


def generate_results_dataframe(resultsrootdir):
  apps = []
  for app_dir in os.listdir(resultsrootdir):
    try:
      if os.path.isdir(app_dir):
        app = App(app_dir, 
          get_results_from_resultsdir(app_dir, app_dir + '/gainestown'), 
          get_results_from_resultsdir(app_dir, app_dir + '/kruger/0.5'), 
          get_results_from_resultsdir(app_dir, app_dir + '/kruger/0.75'), 
          get_results_from_resultsdir(app_dir, app_dir + '/kruger/1.0'))
        apps.append(app)
    except:
      print(('An exception occurred in application: {}'.format(app_dir)))

  df = pd.concat([get_exec_time_dataframe(apps), get_mem_access_dataframe(apps), 
    get_mem_bandwidth_utilization_dataframe(apps), get_mem_writes_dataframe(apps)], 
    axis=1, names=['Application'])
  
  # df.index.name = 'Application'
  return df.sort_index()


def generate_sheet(df, output):
  with pd.ExcelWriter('{}/results_cpu2006_donuts.xlsx'.format(output), engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name='SPEC CPU2006')

    startrow, rowssize = 4, df.shape[0]
    worksheet = writer.sheets['SPEC CPU2006']
    # for r in range(startrow, rowssize + startrow):
    #   worksheet.write_formula('D{}'.format(r), '(C{}-B{})/B{}'.format(r, r, r))
    #   worksheet.write_formula('G{}'.format(r), '(F{}-E{})/E{}'.format(r, r, r))
    #   worksheet.write_formula('J{}'.format(r), 'I{}-H{}'.format(r, r))
      # worksheet.write_formula('O{}'.format(r), 'M{}/L{}'.format(r, r))
      # worksheet.write_formula('P{}'.format(r), 'L{}/(L{}-K{})'.format(r, r, r))


def generate_results_cpu2006(resultsrootdir = '.', output = '.', silent = False):
  df = generate_results_dataframe(resultsrootdir)
  if (not silent): 
    print(df)
  generate_sheet(df, output)


if __name__ == '__main__': 
  generate_results_cpu2006()
