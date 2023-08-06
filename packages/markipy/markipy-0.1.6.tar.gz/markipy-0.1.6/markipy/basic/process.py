from pathlib import Path
from threading import Thread
from subprocess import PIPE, Popen
from time import sleep
from markipy import DEFAULT_LOG_PATH
from .perf import Performance
from .logger import Logger

_process_ = {'class': 'Process', 'version': 4}


class Process(Logger):

    def __init__(self, cmd=None, console=False, file_log='Process', log_path=DEFAULT_LOG_PATH):
        Logger.__init__(self, console=console, file_log=file_log, log_path=log_path)
        self._init_atom_register_class(_process_)
        self.proc = None
        self.loop = True
        self.cmd = cmd

    def _clean_out_line(self, line):
        return str(line).replace('\r', '').replace('\n', '')

    def _read_stream(self, stream, cb):
        while True:
            line = stream.readline()
            if line:
                cb(self._clean_out_line(line))
            else:
                break
            sleep(0.005)

    def _stream_subprocess(self, cmd):
        process = Popen(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        self.loop = True
        t_out = Thread(target=self._read_stream, args=(process.stdout, self.stdout_callback))
        t_err = Thread(target=self._read_stream, args=(process.stderr, self.stderr_callback))
        t_out.start()
        t_err.start()
        status = process.wait()
        self.loop = False
        t_out.join()
        t_err.join()
        return status

    def stdout_callback(self, line):
        self.log.debug(line)

    def stderr_callback(self, line):
        self.log.error(line)

    @Performance.collect
    def execute(self, cmd):
        self.log.debug(f'Process executing: {self.cyan(cmd)}')
        rc = self._stream_subprocess(cmd)
        return rc

    def start(self):
        if self.cmd:
            self.execute(self.cmd)
