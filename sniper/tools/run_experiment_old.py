#!/usr/bin/env python3

import os, errno

HOME_SNIPER = os.environ['GRAPHITE_ROOT']
HOME_BENCHMARKS = os.environ['BENCHMARKS_ROOT']
postfix = 'donuts-m64.0000'

class Application:
  def __init__(self, id, name, category = '', min_cores = 1):
    self.id = id
    self.name = name
    self.category = category
    self.min_cores = min_cores
    self.fullname = '{}.{}'.format(id, name)
    self.dirpath = os.path.join(HOME_BENCHMARKS, 'cpu2017', self.fullname)
    
  def get_rundir_path(self, inputsize, tune='base'):
    if inputsize == 'ref':
      inputsize = 'refrate' if self.id < 600 else 'refspeed'
    return os.path.join(self.dirpath, 'run', 'run_{}_{}_{}'.format(tune, inputsize, postfix))

  def get_cmd(self, inputsize, index=None, tune='base'):
    cmds = get_spec_cmds(self.get_rundir_path(inputsize, tune))
    return cmds[index] if index is not None else cmds
    
  def __repr__(self):
    return f"{self.id}.{self.name} - [category: {self.category}, min cores: {self.min_cores}]"


PARSEC_APPS = [
  Application(0, 'blackscholes', '', 2),
  Application(0, 'bodytrack', '', 3),
  Application(0, 'facesim', '', 1),
  Application(0, 'ferret', '', 6),
  Application(0, 'fluidanimate', '', 2),
  Application(0, 'freqmine', '', 1),
  Application(0, 'raytrace', '', 2),
  Application(0, 'swaptions', '', 2),
  Application(0, 'vips', '', 3),
  Application(0, 'x264', '', 1),
  Application(0, 'canneal', '', 2),
  Application(0, 'dedup', '', 4),
]

CPU2006_APPS = [
  Application(400, 'perlbench', 'integer'),
  Application(401, 'bzip2', 'integer'),
  Application(403, 'gcc', 'integer'),
  Application(410, 'bwaves', 'floating'),
  Application(416, 'gamess', 'floating'),
  Application(429, 'mcf', 'integer'),
  Application(433, 'milc', 'floating'),
  Application(434, 'zeusmp', 'floating'),
  Application(435, 'gromacs', 'floating'),
  Application(436, 'cactusADM', 'floating'),
  Application(437, 'leslie3d', 'floating'),
  Application(444, 'namd', 'floating'),
  Application(445, 'gobmk', 'integer'),
  Application(447, 'dealII', 'floating'),
  Application(450, 'soplex', 'floating'),
  Application(453, 'povray', 'floating'),
  Application(454, 'calculix', 'floating'),
  Application(456, 'hmmer', 'integer'),
  Application(458, 'sjeng', 'integer'),
  Application(459, 'GemsFDTD', 'floating'),
  Application(462, 'libquantum', 'integer'),
  Application(464, 'h264ref', 'integer'),
  Application(465, 'tonto', 'floating'),
  Application(470, 'lbm', 'floating'),
  Application(471, 'omnetpp', 'integer'),
  Application(473, 'astar', 'integer'),
  Application(481, 'wrf', 'floating'),
  Application(482, 'sphinx3', 'floating'),
  Application(483, 'xalancbmk', 'integer'),
  # Application(498, 'specrand'),
  # # Application(499, 'specrand', 'floating'),
]

CPU2017_APPS = [
  Application(500, 'perlbench_r'),
  Application(502, 'gcc_r'),
  Application(503, 'bwaves_r'),
  Application(505, 'mcf_r'),
  Application(507, 'cactuBSSN_r'),
  Application(508, 'namd_r'),
  Application(510, 'parest_r'),
  Application(511, 'povray_r'),
  Application(519, 'lbm_r'),
  Application(520, 'omnetpp_r'),
  Application(521, 'wrf_r'),
  Application(523, 'xalancbmk_r'),
  Application(525, 'x264_r'),
  Application(526, 'blender_r'),
  Application(527, 'cam4_r'),
  Application(531, 'deepsjeng_r'),
  Application(538, 'imagick_r'),
  Application(541, 'leela_r'),
  Application(544, 'nab_r'),
  Application(548, 'exchange2_r'),
  Application(549, 'fotonik3d_r'),
  Application(554, 'roms_r'),
  Application(557, 'xz_r'),
  # Application(600, 'perlbench_s'),
  # Application(602, 'gcc_s'),
  # Application(603, 'bwaves_s'),
  # Application(605, 'mcf_s'),
  # Application(607, 'cactuBSSN_s'),
  # Application(619, 'lbm_s'),
  # Application(620, 'omnetpp_s'),
  # Application(621, 'wrf_s'),
  # Application(623, 'xalancbmk_s'),
  # Application(625, 'x264_s'),
  # Application(627, 'cam4_s'),
  # Application(628, 'pop2_s'),
  # Application(631, 'deepsjeng_s'),
  # Application(638, 'imagick_s'),
  # Application(641, 'leela_s'),
  # Application(644, 'nab_s'),
  # Application(648, 'exchange2_s'),
  # Application(649, 'fotonik3d_s'),
  # Application(654, 'roms_s'),
  # Application(657, 'xz_s')
]


def extract_cmd(line):
  cmd = line[line.find("../run"):].split(' ', 1)
  exe, args = os.path.basename(cmd[0]), cmd[1][:cmd[1].find('>')]
  return "./{} {}".format(exe, args).strip()


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


def add_app_to_spooler(benchmark, app, input, num_cores, config, out_dir, num_instr, debug=False):  
  out_dir = f"{HOME_BENCHMARKS}/{out_dir}"
  
  if (not debug):
    os.system(f"tsp mkdir -p {out_dir}")
  print(f"tsp mkdir -p {out_dir}")
  
  # cmd = f"tsp ./run-sniper -p {benchmark}-{app.name} -i {input} -n {num_cores} -c {config} -d {out_dir} -s stop-by-icount:{num_instr}"
  runpath = app.get_rundir_path(input)
  specinstr = app.get_cmd(input, 0)
  print(f"cd {runpath}")
  # print(specinstr)
  cmd = f"tsp {HOME_SNIPER}/run-sniper -n {num_cores} -c {config} -d {out_dir} -s stop-by-icount:{num_instr} -- {specinstr}"
  print(cmd + '\n')
  
  os.chdir(runpath)
  if (not debug):
    os.system(cmd)
  os.chdir(HOME_BENCHMARKS)


def main(debug=False):
  os.chdir(HOME_BENCHMARKS)
  
  num_slots = 6
  benchmark = 'cpu2017'
  app_list = CPU2017_APPS
  input = 'ref'
  num_cores = 8
  config = 'donuts-store'
  out_dir_base = 'out/multicore/cpu2017'
  num_instr = 1000000000

  os.system(f"tsp -S {num_slots}")
  for app in app_list:
    out_dir = f"{out_dir_base}/{app.name}/{config}"
    add_app_to_spooler(benchmark, app, input, num_cores, config, out_dir, num_instr, debug)


if __name__ == "__main__":
  main()
