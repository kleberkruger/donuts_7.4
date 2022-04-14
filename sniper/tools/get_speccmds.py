#!/usr/bin/env python3

import sys, os

def extract_cmd(line):
  cmd = line[line.find("../run"):].split(' ', 1)
  exe, args = os.path.basename(cmd[0]), cmd[1][:cmd[1].find('>')]
  return './' + exe + ' ' + args


def get_spec_cmds(run_path):
  cmds = []
  with open(f"{run_path}/speccmds.cmd", 'r') as file:
    for line in file:
      if (line.startswith('-i') or line.startswith('-o') or line.startswith('-e')):
        cmds.append(extract_cmd(line))
  return cmds


def main():
  cmds = get_spec_cmds(sys.argv[1])
  for cmd in cmds:
    print(cmd)


if __name__ == '__main__':
  main()
