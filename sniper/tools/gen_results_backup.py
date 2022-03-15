#!/usr/bin/env python3

import os, subprocess, argparse, json
import pandas as pd


class ExecutionData:
  def __init__(self, exec_time, mem_bandwidth_usage, num_mem_access, num_mem_writes,
               num_mem_logs = 0, num_buffer_overflow = 0, num_checkpoints = 0):
    self.exec_time = exec_time
    self.mem_bandwidth_usage = mem_bandwidth_usage
    self.num_mem_access = num_mem_access
    self.num_mem_writes = num_mem_writes
    self.num_mem_logs = num_mem_logs
    self.num_buffer_overflow = num_buffer_overflow
    self.num_checkpoints = num_checkpoints

  def __str__(self):
    return f"[ ExecTime: {self.exec_time}, MemBandwidthUsage: {self.mem_bandwidth_usage} NumMemAccess: {self.num_mem_access}, NumMemWrites: {self.num_mem_writes}, NumMemLogs: {self.num_mem_logs} NumBufferOverflow: {self.num_buffer_overflow}, NumCheckpoints: {self.num_checkpoints}]"


class App:
  def __init__(self, name, baseline, picl, donuts_1k, donuts_2k, donuts_4k, donuts_8k, donuts_16k):
    self.name = name
    self.baseline = baseline
    self.picl = picl
    self.donuts_1k = donuts_1k
    self.donuts_2k = donuts_2k
    self.donuts_4k = donuts_4k
    self.donuts_8k = donuts_8k
    self.donuts_16k = donuts_16k
  
  def __str__(self):
    return f"Name: {self.name}\tBaseline: {self.baseline}\tPiCL: {self.picl}\t\
      Donuts 1K: {self.donuts_1k}\tDonuts 4K: {self.donuts_4k}\tDonuts 8K: {self.donuts_8k}\n"


def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-c', '--config', type=str, nargs='+', default=['all'], help='configutarions')
	parser.add_argument('-a', '--apps', type=str, nargs='+', default=['all'], help='applications to running')
	parser.add_argument('-o', '--out', '--output', type=str, default='out/cpu2006', help='output base path')
	parser.add_argument('-r', '--result', type=str, default=['.'], help='result file')
	return parser.parse_args()


def get_execution_data(path):
  data = json.loads(subprocess.check_output(["./get_exec_data.py", path], universal_newlines=True))
  return ExecutionData(data['exec_time'], data['mem_bandwidth_usage'], 
                       data['num_mem_access'], data['num_mem_writes'], data['num_mem_logs'], 
                       data['num_buffer_overflow'], data['num_checkpoints'])


def get_exec_time_dataframe(apps):
  exec_time_df = pd.DataFrame({
    'Baseline': [ a.baseline.exec_time for a in apps ],
    'PiCL': [ a.picl.exec_time for a in apps ],
    'Donuts-1k': [ a.donuts_1k.exec_time for a in apps ],
    'Donuts-2k': [ a.donuts_2k.exec_time for a in apps ],
    'Donuts-4k': [ a.donuts_4k.exec_time for a in apps ],
    'Donuts-8k': [ a.donuts_8k.exec_time for a in apps ],
    'Donuts-16k': [ a.donuts_16k.exec_time for a in apps ],
    'Overhead PiCL': [ 0 for a in apps ],
    'Overhead Donuts-1k': [ 0 for a in apps ],
    'Overhead Donuts-2k': [ 0 for a in apps ],
    'Overhead Donuts-4k': [ 0 for a in apps ],
    'Overhead Donuts-8k': [ 0 for a in apps ],
    'Overhead Donuts-16k': [ 0 for a in apps ]
  }, index = [ a.name for a in apps ])

  exec_time_df = exec_time_df.reindex(columns=['Baseline', 'PiCL', 'Donuts-1k', 'Donuts-2k', 'Donuts-4k', 'Donuts-8k', 'Donuts-16k', 'Overhead PiCL', 'Overhead Donuts-1k', 'Overhead Donuts-2k', 'Overhead Donuts-4k', 'Overhead Donuts-8k', 'Overhead Donuts-16k'])
  return pd.concat({"Execution Time": exec_time_df}, axis=1)


def get_mem_access_dataframe(apps):
  mem_access_df = pd.DataFrame({
    'Baseline': [ a.baseline.num_mem_access for a in apps ],
    'PiCL': [ a.picl.num_mem_access for a in apps ],
    'Donuts-1k': [ a.donuts_1k.num_mem_access for a in apps ],
    'Donuts-2k': [ a.donuts_2k.num_mem_access for a in apps ],
    'Donuts-4k': [ a.donuts_4k.num_mem_access for a in apps ],
    'Donuts-8k': [ a.donuts_8k.num_mem_access for a in apps ],
    'Donuts-16k': [ a.donuts_16k.num_mem_access for a in apps ],
    'Overhead PiCL': [ 0 for a in apps ],
    'Overhead Donuts-1k': [ 0 for a in apps ],
    'Overhead Donuts-2k': [ 0 for a in apps ],
    'Overhead Donuts-4k': [ 0 for a in apps ],
    'Overhead Donuts-8k': [ 0 for a in apps ],
    'Overhead Donuts-16k': [ 0 for a in apps ]
  }, index = [ a.name for a in apps ])

  mem_access_df = mem_access_df.reindex(columns=[
    'Baseline', 'PiCL', 'Donuts-1k', 'Donuts-2k', 'Donuts-4k', 'Donuts-8k', 'Donuts-16k', 
    'Overhead PiCL', 'Overhead Donuts-1k', 'Overhead Donuts-2k', 'Overhead Donuts-4k', 'Overhead Donuts-8k', 'Overhead Donuts-16k'])
  return pd.concat({"Memory Access": mem_access_df}, axis=1)


def get_mem_bandwidth_usage_dataframe(apps):
  mem_bandwidth_usage_df = pd.DataFrame({
    'Baseline': [ a.baseline.mem_bandwidth_usage / 100.0 for a in apps ],
    'PiCL': [ a.picl.mem_bandwidth_usage / 100.0 for a in apps ],
    'Donuts-1k': [ a.donuts_1k.mem_bandwidth_usage / 100.0 for a in apps ],
    'Donuts-2k': [ a.donuts_2k.mem_bandwidth_usage / 100.0 for a in apps ],
    'Donuts-4k': [ a.donuts_4k.mem_bandwidth_usage / 100.0 for a in apps ],
    'Donuts-8k': [ a.donuts_8k.mem_bandwidth_usage / 100.0 for a in apps ],
    'Donuts-16k': [ a.donuts_16k.mem_bandwidth_usage / 100.0 for a in apps ],
    'Delta PiCL': [ 0 for a in apps ],
    'Delta Donuts-1k': [ 0 for a in apps ],
    'Delta Donuts-2k': [ 0 for a in apps ],
    'Delta Donuts-4k': [ 0 for a in apps ],
    'Delta Donuts-8k': [ 0 for a in apps ],
    'Delta Donuts-16k': [ 0 for a in apps ]
  }, index = [ a.name for a in apps ])

  mem_bandwidth_usage_df = mem_bandwidth_usage_df.reindex(columns=[
    'Baseline', 'PiCL', 'Donuts-1k', 'Donuts-2k', 'Donuts-4k', 'Donuts-8k', 'Donuts-16k', 
    'Delta PiCL', 'Delta Donuts-1k', 'Delta Donuts-2k', 'Delta Donuts-4k', 'Delta Donuts-8k', 'Delta Donuts-16k'])
  return pd.concat({"Average DRAM Bandwidth Usage": mem_bandwidth_usage_df}, axis=1)


def get_mem_writes_dataframe(apps):
  mem_writes_df = pd.DataFrame({
    'Baseline': [ a.baseline.num_mem_writes for a in apps ],
    'PiCL': [ a.picl.num_mem_writes for a in apps ],
    'Donuts-1k': [ a.donuts_1k.num_mem_writes for a in apps ],
    'Donuts-2k': [ a.donuts_2k.num_mem_writes for a in apps ],
    'Donuts-4k': [ a.donuts_4k.num_mem_writes for a in apps ],
    'Donuts-8k': [ a.donuts_8k.num_mem_writes for a in apps ],
    'Donuts-16k': [ a.donuts_16k.num_mem_writes for a in apps ],
    # 'Logging': [ a.picl.num_mem_logs for a in apps ],
    # 'Buffer Overflow': [ a.picl.num_buffer_overflow for a in apps ],
    # '%% Logging': [ 0 for a in apps ],
    'Overhead PiCL': [ 0 for a in apps ],
    'Overhead Donuts-1k': [ 0 for a in apps ],
    'Overhead Donuts-2k': [ 0 for a in apps ],
    'Overhead Donuts-4k': [ 0 for a in apps ],
    'Overhead Donuts-8k': [ 0 for a in apps ],
    'Overhead Donuts-16k': [ 0 for a in apps ]
  }, index = [ a.name for a in apps ])

  mem_writes_df = mem_writes_df.reindex(columns=[
    'Baseline', 'PiCL', 'Donuts-1k', 'Donuts-2k', 'Donuts-4k', 'Donuts-8k', 'Donuts-16k', 
    'Overhead PiCL', 'Overhead Donuts-1k', 'Overhead Donuts-2k', 'Overhead Donuts-4k', 'Overhead Donuts-8k', 'Overhead Donuts-16k'])
  return pd.concat({"Memory Writes": mem_writes_df}, axis=1)


def get_checkpoints_dataframe(apps):
  checkpoints_df = pd.DataFrame({
    'PiCL': [ a.picl.num_checkpoints for a in apps ],
    'Donuts-1k': [ a.donuts_1k.num_checkpoints for a in apps ],
    'Donuts-2k': [ a.donuts_2k.num_checkpoints for a in apps ],
    'Donuts-4k': [ a.donuts_4k.num_checkpoints for a in apps ],
    'Donuts-8k': [ a.donuts_8k.num_checkpoints for a in apps ],
    'Donuts-16k': [ a.donuts_16k.num_checkpoints for a in apps ]
  }, index = [ a.name for a in apps ])
  # checkpoints_df = checkpoints_df.reindex(columns=['PiCL', 'Donuts'])
  return pd.concat({"Checkpoints": checkpoints_df}, axis=1)


def generate_results_dataframe(apps):
  df = pd.concat([
    get_exec_time_dataframe(apps),
    get_mem_access_dataframe(apps),
    get_mem_writes_dataframe(apps),
    get_mem_bandwidth_usage_dataframe(apps),
    get_checkpoints_dataframe(apps)
  ], axis=1, names=['Application'])
  
  # df.index.name = 'Application'
  return df.sort_index()


def generate_sheet(df, output):
  with pd.ExcelWriter(f"{output}/results_cpu2006.xlsx", engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name='SPEC CPU2006')

    # startrow, rowssize = 4, df.shape[0]
    # worksheet = writer.sheets['SPEC CPU2006']
    # for r in range(startrow, rowssize + startrow):
    #   worksheet.write_formula('D{}'.format(r), '(C{}-B{})/B{}'.format(r, r, r))
    #   worksheet.write_formula('G{}'.format(r), '(F{}-E{})/E{}'.format(r, r, r))
    #   worksheet.write_formula('J{}'.format(r), 'I{}-H{}'.format(r, r))
    #   worksheet.write_formula('O{}'.format(r), 'M{}/L{}'.format(r, r))
    #   worksheet.write_formula('P{}'.format(r), 'L{}/(L{}-K{})'.format(r, r, r))
  

def main(resultsrootdir = None, output = '.', silent = False):
  args = parse_args()
  if resultsrootdir is None:
    resultsrootdir = f"{os.environ['BENCHMARKS_ROOT']}/out/cpu2006"
  
  apps = []
  for app_name in os.listdir(resultsrootdir):
    app_dir = f"{resultsrootdir}/{app_name}"
    try:
      if os.path.isdir(app_dir) and app_dir != 'cpu2006':
        app = App(app_name, get_execution_data(f"{app_dir}/baseline-nvm"), 
                            get_execution_data(f"{app_dir}/picl"), 
                            get_execution_data(f"{app_dir}/donuts-1k"),
                            get_execution_data(f"{app_dir}/donuts-2k"), 
                            get_execution_data(f"{app_dir}/donuts-4k"),
                            get_execution_data(f"{app_dir}/donuts-8k"),
                            get_execution_data(f"{app_dir}/donuts-16k"))
        apps.append(app)
    except:
      print(f"An exception occurred in application: {app_dir}")

  df = generate_results_dataframe(apps)
  generate_sheet(df, '.')
  
  





def get_exec_time_dataframe_2(apps):
  exec_time_df = pd.DataFrame({
    'Donuts-50': [ a.donuts_50.exec_time for a in apps ],
    'Donuts-63': [ a.donuts_63.exec_time for a in apps ],
    'Donuts-75': [ a.donuts_75.exec_time for a in apps ],
    'Donuts-88': [ a.donuts_88.exec_time for a in apps ],
    'Donuts-100': [ a.donuts_100.exec_time for a in apps ],
  }, index = [ a.name for a in apps ])
  return pd.concat({"Execution Time": exec_time_df}, axis=1)


def get_mem_access_dataframe_2(apps):
  mem_access_df = pd.DataFrame({
    'Donuts-50': [ a.donuts_50.num_mem_access for a in apps ],
    'Donuts-63': [ a.donuts_63.num_mem_access for a in apps ],
    'Donuts-75': [ a.donuts_75.num_mem_access for a in apps ],
    'Donuts-88': [ a.donuts_88.num_mem_access for a in apps ],
    'Donuts-100': [ a.donuts_100.num_mem_access for a in apps ],
  }, index = [ a.name for a in apps ])
  return pd.concat({"Memory Access": mem_access_df}, axis=1)


def get_mem_bandwidth_usage_dataframe_2(apps):
  mem_bandwidth_usage_df = pd.DataFrame({
    'Donuts-50': [ a.donuts_50.mem_bandwidth_usage / 100.0 for a in apps ],
    'Donuts-63': [ a.donuts_63.mem_bandwidth_usage / 100.0 for a in apps ],
    'Donuts-75': [ a.donuts_75.mem_bandwidth_usage / 100.0 for a in apps ],
    'Donuts-88': [ a.donuts_88.mem_bandwidth_usage / 100.0 for a in apps ],
    'Donuts-100': [ a.donuts_100.mem_bandwidth_usage / 100.0 for a in apps ],
  }, index = [ a.name for a in apps ])
  return pd.concat({"Average DRAM Bandwidth Usage": mem_bandwidth_usage_df}, axis=1)


def get_mem_writes_dataframe_2(apps):
  mem_writes_df = pd.DataFrame({
    'Donuts-50': [ a.donuts_50.num_mem_writes for a in apps ],
    'Donuts-63': [ a.donuts_63.num_mem_writes for a in apps ],
    'Donuts-75': [ a.donuts_75.num_mem_writes for a in apps ],
    'Donuts-88': [ a.donuts_88.num_mem_writes for a in apps ],
    'Donuts-100': [ a.donuts_100.num_mem_writes for a in apps ],
  }, index = [ a.name for a in apps ])
  return pd.concat({"Memory Writes": mem_writes_df}, axis=1)


def get_checkpoints_dataframe_2(apps):
  checkpoints_df = pd.DataFrame({
    'Donuts-50': [ a.donuts_50.num_checkpoints for a in apps ],
    'Donuts-63': [ a.donuts_63.num_checkpoints for a in apps ],
    'Donuts-75': [ a.donuts_75.num_checkpoints for a in apps ],
    'Donuts-88': [ a.donuts_88.num_checkpoints for a in apps ],
    'Donuts-100': [ a.donuts_100.num_checkpoints for a in apps ],
  }, index = [ a.name for a in apps ])
  return pd.concat({"Checkpoints": checkpoints_df}, axis=1)


def generate_results_dataframe_2(apps):
  df = pd.concat([
    get_exec_time_dataframe_2(apps),
    get_mem_access_dataframe_2(apps),
    get_mem_writes_dataframe_2(apps),
    get_mem_bandwidth_usage_dataframe_2(apps),
    get_checkpoints_dataframe_2(apps)
  ], axis=1, names=['Application'])
  return df
  
  
class App_2:
  def __init__(self, name, **configs):
    self.name = name
    self.configs = configs
    print(configs['donuts_50'])
    # for key, value in configs.items():
    #   print(value)
  
  def __str__(self):
    return f"Name: {self.name}\tDonuts 50: {self.donuts_50}\tDonuts 75: {self.donuts_75}\tDonuts 100: {self.donuts_100}\n"

  
def main_2(resultsrootdir = None):
  if resultsrootdir is None:
    resultsrootdir = f"{os.environ['BENCHMARKS_ROOT']}/out/cpu2006/threshold"
  
  apps = []
  # for app_name in os.listdir(resultsrootdir):
  
  app_cpu2006_sorted = [
    'libquantum', 
    'bwaves', 
    'cactusADM', 
    'lbm', 
    'wrf', 
    'leslie3d',
    'sjeng',
    'bzip2',
    'mcf',
    'zeusmp',
    'milc',
    'astar',
    # 'gobmk',
    # 'perlbench',
    # 'gcc',
    # 'omnetpp',
    # 'gromacs',
    # 'dealII',
    # 'namd',
    # 'calculix',
    # 'gamess',
    # 'h264ref',
    # 'sphinx3',
    # 'povray',
    # 'tonto',
    # 'GemsFDTD'
  ]
  
  for app_name in app_cpu2006_sorted:
    app_dir = f"{resultsrootdir}/{app_name}"
    print(app_dir)
    try:
      if os.path.isdir(app_dir) and app_dir != 'threshold':
        app = App_2(app_name, 
                    donuts_50 = get_execution_data(f"{app_dir}/donuts-th50"),
                    donuts_63 = get_execution_data(f"{app_dir}/donuts-th63"),
                    donuts_75 = get_execution_data(f"{app_dir}/donuts-th75"),
                    donuts_88 = get_execution_data(f"{app_dir}/donuts-th88"),
                    donuts_100 = get_execution_data(f"{app_dir}/donuts-th100"))
        apps.append(app)
    except:
      print(f"An exception occurred in application: {app_dir}")
  
  # df = generate_results_dataframe_2(apps)
  # print(df)
  # generate_sheet(df, '.')


if __name__ == '__main__':
  # main()
  main_2()
