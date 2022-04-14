#!/usr/bin/env python3

import os, argparse


class Application:
	def __init__(self, id, name, category = '', min_cores = 1):
		self.id = id
		self.name = name
		self.category = category
		self.min_cores = min_cores

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
  Application(600, 'perlbench_s'),
  Application(602, 'gcc_s'),
  Application(603, 'bwaves_s'),
  Application(605, 'mcf_s'),
  Application(607, 'cactuBSSN_s'),
  Application(619, 'lbm_s'),
  Application(620, 'omnetpp_s'),
  Application(621, 'wrf_s'),
  Application(623, 'xalancbmk_s'),
  Application(625, 'x264_s'),
  Application(627, 'cam4_s'),
  Application(628, 'pop2_s'),
  Application(631, 'deepsjeng_s'),
  Application(638, 'imagick_s'),
  Application(641, 'leela_s'),
  Application(644, 'nab_s'),
  Application(648, 'exchange2_s'),
  Application(649, 'fotonik3d_s'),
  Application(654, 'roms_s'),
  Application(657, 'xz_s')
]


def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('config', type=str, nargs='+', help='experiment configutarions')
  parser.add_argument('-s', '--slots', type=int, default=4, help='number of task-spooler slots')
  parser.add_argument('-p', '--benchmark', type=str, nargs='+', 
                      choices=['npb', 'parsec', 'splash2', 'cpu2006', 'cpu2017', 'all'], default=['cpu2006'],
                      help='benchmark selected')
  parser.add_argument('-a', '--apps', type=str, nargs='+', default=['all'], help='applications to running' )
  parser.add_argument('-i', '--in', '--input', type=str, nargs='+', default=['ref'], help='input type')
  parser.add_argument('-o', '--out', '--output', type=str, default='out/cpu2006', help='output base path') # Arrumar isso aqui {out/cpu2006/ref}?
  parser.add_argument('-n', '--cores', type=int, nargs='+', default=[1], help='number of cores to running')
  parser.add_argument('-t', '--instr', type=int, nargs='+', default=[1000000000], help='number of instructions')
  parser.add_argument('-m', '--more', type=int, nargs='+', default=[1000000000], help='run n more-intensive <attributte>')
  return parser.parse_args()


def add_app_to_spooler(app, input, num_cores, config, out_dir, num_instr):
  app_type = 'rate' if app.name.endswith('_r') else 'speed'
  app_path = f"{os.environ['BENCHMARKS_ROOT']}/cpu2017/{app.id}.{app.name}/run/run_base_ref{app_type}_donuts-m64.0000"
  make_path = f"{app_path}/Makefile"
  if not os.path.exists(make_path):
    print(f"Não existe configuração de execução para o {app.name}")
    return
  with open(make_path) as file:
    speccmd = file.readline()
    
  run_sniper_path = f"{os.environ['GRAPHITE_ROOT']}/run-sniper"
  out_dir = f"{os.environ['BENCHMARKS_ROOT']}/{out_dir}"
  os.system(f"tsp mkdir -p {out_dir}")
  # cmd = f"tsp ./run-sniper -p cpu2006-{app.name} -i {input} -n {num_cores} -c {config} -d {out_dir} -s stop-by-icount:{num_instr}"
  cmd = f"tsp {run_sniper_path} -n {num_cores} -c {config} -d {out_dir} -s stop-by-icount:{num_instr} -- {speccmd}"
  print(f"cd {app_path}")
  print(cmd)
  os.chdir(app_path)
  os.system(cmd)


def main():
  os.chdir(os.environ['BENCHMARKS_ROOT'])
  
  num_slots = 6
  app_list = CPU2017_APPS
  input = 'ref'
  num_cores = 1
  config = 'picl-enabled'
  out_dir_base = 'out/spec2017/cpu2017'
  num_instr = 1000000000

  os.system(f"tsp -S {num_slots}")
  for app in app_list:
    out_dir = f"{out_dir_base}/{app.name}/{config}"
    add_app_to_spooler(app, input, num_cores, config, out_dir, num_instr)


if __name__ == "__main__":
  main()
	# print(parse_args())
