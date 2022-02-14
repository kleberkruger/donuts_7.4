#!/usr/bin/env python3

import os
import argparse


class Application:
	def __init__(self, id, name, category = '', min_cores = 1):
		self.id = id
		self.name = name
		self.category = category
		self.min_cores = min_cores

	def __repr__(self):
		return f"{self.id}.{self.name} - [category: {self.category}, min cores: {self.min_cores}]"


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
	# Application(499, 'specrand', 'floating'),
]

def parse_args():
	parser = argparse.ArgumentParser()

	parser.add_argument('config', type=str, nargs='+', help='experiment configutarions')
	parser.add_argument('-s', '--slots', type=int, default=4, help='number of task-spooler slots')
	parser.add_argument('-b', '--benchmark', type=str, nargs='+', 
						choices=['npb', 'parsec', 'splash2', 'cpu2006', 'cpu2017', 'all'], default=['cpu2006'],
                        help='benchmark selected')
	parser.add_argument('-a', '--apps', type=str, nargs='+', default=['all'], help='applications to running')
	parser.add_argument('-i', '--in', '--input', type=str, nargs='+', default=['ref'], help='input type')
	parser.add_argument('-o', '--out', '--output', type=str, default='out/cpu2006', help='output base path') # Arrumar isso aqui {out/cpu2006/ref}?
	parser.add_argument('-n', '--cores', type=int, nargs='+', default=[1], help='number of cores to running')
	parser.add_argument('-t', '--instr', type=int, nargs='+', default=[1000000000], help='number of instructions')

	return parser.parse_args()


def add_app_to_spooler(app, input, num_cores, config, out_dir, num_instr):
	os.system(f"tsp mkdir -p {out_dir}")
	cmd = f"tsp ./run-sniper -p cpu2006-{app.name} -i {input} -n {num_cores} -c {config} -d {out_dir} -s stop-by-icount:{num_instr}"
	print(cmd)
	os.system(cmd)

def main():
    os.chdir(os.environ['BENCHMARKS_ROOT'])

    num_slots = 6
    app_list = CPU2006_APPS
    input = 'ref'
    num_cores = 1
    config = 'baseline-nvm'
    out_dir_base = 'out/test'
    num_instr = 30000000

    os.system(f"tsp -S {num_slots}")
    for app in app_list:
        out_dir = f"{out_dir_base}/{app.name}/{config}"
        add_app_to_spooler(app, input, num_cores, config, out_dir, num_instr)


if __name__ == "__main__":
    main()
	# print(parse_args())
