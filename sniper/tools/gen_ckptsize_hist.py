#!/usr/bin/env python3

# Default results path: 
# BENCHMARKS_ROOT/out/<test-name>/<benchmark-name>/<app-name>/<config>

# TODO: Passar o caminho de um arquivo de entrada e lá terá as configurações do teste a ser executado?
# Path das configurações com seu label
# Qual das configurações é a baseline

import argparse, os, subprocess, json, re
from math import ceil
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

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


def remove_baselines(configs):
  configs = configs.copy()
  configs.remove('baseline-nvm')
  return configs


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


def remove_outliers(data, outlier = 0.5):
  x = pd.Series(data)  # 200 values
  x = x[x.between(x.quantile(0.0), x.quantile(1.0 - (outlier / 100.0)))]  # without outliers
  return x
  # an_array = np.array(data)
  # mean = np.mean(an_array)
  # standard_deviation = np.std(an_array)
  # distance_from_mean = abs(an_array - mean)
  # max_deviations = 2
  # not_outlier = distance_from_mean < max_deviations * standard_deviation
  # no_outliers = an_array[not_outlier]
  # return no_outliers


def histogram(data, filepath, max=None):
  data = remove_outliers(data, 0.0)

  plt.style.use('seaborn-whitegrid')
  plt.figure(figsize=(10, 5))
  if max:
    plt.xlim(0, max)
    plt.ylim(0.0, 1.0)
  plt.hist(data, weights=np.ones(len(data)) / len(data))
  # plt.title('({}) - Histograma de {}'.format(letter[filepath], filepath))
  plt.title('Histogram of {}'.format(filepath))
  plt.xlabel('Checkpoint Size (KB)')
  plt.ylabel('Percentage of checkpoints')
  plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
  
  if os.path.isfile(filepath + '.png'):
    os.remove(filepath + '.png')
  plt.savefig(filepath + '.png')
  # plt.savefig(filepath + '.svg')
  # plt.savefig(filepath + '.pdf')
  plt.close()
  # print(("[HISTOGRAM] [ Histogram generated at: '{}.png ]".format(filepath)))
  
  
def get_max_ckpt_size(apps):
  max = 0
  for app in apps:
    for data in app.data.values():
      if data['max_ckpt_size'] > max:
        max = data['max_ckpt_size']
  return max


def generate_histograms(apps):
  # max = ceil(get_max_ckpt_size(apps) / 1024)
  print(f'0..{max}')
  for app in apps:
    max = app.data.values()
    for config_name, config_values in app.data.items():
      ckpts = [ceil(c / 1024) for c in config_values['checkpoints']]
      if not ckpts:
        continue
      filepath = os.path.join('histogramas', f'{app.name}_{config_name}')
      histogram(ckpts, filepath, max)


def main():
  args = parse_args()
  root_dir, benchmark, app_names, ncores, configs, infos, out_file, err_file = get_args(args)
  
  apps = load_execution_data(root_dir, app_names, configs, infos)
  generate_histograms(apps)

if __name__ == '__main__':
  main()
