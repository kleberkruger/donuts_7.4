#!/usr/bin/env python3

# Default results path: 
# BENCHMARKS_ROOT/out/<test-name>/<benchmark-name>/<app-name>/<config>

# TODO: Passar o caminho de um arquivo de entrada e lá terá as configurações do teste a ser executado?
# Path das configurações com seu label
# Qual das configurações é a baseline

import argparse, os, subprocess, json, re
from copy import copy
from math import ceil
import pandas as pd

COLUMN_OPTIONS = ['r','a','w','l','o','b','c','m']
DEFAULT_RESULTS_PATH = f"{os.environ['DONUTS_ROOT']}/results"

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
  parser.add_argument('-r', '--root', type=str, default=DEFAULT_RESULTS_PATH, help='<root-path> from results directory')
  parser.add_argument('-t', '--test', type=str, help='test name')
  parser.add_argument('-n', '--ncores', type=int, nargs='+', help='select number of cores')
  parser.add_argument('-p', '--benchmark', type=str, default='cpu2006', help='benchmark selected')
  parser.add_argument('-a', '--app', '--apps', type=str, nargs='+', default=[], help='applications to extract results')
  parser.add_argument('-c', '--config', '--configs', type=str, nargs='+', default=[], help='configurations to extract results')
  parser.add_argument('-b', '--baseline', type=str, help='select baseline configuration')
  parser.add_argument('-i', '--info', type=str, nargs='+', choices=COLUMN_OPTIONS, default=COLUMN_OPTIONS, help='information colums')
  parser.add_argument('-ct', '--checkpoint-times', action='store_true', help='generate a checkpoint-times tab')
  parser.add_argument('-cs', '--checkpoint-sizes', action='store_true', help='generate a checkpoint-sizes tab')
  parser.add_argument('-o', '--out', '--output', type=str, help='results output file')
  parser.add_argument('-e', '--err', '--error', type=str, default='results_error.txt', help='error output file')
  return parser.parse_args()


def find_configs(root_dir, app_names):
  all_configs = []
  for app_name in app_names:
    app_dir = f"{root_dir}/{app_name}"
    try:
      app_configs = list(filter(lambda f: os.path.isdir(f"{app_dir}/{f}"), sorted(os.listdir(app_dir), key=natural_keys)))
      new_configs = set(app_configs) - set(all_configs)
      all_configs = all_configs + list(new_configs)
    except:
      print(f"An exception occurred in application: {app_dir}")
  return sorted(all_configs, key=natural_keys)
  
  
def get_args(args):
  root_dir = f"{args.root}/{args.test}" if args.test else args.root
  root_dir += f"/{args.benchmark}"
  app_names = args.app if args.app else list(filter(lambda f: 
    os.path.isdir(f"{root_dir}/{f}"), sorted(os.listdir(root_dir), key=natural_keys)))
  configs = args.config if args.config else find_configs(root_dir, app_names)
  test_name = '_' + args.test.replace('/', '-') if args.test else ''
  out_file = f"results{test_name}_{args.benchmark}.xlsx"
  cores = args.ncores # TODO: use this parameter
  return root_dir, args.benchmark, app_names, cores, configs, args.info, out_file, args.err


def get_execution_data(path):
  return json.loads(subprocess.check_output(['./get_exec_data.py', '--all', path], universal_newlines=True))


def get_dataframe(apps, configs, attr, title = None, in_percent = False, style=None):
  title = attr if title is None else title
  data = dict([(c, [a.data[c][attr] / 100.0 if in_percent else a.data[c][attr] for a in apps]) for c in configs])
  df = pd.DataFrame(data, index = [ a.name for a in apps ])
  if style is not None: # TODO: Fazer isto funcionar no excel
    df.style.set_properties(**style)
  return pd.concat({title: df}, axis=1)


def generate_results_dataframe(apps, configs, infos):
  all_dataframes = {
    'r': get_dataframe(apps, configs, 'runtime', 'Runtime'),
    'a': get_dataframe(apps, configs, 'num_mem_access', 'Memory Access'),
    'w': get_dataframe(apps, configs, 'num_mem_writes', 'Memory Writes'),
    'l': get_dataframe(apps, configs, 'num_mem_logs', 'Memory Logs'),
    'o': get_dataframe(apps, configs, 'num_buffer_overflow', 'Memory Buffer Overflow'),
    'b': get_dataframe(apps, configs, 'avg_bandwidth_usage', 'Average Bandwidth Usage', in_percent=True),
    'c': get_dataframe(apps, configs, 'num_checkpoints', 'Number of Checkpoints'),
    'm': get_dataframe(apps, configs, 'max_ckpt_size', 'Max Checkpoint Size'),
    'e': get_dataframe(apps, configs, 'error', 'Error', style={'color': 'red'})
  }
  df = pd.concat([all_dataframes[i] for i in infos], axis=1, names=['Application'])
  df.index.name = 'Application'
  # return df.sort_index()
  return df


def generate_sheet(out_file, df_sheets):
  with pd.ExcelWriter(out_file, engine='xlsxwriter') as writer:
    for sheet_name, df in df_sheets.items():
      df.to_excel(writer, sheet_name=sheet_name)


def remove_baselines(configs):
  configs = configs.copy()
  configs.remove('baseline-nvm')
  return configs
 
      
def generate_checkpoint_series(apps, configs):
  configs = remove_baselines(configs)
  app_dfs = {}
  for app in apps:
    app_ckpts = {}
    for config in configs:
      # ckpts = app.data[config]['checkpoints']
      # if not ckpts:
      #   print('removing ' + app.name + ' ' + config)
      #   continue
      app_ckpts[config] = pd.Series([ceil(c / 1024) for c in app.data[config]['checkpoints']])
    # app_dfs[app] = pd.concat(app_ckpts.values(), keys=app_ckpts.keys(), axis=1).fillna(0).astype('Int64')
    app_dfs[app.name] = pd.concat(app_ckpts.values(), keys=app_ckpts.keys(), axis=1).astype('Int64')
  # for df in app_dfs.values():
  #   print(df)
  data = pd.concat(app_dfs.values(), keys=app_dfs.keys(), axis=1)
  print(data)
  return data
    


def generate_sheet_2(out_file, df):
  with pd.ExcelWriter(out_file, engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name='checkpoint sizes')


def load_execution_data(root_dir, app_names, configs, infos):
  apps = []
  error = False
  for app_name in app_names:
    app_dir = f"{root_dir}/{app_name}"
    # app_data = dict([(c, get_execution_data(f"{app_dir}/{c}")) for c in configs])
    app_data = dict()
    for c in configs:
      app_data[c] = get_execution_data(f"{app_dir}/{c}")
      if app_data[c]['error']:
        error = True
    apps.append(AppData(app_name, app_data))
  if error:
    infos.append('e')
  return apps


def main():
  args = parse_args()
  root_dir, benchmark, app_names, ncores, configs, infos, out_file, err_file = get_args(args)
  
  apps = load_execution_data(root_dir, app_names, configs, infos)
  df = generate_results_dataframe(apps, configs, infos)
  generate_sheet(out_file, { benchmark: df })
  
  if args.checkpoint_sizes:
    df = generate_checkpoint_series(apps, configs)
    generate_sheet_2('test.xlsx', df)


if __name__ == '__main__':
  main()

# ./gen_results.py -t spec2017 -p cpu2017 -a perlbench_r gcc_r bwaves_r mcf_r cactuBSSN_r namd_r povray_r lbm_r omnetpp_r wrf_r xalancbmk_r x264_r blender_r cam4_r deepsjeng_r imagick_r leela_r nab_r exchange2_r fotonik3d_r roms_r xz_r perlbench_s gcc_s bwaves_s mcf_s cactuBSSN_s lbm_s omnetpp_s wrf_s xalancbmk_s x264_s cam4_s pop2_s deepsjeng_s imagick_s leela_s nab_s exchange2_s fotonik3d_s roms_s xz_s
# ./gen_results.py -t multicore -p cpu2017 -a perlbench_r gcc_r bwaves_r mcf_r cactuBSSN_r namd_r povray_r lbm_r omnetpp_r wrf_r xalancbmk_r x264_r blender_r cam4_r deepsjeng_r imagick_r leela_r nab_r exchange2_r fotonik3d_r roms_r xz_r