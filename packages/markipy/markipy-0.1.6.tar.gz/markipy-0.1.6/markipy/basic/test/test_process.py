import unittest
import HtmlTestRunner

from markipy.basic import AsyncProcess

_process_ps_ = {'class': 'ProcessPS', 'version': 1}


class PS(AsyncProcess):
    def __init__(self, cmd):
        AsyncProcess.__init__(self, cmd=cmd, file_log='Unittest.PS')
        self._init_atom_register_class(_process_ps_)
        self.ps = []

    def stdout_callback(self, line):
        self.ps.append(line)


class TestProcess(unittest.TestCase):

    def test_process(self):
        p = AsyncProcess('Unittest')
        p.execute(['ls', '-ashu'])

    def test_custom_process(self):
        ps_cmd = ['ps', '-aux']
        ps = PS(cmd=ps_cmd)
        ps.start()
        ps.log.debug(ps.ps)


if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='/tmp/markpy_unittest/'))
