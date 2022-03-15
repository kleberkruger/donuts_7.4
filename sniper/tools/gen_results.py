#!/usr/bin/env python3

# Default results path: 
# BENCHMARKS_ROOT/out/<test-name>/<benchmark-name>/<app-name>/<config>

import argparse, os, subprocess, json, re
import pandas as pd

import re

def atoi(text):
  return int(text) if text.isdigit() else text

def natural_keys(text):
  return [atoi(c) for c in re.split(r'(\d+)', text)]

class RunData:
    
  def __init__(self, data, runtime, avg_bandwidth_usage, num_mem_access, num_mem_writes,
               num_mem_logs = 0, num_buffer_overflow = 0, num_checkpoints = 0):
    self.data = data
    self.runtime = runtime
    self.avg_bandwidth_usage = avg_bandwidth_usage
    self.num_mem_access = num_mem_access
    self.num_mem_writes = num_mem_writes
    self.num_mem_logs = num_mem_logs
    self.num_buffer_overflow = num_buffer_overflow
    self.num_checkpoints = num_checkpoints
    
  def __repr__(self):
    return json.dumps(vars(self))


class AppData:
      
  def __init__(self, name, data):
    self.name = name
    self.data = data

  def __repr__(self):
    info = f"{self.name}:\n"
    for key, value in self.data.items():
      info += f"\t{key}: {value}\n"
    return info
  
  
def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('-r', '--root', type=str, default=f"{os.environ['BENCHMARKS_ROOT']}/out", help='<root-path> from results directory')
  parser.add_argument('-t', '--test', type=str, help='test name')
  parser.add_argument('-p', '--benchmark', type=str, default='cpu2006', help='benchmark selected')
  parser.add_argument('-a', '--app', '--apps', type=str, nargs='+', default=[], help='applications to extract results')
  parser.add_argument('-c', '--config', '--configs', type=str, nargs='+', default=[], help='configurations to extract results')
  parser.add_argument('-b', '--baseline', type=str, help='select baseline configuration')
  parser.add_argument('-i', '--info', type=str, nargs='+', choices=['r','b','a','w','l','o','c'], default=[], help='information colums')
  parser.add_argument('-o', '--out', '--output', type=str, default='results_cpu2006.xlsx', help='results output file')
  parser.add_argument('-e', '--err', '--error', type=str, default='results_error.txt', help='error output file')
  return parser.parse_args()


def find_configs(root_dir, app_names):
  all_configs = []
  for app_name in app_names:
    app_dir = f"{root_dir}/{app_name}"
    app_configs = list(filter(lambda f: os.path.isdir(f"{app_dir}/{f}"), sorted(os.listdir(app_dir), key=natural_keys)))
    new_configs = set(app_configs) - set(all_configs)
    all_configs = all_configs + list(new_configs)
  return sorted(all_configs, key=natural_keys)
  
  
def get_args(args):
  root_dir = f"{args.root}/{args.test}" if args.test else args.root
  root_dir += f"/{args.benchmark}"
  app_names = args.app if args.app else list(filter(lambda f: 
    os.path.isdir(f"{root_dir}/{f}"), sorted(os.listdir(root_dir))))
  configs = args.config if args.config else find_configs(root_dir, app_names)
  return root_dir, app_names, configs


# TODO: create a separated module execution_data?
# TODO: put in try cat?
def get_execution_data(path):
  data = json.loads(subprocess.check_output(["./get_exec_data.py", path], universal_newlines=True))
  return RunData(data, 
                 data['exec_time'], data['mem_bandwidth_usage'], 
                 data['num_mem_access'], data['num_mem_writes'], data['num_mem_logs'], 
                 data['num_buffer_overflow'], data['num_checkpoints'])


def get_app_data_array(apps, config):
  return [a.data[config].runtime for a in apps]


def get_runtime_dataframe(apps, configs):
  data = dict([(c, [a.data[c].runtime for a in apps]) for c in configs])
  runtime_df = pd.DataFrame(data, index = [ a.name for a in apps ])
  return pd.concat({"Runtime": runtime_df}, axis=1)


def get_dataframe(apps, configs, attr, title):
  data = dict([(c, [a.data[c].data[attr] for a in apps]) for c in configs])
  df = pd.DataFrame(data, index = [ a.name for a in apps ])
  return pd.concat({title: df}, axis=1)


def get_dataframe_perc(apps, configs, attr, title):
  data = dict([(c, [a.data[c].data[attr] / 100.0 for a in apps]) for c in configs])
  df = pd.DataFrame(data, index = [ a.name for a in apps ])
  return pd.concat({title: df}, axis=1)


def get_avg_bandwidth_usage_dataframe(apps, configs):
  data = dict([(c, [a.data[c].avg_bandwidth_usage / 100.0 for a in apps]) for c in configs])
  avg_bandwidth_usage_df = pd.DataFrame(data, index = [ a.name for a in apps ])
  return pd.concat({"Average DRAM Bandwidth Usage": avg_bandwidth_usage_df}, axis=1)


def generate_results_dataframe(apps, configs):
  df = pd.concat([
    get_runtime_dataframe(apps, configs),
    get_avg_bandwidth_usage_dataframe(apps, configs),
    get_dataframe(apps, configs, 'num_mem_access', 'Memory Access'),
    get_dataframe(apps, configs, 'num_mem_writes', 'Memory Writes'),
    get_dataframe(apps, configs, 'num_mem_logs', 'Memory Logs'),
    get_dataframe(apps, configs, 'num_buffer_overflow', 'Memory Buffer Overflow'),
    get_dataframe(apps, configs, 'num_checkpoints', 'Number of Checkpoints'),
  ], axis=1, names=['Application'])
  
  # df.index.name = 'Application'
  return df.sort_index()


def generate_sheet(df, output):
  with pd.ExcelWriter(f"{output}/results_cpu2006.xlsx", engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name='SPEC CPU2006')


def main():
  args = parse_args()
  root_dir, app_names, configs = get_args(args)
  apps = []
  for app_name in app_names:
    app_dir = f"{root_dir}/{app_name}"
    try:
      app_data = dict([(c, get_execution_data(f"{app_dir}/{c}")) for c in configs])
      apps.append(AppData(app_name, app_data))
    except:
      print(f"An exception occurred in application: {app_dir}")
  
  df = generate_results_dataframe(apps, configs)
  generate_sheet(df, '.')
  print(df)

  
if __name__ == '__main__':
  main()
