#!/usr/bin/env python3

import string
import sys, os, re


def atoi(text):
  return int(text) if text.isdigit() else text

def natural_keys(text):
  return [atoi(c) for c in re.split(r'(\d+)', text)]


def extract_command(line):
  cmd = line[line.find("../run"):].split(' ', 1)
  exe, args = os.path.basename(cmd[0]), cmd[1][:cmd[1].find('>')]
  return f"./{exe} {args}".strip()


def get_app_cmds(path):
  # path = sys.argv[1]
  cmds = []
  with open(path, 'r') as f:
    for line in f:
      if line.startswith('-i') or line.startswith('-o') or line.startswith('-e'):
        cmds.append(extract_command(line))
  return cmds


def create_makefile(path, cmds):
  with open(path, 'w') as f:
    if len(cmds) == 1:
      print(f"run:\n\t{cmds[0]}", file=f)
    else:
      print(f"run: 0\n", file=f)
      for idx, cmd in enumerate(cmds):
        print(f"{idx}:\n\t{cmd}", file=f)


def main():
  root_dir = f"{os.environ['BENCHMARKS_ROOT']}/cpu2017"
  apps = list(filter(lambda f: os.path.isdir(f"{root_dir}/{f}"), sorted(os.listdir(root_dir), key=natural_keys)))
  for app in apps:
    run_dir = f"{root_dir}/{app}/run"
    runs = list(filter(lambda f: os.path.isdir(f"{run_dir}/{f}"), sorted(os.listdir(run_dir), key=natural_keys)))
    for run in runs:
      create_makefile(f"{run_dir}/{run}/Makefile", get_app_cmds(f"{run_dir}/{run}/speccmds.cmd"))


if __name__ == '__main__':
  main()
