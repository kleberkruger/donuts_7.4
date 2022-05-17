#!/usr/bin/env python3

from distutils.log import error
import sys, os, argparse, shutil

GRAPHITE_ROOT = os.environ['GRAPHITE_ROOT']
BENCHMARKS_ROOT = os.environ['BENCHMARKS_ROOT']

TASK_SPOOLER_CMD = 'tsp'

DEFAULT_RESULTS_ROOT_PATH = os.path.join(GRAPHITE_ROOT, 'results')

ALL_BENCHMARKS = sorted(['cpu2006', 'cpu2017'])

def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('config', type=str, nargs='+', 
                      help='sniper configurations to the experiment')
  parser.add_argument('-s', '--slots', type=int, default=4, 
                      help='number of task-spooler slots')
  parser.add_argument('-p', '--benchmark', type=str, choices=ALL_BENCHMARKS, 
                      help='benchmark selected')
  parser.add_argument('-a', '--apps', type=str, nargs='+', default=['all'], 
                      help='applications to run')
  parser.add_argument('-i', '--in', '--input', dest='input', type=str, default='ref', 
                      help='input type')
  parser.add_argument('-r', '--root', type=str, default=DEFAULT_RESULTS_ROOT_PATH, 
                      help='results root directory path')
  parser.add_argument('-l', '--label', '--name', type=str, 
                      help='test name (label)')
  parser.add_argument('-n', '--ncores', '--core', type=int, nargs='+', default=[1], 
                      help='number of cores to run')
  parser.add_argument('-t', '--instr', type=int, default=1000000000, 
                      help='number of instructions')
  parser.add_argument('-m', '--more', nargs='+', 
                      help='run n more-intensive <attributte> applications. Example: p8 m8 b8>')
  parser.add_argument('-f', '--force', action='store_true', 
                      help='force test (override old results)')
  parser.add_argument('--debug', action='store_true', 
                      help='debug mode (only shows the commands)')
  return parser.parse_args()


def get_sniper_cmd(benchmark, app, input, ncores, config, out, ninstr, tsp_usage=True):
  tsp = f'{TASK_SPOOLER_CMD} ' if tsp_usage else ''
  return f"{tsp}./run-sniper -p {benchmark}-{app} -i {input} -n {ncores} -c {config} -d {out} -s stop-by-icount:{ninstr}"


def add_experiment_to_spooler(benchmark, app, input, ncores, config, out, ninstr, debug=False, force=False):
  cmd = get_sniper_cmd(benchmark, app, input, ncores, config, out, ninstr, True)
  # if already exists a result... except in force mode, do nothing!
  print(cmd)
  
  
def get_benchmark(app):
  return 'parsec' if app == 'ferret' else 'cpu2006'


def load_benchmark_apps(benchmark):
  return ['gcc', 'soplex', 'lbm']


def extend_apps(benchmark, group):
  return ['gcc', 'soplex']


def detect_benchmark(apps):
  benchmark = get_benchmark(apps[0])
  if len(apps) > 1:        
    for app in apps[1:]:
      if get_benchmark(app) != benchmark:
        raise Exception('Applications from different benchmarks')
  return benchmark


def check_configs(configs):
  errors = []
  for config in configs:
    config_file = config if config.endswith('.cfg') else f'{config}.cfg'
    if not os.path.exists(os.path.join(GRAPHITE_ROOT, 'config', config_file)):
      errors.append(config)
  return errors


def check_apps(benchmark_apps, apps):
  result = set(apps) - set(benchmark_apps)
  print(result)
  return list(result)


def main():  
  args = parse_args()
  if not shutil.which(TASK_SPOOLER_CMD) and not args.debug:
    print(f"task-spooler ({TASK_SPOOLER_CMD}) is not installed. Execute in debug mode (--debug) or install it!\n"
           "Example: sudo apt-get install -y task-spooler", file=sys.stderr)
    exit(1)
  
  benchmark = args.benchmark if args.benchmark else 'cpu2006' if args.apps == ['all'] else detect_benchmark(args.apps)
  benchmark_apps = load_benchmark_apps(benchmark)
  # apps = extend_apps(benchmark, args.apps)
  apps = args.apps
  error = check_apps(benchmark_apps, apps)
  print(error)
  
  # error = check_configs(args.config)
  # print(error)
  
  for n in args.ncores:
    for app in apps:
      for config in args.config:
        out = ''
        # add_experiment_to_spooler(args.benchmark, app, args.input, n, config, out, args.instr, args.debug, args.force)


if __name__ == "__main__":
  main()
