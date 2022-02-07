import os
import argparse


class Application:
	def __init__(self, id, name, category = '', min_cores = 1):
		self.id = id
		self.name = name
		self.category = category
		self.min_cores = min_cores

	def __repr__(self):
		return '{}.{} ({})'.format(self.id, self.name, self.category)


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
    args = parse_args()


def add_app_to_spooler(app, input, num_cores, config, out_dir, num_instr):
	os.system('mkdir -p {}'.format(out_dir))
	cmd = 'tsp ./run-sniper -p cpu2006-{} -i {} -n {} -c {} -d {} -s stop-by-icount:{} \> {}'.\
		format(app.name, input, num_cores, config, out_dir, num_instr, '{}/out.txt'.format(out_dir))
	print(cmd)
	os.system(cmd)

def main():
    os.chdir(os.environ['BENCHMARKS_ROOT'])

    num_slots = 4
    app_list = CPU2006_APPS
    input = 'ref'
    num_cores = 1
    config = 'baseline'
    out_dir_base = 'out/cpu2006'
    num_instr = 40000000

    os.system('tsp -S {}'.format(num_slots))
    for app in app_list:
        out_dir = '{}/{}/{}'.format(out_dir_base, app.name, config)
        add_app_to_spooler(app, input, num_cores, config, out_dir, num_instr)


if __name__ == "__main__":
    main()
