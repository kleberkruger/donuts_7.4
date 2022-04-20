import sys, os, re, subprocess, tempfile, errno

abspath = lambda d: os.path.abspath(os.path.join(d))

HOME = abspath(os.path.dirname(__file__))

postfix = '_base.sniper-x86_64'

class Application:
  def __init__(self, id, name, type=None):
    self.id = id
    self.name = name
    self.type = type
    self.fullname = '{}.{}'.format(id, name)
    self.dirpath = os.path.join(HOME, self.fullname)
    self.data = {}
    self.commands = {}


CPU2017_APPS = [
  Application(500, 'perlbench_r', 'int'),
  Application(502, 'gcc_r', 'int'),
  Application(503, 'bwaves_r', 'fp'),
  Application(505, 'mcf_r', 'int'),
  Application(507, 'cactuBSSN_r', 'fp'),
  Application(508, 'namd_r', 'fp'),
  Application(510, 'parest_r', 'fp'),
  Application(511, 'povray_r', 'fp'),
  Application(519, 'lbm_r', 'fp'),
  Application(520, 'omnetpp_r', 'int'),
  Application(521, 'wrf_r', 'fp'),
  Application(523, 'xalancbmk_r', 'int'),
  Application(525, 'x264_r', 'int'),
  Application(526, 'blender_r', 'fp'),
  Application(527, 'cam4_r', 'fp'),
  Application(531, 'deepsjeng_r', 'int'),
  Application(538, 'imagick_r', 'fp'),
  Application(541, 'leela_r', 'int'),
  Application(544, 'nab_r', 'fp'),
  Application(548, 'exchange2_r', 'int'),
  Application(549, 'fotonik3d_r', 'fp'),
  Application(554, 'roms_r', 'fp'),
  Application(557, 'xz_r', 'int'),
  Application(600, 'perlbench_s', 'int'),
  Application(602, 'gcc_s', 'int'),
  Application(603, 'bwaves_s', 'fp'),
  Application(605, 'mcf_s', 'int'),
  Application(607, 'cactuBSSN_s', 'fp'),
  Application(619, 'lbm_s', 'fp'),
  Application(620, 'omnetpp_s', 'int'),
  Application(621, 'wrf_s', 'fp'),
  Application(623, 'xalancbmk_s', 'int'),
  Application(625, 'x264_s', 'int'),
  Application(627, 'cam4_s', 'fp'),
  Application(628, 'pop2_s', 'fp'),
  Application(631, 'deepsjeng_s', 'int'),
  Application(638, 'imagick_s', 'fp'),
  Application(641, 'leela_s', 'int'),
  Application(644, 'nab_s', 'fp'),
  Application(648, 'exchange2_s', 'int'),
  Application(649, 'fotonik3d_s', 'fp'),
  Application(654, 'roms_s', 'fp'),
  Application(657, 'xz_s', 'int'),
  # Application(996, 'specrand_fs'),
  # Application(997, 'specrand_fr'),
  # Application(998, 'specrand_is'),
  # Application(999, 'specrand_ir'),
]

# CPU2017_APPS = {
#   'perlbench_r': Application(500, 'perlbench_r', 'int'),
#   'gcc_r': Application(502, 'gcc_r', 'int'),
#   'bwaves_r': Application(503, 'bwaves_r', 'fp'),
#   'mcf_r': Application(505, 'mcf_r', 'int'),
#   'cactuBSSN_r': Application(507, 'cactuBSSN_r', 'fp'),
#   'namd_r': Application(508, 'namd_r', 'fp'),
#   'parest_r': Application(510, 'parest_r', 'fp'),
#   'povray_r': Application(511, 'povray_r', 'fp'),
#   'lbm_r': Application(519, 'lbm_r', 'fp'),
#   'omnetpp_r': Application(520, 'omnetpp_r', 'int'),
#   'wrf_r': Application(521, 'wrf_r', 'fp'),
#   'xalancbmk_r': Application(523, 'xalancbmk_r', 'int'),
#   'x264_r': Application(525, 'x264_r', 'int'),
#   'blender_r': Application(526, 'blender_r', 'fp'),
#   'cam4_r': Application(527, 'cam4_r', 'fp'),
#   'deepsjeng_r': Application(531, 'deepsjeng_r', 'int'),
#   'imagick_r': Application(538, 'imagick_r', 'fp'),
#   'leela_r': Application(541, 'leela_r', 'int'),
#   'nab_r': Application(544, 'nab_r', 'fp'),
#   'exchange2_r': Application(548, 'exchange2_r', 'int'),
#   'fotonik3d_r': Application(549, 'fotonik3d_r', 'fp'),
#   'roms_r': Application(554, 'roms_r', 'fp'),
#   'xz_r': Application(557, 'xz_r', 'int'),
#   'perlbench_s': Application(600, 'perlbench_s', 'int'),
#   'gcc_s': Application(602, 'gcc_s', 'int'),
#   'bwaves_s': Application(603, 'bwaves_s', 'fp'),
#   'mcf_s': Application(605, 'mcf_s', 'int'),
#   'cactuBSSN_s': Application(607, 'cactuBSSN_s', 'fp'),
#   'lbm_s': Application(619, 'lbm_s', 'fp'),
#   'omnetpp_s': Application(620, 'omnetpp_s', 'int'),
#   'wrf_s': Application(621, 'wrf_s', 'fp'),
#   'xalancbmk_s': Application(623, 'xalancbmk_s', 'int'),
#   'x264_s': Application(625, 'x264_s', 'int'),
#   'cam4_s': Application(627, 'cam4_s', 'fp'),
#   'pop2_s': Application(628, 'pop2_s', 'fp'),
#   'deepsjeng_s': Application(631, 'deepsjeng_s', 'int'),
#   'imagick_s': Application(638, 'imagick_s', 'fp'),
#   'leela_s': Application(641, 'leela_s', 'int'),
#   'nab_s': Application(644, 'nab_s', 'fp'),
#   'exchange2_s': Application(648, 'exchange2_s', 'int'),
#   'fotonik3d_s': Application(649, 'fotonik3d_s', 'fp'),
#   'roms_s': Application(654, 'roms_s', 'fp'),
#   'xz_s': Application(657, 'xz_s', 'int'),
#   'specrand_fs': Application(996, 'specrand_fs'),
#   'specrand_fs': Application(997, 'specrand_fr'),
#   'specrand_is': Application(998, 'specrand_is'),
#   'specrand_ir': Application(999, 'specrand_ir'),
# }

def find_application(name_or_id):
  expr = (a for a in CPU2017_APPS if a.id == name_or_id) if isinstance(name_or_id, int) \
    else (a for a in CPU2017_APPS if a.fullname == name_or_id) if '.' in name_or_id \
    else (a for a in CPU2017_APPS if a.name == name_or_id)
  return next(expr, None)


def find_similar_application(name_or_id):
  orig = find_application(name_or_id)
  return None if orig.id > 900 else find_application(orig.id + 100 if orig.id < 600 else orig.id - 100)


def load_application_input(orig):
  a = orig if os.path.exists(os.path.join(orig.dirpath, 'data')) else find_similar_application(orig.id)
  ref = 'refrate' if orig.id < 600 or not os.path.exists(os.path.join(
    a.dirpath, 'data', 'refspeed')) else 'refspeed'
  orig.data = {
    'test:': [input for input in os.listdir(os.path.join(a.dirpath, 'data', 'test', 'input'))],
    'train': [input for input in os.listdir(os.path.join(a.dirpath, 'data', 'train', 'input'))],
    'ref':   [input for input in os.listdir(os.path.join(a.dirpath, 'data', ref, 'input'))]
  }
  print(orig.fullname)
  print(orig.data)
  
  # if os.path.exists(os.path.join(app.dirpath, 'data')):
  #   print('Finded in original {}:'.format(app.fullname))
  #   ref = 'refrate' if app.id < 600 else 'refspeed'
  #   app.commands = {
  #     'test:': [input for input in os.listdir(os.path.join(app.dirpath, 'data', 'test', 'input'))],
  #     'train': [input for input in os.listdir(os.path.join(app.dirpath, 'data', 'train', 'input'))],
  #     'ref':   [input for input in os.listdir(os.path.join(app.dirpath, 'data', ref, 'input'))],
  #   }
  # else:
  #   similar = find_similar_application(app.id)
  #   if similar is not None and os.path.exists(os.path.join(similar.dirpath, 'data')):
  #     print('Finded in similar {}: {}'.format(app.fullname, similar.fullname if similar is not None else 'None'))
  #     ref = 'refspeed' if os.path.exists(os.path.join(similar.dirpath, 'data', 'refspeed')) else 'refrate'
  #     app.commands = {
  #       'test:': [input for input in os.listdir(os.path.join(similar.dirpath, 'data', 'test', 'input'))],
  #       'train': [input for input in os.listdir(os.path.join(similar.dirpath, 'data', 'train', 'input'))],
  #       'ref':   [input for input in os.listdir(os.path.join(similar.dirpath, 'data', ref, 'input'))],
  #     }
  #   else:
  #     print('{}: data not found'.format(app.fullname))


def load_application(name_or_id):
  app = find_application(name_or_id)
  for a in CPU2017_APPS:
    load_application_input(a)
  return app
  

inputmap = {
  'test': 'test',
  'train': 'train',
  'ref': 'ref',
  # small is not valid
  'large': 'train',
  'huge': 'ref',
}

def allbenchmarks():
  return [app.name for app in CPU2017_APPS]

def filter_apps(expr):
  return [app.name for app in list(filter(expr, CPU2017_APPS))]

# def allintrate():
#   return filter_apps(lambda a: a.id < 600 and a.type == 'int')

# def allintspeed():
#   return filter_apps(lambda a: a.id >= 600 and a.type == 'int')

# def allfprate():
#   return filter_apps(lambda a: a.id < 600 and a.type == 'fp')

# def allfpspeed():
#   return filter_apps(lambda a: a.id >= 600 and a.type == 'fp')

all_intrate = filter_apps(lambda a: a.id < 600 and a.type == 'int')
all_intspeed = filter_apps(lambda a: a.id >= 600 and a.type == 'int')
all_fprate = filter_apps(lambda a: a.id < 600 and a.type == 'fp')
all_fpspeed = filter_apps(lambda a: a.id >= 600 and a.type == 'fp')

def allinputs():
  return inputmap.keys()

def split_program_and_index(origprogram):
  underpos = [m.start() for m in re.finditer('_', origprogram)]
  program = origprogram if len(underpos) == 1 else origprogram + '_r' if not underpos else origprogram[:underpos[1]]
  index = origprogram[underpos[1] + 1:] if len(underpos) > 1 else '0'
  return program, index


# Convert index name to index number
def get_input_index(program, inputsize, inputname):
  load_application(program)
  return 0


def name_to_input_index(program, inputsize):
  return 0


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

    
class Program:

  def __init__(self, origprogram, nthreads, inputsize, benchmark_options = []):
    program, origindex = split_program_and_index(origprogram)
    # index = int(origindex) if str.isdigit(origindex) else get_input_index(program, inputsize, origindex) # FIXME!
    index = int(origindex)
    # TODO: Allow run multiples programs? (all, intrate, intspeed, fprate, fpspeed)
    if program not in allbenchmarks():
      raise ValueError("Invalid benchmark %s" % program)
    if inputsize not in allinputs():
      raise ValueError("Invalid input size %s" % inputsize)
    # Index of 0 always works (at least one run) # FIXME!
    # if index != 0 and index >= len(name_to_input_index(program, inputsize)):
    #   raise ValueError("Invalid program index (%s/%s)" % (origprogram, index))
    self.program = program
    self.index = index
    self.nthreads = nthreads
    self.inputsize = inputsize
    self.app = find_application(program)

  def ncores(self):
    return 0
  
  def run(self, graphitecmd, postcmd = ''):
    rc = 1 # Indicate failure if there are any problems
    origcwd = os.getcwd()
    rundir = os.path.join(self.app.dirpath, 'run', 'run_base_refrate_donuts-m64.0000')
    cmd_to_run = get_spec_cmds(rundir)[self.index]
    os.chdir(rundir)
    rc = run_bm(self.program, cmd_to_run, graphitecmd, env = '', postcmd = postcmd)
    os.chdir(origcwd)
    ### os.system('rm -rf "%s"' % rundir)
    return rc
  
  def rungraphiteoptions(self):
    return ''


def run(cmd):
  sys.stdout.flush()
  sys.stderr.flush()
  rc = os.system(cmd)
  rc >>= 8
  return rc

def run_bm(bm, cmd, submit, env, postcmd = ''):
  print('[CPU2017]', '[========== Running benchmark', bm, '==========]')
  cmd = env + ' ' + submit + ' ' + cmd + ' ' + postcmd
  print('[CPU2017]', 'Running \'' + cmd + '\':')
  print('[CPU2017]', '[---------- Beginning of output ----------]')
  rc = run(cmd)
  print('[CPU2017]', '[----------    End of output    ----------]')
  print('[CPU2017]', 'Done.')
  return rc
