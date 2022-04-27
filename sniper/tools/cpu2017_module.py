import os, sys, errno

abspath = lambda d: os.path.abspath(os.path.join(d))

HOME = abspath(os.path.dirname(__file__))

postfix = 'donuts-m64.0000'

inputmap = {
  'test': 'test',
  'train': 'train',
  'ref': 'ref',
  # small is not valid
  'large': 'train',
  'huge': 'ref',
}

def allinputs():
  return inputmap.keys()


class Application:

  def __init__(self, id, name, type=None):
    self.id = id
    self.name = name
    self.type = type
    self.fullname = '{}.{}'.format(id, name)
    self.dirpath = os.path.join(HOME, self.fullname)
    
  def get_rundir_path(self, inputsize, tune='base'):
    if inputsize == 'ref':
      inputsize = 'refrate' if self.id < 600 else 'refspeed'
    return os.path.join(self.dirpath, 'run', 'run_{}_{}_{}'.format(tune, inputsize, postfix))

  def get_cmd(self, inputsize, index=None, tune='base'):
    cmds = get_spec_cmds(self.get_rundir_path(inputsize, tune))
    return cmds[index] if index is not None else cmds
    

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


def get_app(name_or_id):
  expr = (a for a in CPU2017_APPS if a.id == name_or_id) if isinstance(name_or_id, int) \
    else (a for a in CPU2017_APPS if a.fullname == name_or_id) if '.' in name_or_id \
    else (a for a in CPU2017_APPS if a.name == name_or_id)
  return next(expr, None)


def get_similar_app(name_or_id):
  orig = get_app(name_or_id)
  return None if orig.id > 900 else get_app(orig.id + 100 if orig.id < 600 else orig.id - 100)


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


def split_program_and_index(origprogram):
  args = origprogram.split('_')
  if len(args) == 1:
    program, index = origprogram, None
  elif str.isdigit(args[0]) or str.isdigit(args[1]):
    args = origprogram.split('_', 1)
    program, index = args[0], args[1]
  else:
    args = origprogram.split('_', 2)
    program, index = args[0] + '_' + args[1], args[2] if len(args) > 2 else None
  if index:
    if '_' in index:
      raise ValueError("Invalid number of arguments. Use <program name or id>_<index>")
    elif not str.isdigit(index):
      raise ValueError("Invalid value to program index ('%s' is not integer)" % index)
  program = int(program) if str.isdigit(program) else program + '_r' if program and not '_' in program else program
  index = int(index) if index else 0
  return program, index

  # args = origprogram.split('_')
  # argc = len(args)
  # if argc == 1:
  #   program = int(args[0]) if str.isdigit(args[0]) else origprogram + '_r'
  #   index = 0
  # elif argc == 2:
  #   if str.isdigit(args[0]):
  #     if not str.isdigit(args[1]):
  #       raise ValueError("Invalid value to program index ('%s' is not integer)" % args[1])
  #     program = int(args[0])
  #     index = int(args[1])
  #   else:
  #     program = origprogram if not str.isdigit(args[1]) else int(args[0]) if str.isdigit(args[0]) else args[0] + '_r'
  #     index = int(args[1]) if str.isdigit(args[1]) else 0
  # elif argc == 3:
  #   if not str.isdigit(args[2]):
  #     raise ValueError("Invalid value to program index ('%s' is not integer)" % args[2])
  #   program = args[0] + '_' + args[1]
  #   index = int(args[2])
  # else:
  #   raise ValueError("Invalid number of arguments (%s, max=3)" % argc)
  # return program, index
  
  # underpos = [m.start() for m in re.finditer('_', origprogram)]
  # program = origprogram if len(underpos) == 1 else origprogram + '_r' if not underpos else origprogram[:underpos[1]]
  # index = origprogram[underpos[1] + 1:] if len(underpos) > 1 else '0'  


class Program:
    
  def __init__(self, origprogram, nthreads, inputsize, benchmark_options = []):
    program, index = split_program_and_index(origprogram)
    app = get_app(program)
    if not app:
      raise ValueError("Invalid benchmark %s" % program)
    if inputsize not in allinputs():
      raise ValueError("Invalid input size %s" % inputsize)
    if index < 0 or index >= len(app.get_cmd(inputsize)):
      raise ValueError("Invalid program index (%s/%s)" % (origprogram, index))
    self.program = program
    self.index = index
    self.nthreads = nthreads
    self.inputsize = inputsize
    self.app = app

  def ncores(self):
    return self.nthreads
  
  def run(self, graphitecmd, postcmd = ''):
    # TODO: Use temp folder to run
    origcwd = os.getcwd()
    cmd_to_run = self.app.get_cmd(self.inputsize, self.index)
    os.chdir(self.app.get_rundir_path(self.inputsize))
    rc = run_bm(self.program, cmd_to_run, graphitecmd, env = '', postcmd = postcmd)
    os.chdir(origcwd)
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