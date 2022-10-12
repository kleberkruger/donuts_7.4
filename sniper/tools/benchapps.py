#!/usr/bin/env python

import sys, os, json

sys.path.insert(0, os.environ['BENCHMARKS_ROOT'])

from suites import modules

# def load_benchmark_apps():
#   benchmarks = {}
#   for module in sorted(modules):
#     module = __import__(module)
#     try:
#       benchmarks[module.__name__] = module.allbenchmarks()
#     except TypeError as ex:
#       raise ex('INFO: %s not downloaded yet, run make to download its components.' % module.__name__)
#   return benchmarks


def load_benchmark_apps(benchmark):
  module = __import__(benchmark)
  try:
    return module.allbenchmarks()
  except TypeError as ex:
    raise ex('INFO: %s not downloaded yet, run make to download its components.' % module.__name__)
  

def load_benchmark_inputs(benchmark):
  module = __import__(benchmark)
  try:
    return module.allinputs()
  except TypeError as ex:
    raise ex('INFO: %s not downloaded yet, run make to download its components.' % module.__name__)
  
  
def get_benchmarks():
  return sorted(modules)


def get_apps(benchmark=None):
  return load_benchmark_apps(benchmark) if benchmark else \
    dict([(b, load_benchmark_apps(b)) for b in sorted(modules)])
    
def print_get_apps(benchmark=None):
  print(get_apps(benchmark))


def get_app_names():
  pass


def get_benchmark(app):
  pass


def main():
  func = sys.argv[1] if len(sys.argv) > 1 else 'get_apps'
  if func == 'get_apps':
    args = sys.argv[2] if len(sys.argv) > 2 else None
    print(json.dumps(get_apps(args)))
  elif func == 'get_benchmarks':
    print(json.dumps(get_benchmarks()))
  else:
    sys.stderr.write("Invalid function!\n")
    

if __name__ == "__main__":
  main()
