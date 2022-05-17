#!/usr/bin/env python3

# Usage:
# ./get_speccmds.py <*path>
# ./get_speccmds.py <*app (id or id.name or name)> <*size> <index>

import sys, os, errno, argparse

def required_length(nmin,nmax):
  class RequiredLength(argparse.Action):
    def __call__(self, parser, args, values, option_string=None):
      if not nmin<=len(values)<=nmax:
        msg='argument "{f}" requires between {nmin} and {nmax} arguments'.format(f=self.dest,nmin=nmin,nmax=nmax)
        raise argparse.ArgumentTypeError(msg)
        setattr(args, self.dest, values)
        return RequiredLength

def parse_args():
  # parser = argparse.ArgumentParser()
  # app_args_group = parser.add_argument_group()
  # app_args_group.add_argument('app', type=str, help='application (<id>, <name> or <id.name>)')
  # app_args_group.add_argument('input', type=str, choices=['test', 'train', 'ref'], help='input size')
  # app_args_group.add_argument('index', type=int, default=0, help='index of input')
  # exclusive_group = parser.add_mutually_exclusive_group()
  # exclusive_group.add_argument(app_args_group)
  # exclusive_group.add_argument('path', type=str, help='application run path')
  # parser.add_argument('-r', '--root', type=str, default=f"{os.environ['BENCHMARKS_ROOT']}/cpu2017", help='<root-path> from cpu2017 directory')
  # parser.add_argument('-t', '--tune', type=str, default='base', help='tune')
  # parser.add_argument('-o', '--out', '--output', type=str, help='response output file')
  
  # # create the top-level parser
  # parser = argparse.ArgumentParser(prog='PROG')
  # parser.add_argument('--foo', action='store_true', help='help for foo arg.')
  # subparsers = parser.add_subparsers(help='help for subcommand', dest="subcommand")

  # # create the parser for the "command_1" command
  # parser_a = subparsers.add_parser('command_1', help='command_1 help')
  # parser_a.add_argument('a', type=str, help='help for bar, positional')

  # # create the parser for the "command_2" command
  # parser_b = subparsers.add_parser('command_2', help='help for command_2')
  # parser_b.add_argument('b', type=str, help='help for b')
  # parser_b.add_argument('c', type=str, action='store', default='', help='test')
  
  parser = argparse.ArgumentParser()
  parser.add_argument('args', type=str, nargs='+', help='arguments')
  
  return parser.parse_args()


def extract_cmd(line):
  cmd = line[line.find("../run"):].split(' ', 1)
  exe, args = os.path.basename(cmd[0]), cmd[1][:cmd[1].find('>')]
  return f"./{exe} {args}".strip()


def get_spec_cmds(path):
  speccmds_path = os.path.join(path, 'speccmds.cmd') if os.path.isdir(path) else path
  if not os.path.exists(speccmds_path):
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), speccmds_path)
  cmds = []
  with open(speccmds_path, 'r') as file:
    for line in file:
      if (line.startswith('-i') or line.startswith('-o') or line.startswith('-e')):
        cmds.append(extract_cmd(line))
  return cmds


def get_app_spec_cmds(app_path):
  run_path = f"{app_path}/run"
  runs = list(filter(lambda f: os.path.isdir(f"{run_path}/{f}"), os.listdir(run_path)))
  data = {
    'base': 
      {
        'test': [],
        'train': [],
        'ref': [],
      },
    'peak':
      {
        'test': [],
        'train': [],
        'ref': [],
      },
  }
  for run in runs:
    _, tune, size, _ = run.split('_', 3)
    if size.startswith('ref'):
      size = 'ref'
    data[tune][size] = get_spec_cmds(f"{run_path}/{run}")
  return data

    
def get_app_spec_cmd(app_name, size, index, tune='base', cpu2017_path=f"{os.environ['BENCHMARKS_ROOT']}/cpu2017"):
  run_dir = f"run_{tune}_{size}_donuts-m64.0000"
  path = os.path.join(cpu2017_path, app_name, 'run', run_dir)
  return get_spec_cmds(path)[index]


def main():
  cmds = get_spec_cmds(sys.argv[1])
  for cmd in cmds:
    print(cmd)


if __name__ == '__main__':
  # main()
  # cmd = get_app_spec_cmd('502.gcc_r', 'test', 0)
  # print(cmd)
  args = parse_args()
  print(args)
