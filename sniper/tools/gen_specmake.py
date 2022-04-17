#!/usr/bin/env python3

import sys, os, re
from get_speccmds import get_spec_cmds, get_app_spec_cmds

def create_makefile(path, cmds):
  with open(path, 'w') as f:
    if len(cmds) == 1:
      print(f"run:\n\t{cmds[0]}", file=f)
    else:
      print(f"run: 0\n", file=f)
      for idx, cmd in enumerate(cmds):
        print(f"{idx}:\n\t{cmd}", file=f)
  print(f"Makefile generated to path: {path}")


def main():
  root_dir = sys.argv[1] if len(sys.argv) == 2 else f"{os.environ['BENCHMARKS_ROOT']}/cpu2017"
  apps = list(filter(lambda f: os.path.isdir(f"{root_dir}/{f}"), os.listdir(root_dir)))
  for app in apps:
    get_app_spec_cmds(f"{root_dir}/{app}")
    # run_dir = f"{root_dir}/{app}/run"
    # runs = list(filter(lambda f: os.path.isdir(f"{run_dir}/{f}"), os.listdir(run_dir)))
    # for run in runs:
    #   create_makefile(f"{run_dir}/{run}/Makefile", get_spec_cmds(f"{run_dir}/{run}"))


if __name__ == '__main__':
  main()