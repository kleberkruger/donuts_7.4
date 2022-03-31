#!/usr/bin/env python3

# Default results path: 
# BENCHMARKS_ROOT/out/<test-name>/<benchmark-name>/<app-name>/<config>

import argparse, os, subprocess, json, re
from tkinter.tix import COLUMN
import pandas as pd

COLUMN_OPTIONS = ['r','b','a','w','l','o','c']

def atoi(text):
  return int(text) if text.isdigit() else text

def natural_keys(text):
  return [atoi(c) for c in re.split(r'(\d+)', text)]


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
  parser.add_argument('-i', '--info', type=str, nargs='+', choices=COLUMN_OPTIONS, default=COLUMN_OPTIONS, help='information colums')
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
    os.path.isdir(f"{root_dir}/{f}"), sorted(os.listdir(root_dir), key=natural_keys)))
  configs = args.config if args.config else find_configs(root_dir, app_names)
  return root_dir, app_names, configs, args.info, args.out, args.err


def get_execution_data(path):
  return json.loads(subprocess.check_output(["./get_exec_data.py", path], universal_newlines=True))


def get_dataframe(apps, configs, attr, title = None, in_percent = False):
  title = attr if title is None else title
  data = dict([(c, [a.data[c][attr] / (100.0 if in_percent else 1) for a in apps]) for c in configs])
  df = pd.DataFrame(data, index = [ a.name for a in apps ])
  return pd.concat({title: df}, axis=1)


def generate_results_dataframe(apps, configs, infos):
  all_dataframes = {
    'r': get_dataframe(apps, configs, 'runtime', 'Runtime'),
    'b': get_dataframe(apps, configs, 'avg_bandwidth_usage', 'Average Bandwidth Usage', in_percent=True),
    'a': get_dataframe(apps, configs, 'num_mem_access', 'Memory Access'),
    'w': get_dataframe(apps, configs, 'num_mem_writes', 'Memory Writes'),
    'l': get_dataframe(apps, configs, 'num_mem_logs', 'Memory Logs'),
    'o': get_dataframe(apps, configs, 'num_buffer_overflow', 'Memory Buffer Overflow'),
    'c': get_dataframe(apps, configs, 'num_checkpoints', 'Number of Checkpoints'),
  }
  df = pd.concat([all_dataframes[i] for i in infos], axis=1, names=['Application'])
  df.index.name = 'Application'
  # return df.sort_index()
  return df


def generate_sheet(df, out_file):
  with pd.ExcelWriter(out_file, engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name='SPEC CPU2006')


def main():
  args = parse_args()
  root_dir, app_names, configs, infos, out_file, err_file = get_args(args)
  apps = []
  for app_name in app_names:
    app_dir = f"{root_dir}/{app_name}"
    try:
      app_data = dict([(c, get_execution_data(f"{app_dir}/{c}")) for c in configs])
      apps.append(AppData(app_name, app_data))
    except:
      print(f"An exception occurred in application: {app_dir}")
  
  df = generate_results_dataframe(apps, configs, infos)
  generate_sheet(df, out_file)

  
if __name__ == '__main__':
  main()
