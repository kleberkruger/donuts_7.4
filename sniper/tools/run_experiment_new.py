#!/usr/bin/env python3

import sys, os, argparse

# sys.path.append(os.path.join(os.path.dirname(__file__), 'tools', 'scheduler'))
# import graphite_tools
# sys.path.append(os.path.join(os.path.dirname(__file__), 'tools', 'python'))
# import env_setup_bm
# sys.path.append(os.path.join(env_setup_bm.sniper_root(), 'tools'))
# import run_sniper

GRAPHITE_ROOT = os.environ['GRAPHITE_ROOT']
BENCHMARKS_ROOT = os.environ['BENCHMARKS_ROOT']

DEFAULT_RESULTS_ROOT_PATH = os.path.join(GRAPHITE_ROOT, 'results')

sys.path.insert(0, BENCHMARKS_ROOT)

abspath = lambda d: os.path.abspath(os.path.join(d))

HOME = abspath(os.path.dirname(__file__))

from suites import modules

def load_benchmark_apps():
  benchmarks = {}
  for module in sorted(modules):
    module = __import__(module)
    try:
      benchmarks[module.__name__] = module.allbenchmarks()
    except TypeError:
      print('INFO: %s not downloaded yet, run make to download its components.' % module.__name__)    
  return benchmarks

ALL_BENCHMARKS = load_benchmark_apps()


def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('config', type=str, nargs='+', help='sniper configurations to the experiment')
  parser.add_argument('-s', '--slots', type=int, default=4, help='number of task-spooler slots')
  parser.add_argument('-p', '--benchmark', type=str, choices=sorted(ALL_BENCHMARKS.keys()), default=['cpu2006'],
                      help='benchmark selected')
  parser.add_argument('-a', '--apps', type=str, nargs='+', default=['all'], help='applications to run')
  parser.add_argument('-i', '--in', '--input', type=str, default='ref', help='input type')
  parser.add_argument('-r', '--root', type=str, default=DEFAULT_RESULTS_ROOT_PATH, help='results root directory path')
  parser.add_argument('-l', '--label', '--name', type=str, help='test name (label)')
  parser.add_argument('-n', '--ncores', '--core', type=int, nargs='+', default=[1], help='number of cores to run')
  parser.add_argument('-t', '--instr', type=int, default=1000000000, help='number of instructions')
  parser.add_argument('-m', '--more', type=int, nargs='+', help='run n more-intensive-applications <attributte>. Example: p8 m8 b8>')
  parser.add_argument('-f', '--force', help='force test (override old results)')
  parser.add_argument('--debug', help='debug mode (only shows the commands)')
  return parser.parse_args()


def get_args(args):
  return [], [], []


def get_sniper_cmd(benchmark, app, input, ncores, config, out, ninstr, tsp_usage=True):
  tsp = 'tsp ' if tsp_usage else ''
  return f"{tsp}./run-sniper -p {benchmark}-{app} -i {input} -n {ncores} -c {config} -d {out} -s stop-by-icount:{ninstr}"


def add_app_to_spooler(benchmark, app, input, num_cores, config, out_dir, num_instr, run_mode=True):
  print(get_sniper_cmd(benchmark, app, input, num_cores, config, out_dir, num_instr))


def main():
  args = parse_args()
  print(args)
  apps = []
  for n in args.ncores:
    for app in apps:
      for c in args.configs:
        # add_app_to_spooler()
        pass


if __name__ == "__main__":
  main()
