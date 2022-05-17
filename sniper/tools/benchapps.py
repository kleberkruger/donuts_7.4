#!/usr/bin/env python3

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


def get_apps():
  pass


def get_app_names():
  pass


def get_benchmark():
  pass


def main():
  pass


if __name__ == "__main__":
  main()
