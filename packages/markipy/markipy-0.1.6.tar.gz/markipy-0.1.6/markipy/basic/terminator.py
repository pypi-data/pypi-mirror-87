import subprocess

from markipy import DEFAULT_LOG_PATH
from .logger import Logger
from .perf import Performance

_terminator_ = {'class': 'Terminator', 'version': 1}


class Terminator(Logger):
    def __init__(self, console=False, x=0, y=0, w=500, h=350, no_border=False):
        Logger.__init__(self, console=console, file_log='Terminator', log_path=DEFAULT_LOG_PATH)
        self._init_atom_register_class(_terminator_)
        self.geometry = "--geometry " + str(w) + "x" + str(h) + "+" + str(x) + "+" + str(y)
        self.shell_init = " -e \"bash -c '"
        if no_border:
            self.geometry = "-b " + self.geometry

    @Performance.collect
    def run_process(self, user_cmd):
        cmd = ["terminator " + self.geometry + self.shell_init + str(user_cmd) + "'\""]
        self.log.debug(f'Running cmd: {self.lightblue(user_cmd)}')
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        proc.wait()
        self.log.debug('Finish')
