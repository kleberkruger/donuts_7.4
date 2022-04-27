#!/usr/bin/env python

import sys, os, argparse

# sys.path.append(os.path.join(os.path.dirname(__file__), 'tools', 'scheduler'))
# import graphite_tools
# sys.path.append(os.path.join(os.path.dirname(__file__), 'tools', 'python'))
# import env_setup_bm
# sys.path.append(os.path.join(env_setup_bm.sniper_root(), 'tools'))
# import run_sniper

sys.path.insert(0, os.environ['BENCHMARKS_ROOT'])

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
  parser.add_argument('config', type=str, nargs='+', help='experiment configutarions')
  parser.add_argument('-s', '--slots', type=int, default=4, help='number of task-spooler slots')
  parser.add_argument('-p', '--benchmark', type=str, choices=sorted(ALL_BENCHMARKS.keys()), default=['cpu2006'],
                      help='benchmark selected')
  parser.add_argument('-a', '--apps', type=str, nargs='+', default=['all'], help='applications to running' )
  parser.add_argument('-i', '--in', '--input', type=str, nargs='+', default=['ref'], help='input type')
  parser.add_argument('-o', '--out', '--output', type=str, default='out', help='output base path') # Arrumar isso aqui {out/cpu2006/ref}?
  parser.add_argument('-n', '--cores', type=int, nargs='+', default=[1], help='number of cores to running')
  parser.add_argument('-t', '--instr', type=int, nargs='+', default=[1000000000], help='number of instructions')
  parser.add_argument('-m', '--more', type=int, nargs='+', help='run n more-intensive-applications <attributte>. Example: p8 m8 b8>')
  return parser.parse_args()


def main():
  args = parse_args()


if __name__ == "__main__":
  main()
