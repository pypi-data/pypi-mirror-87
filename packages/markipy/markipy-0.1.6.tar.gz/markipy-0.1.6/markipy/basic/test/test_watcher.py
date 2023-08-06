import unittest
import os
from time import sleep
import HtmlTestRunner

from markipy.basic import File
from markipy.basic import Watcher

_watcher_child_ = {'class': 'WatcherChild', 'version': 1}
_watcher_nephew_ = {'class': 'WatcherNephew', 'version': 1}


class WatcherChild(Watcher):
    def __init__(self, path='/tmp/watcher_child_test'):
        Watcher.__init__(self, console=False, path=path)
        self._init_atom_register_class(_watcher_child_)
        self.file_has_created = False
        self.file_has_modified = False
    
    def task_file_created(self, event):
        self.file_has_created = True

    def task_file_modified(self, event):
        self.file_has_modified = True


class WatcherNephew(WatcherChild):
    def __init__(self, path='/tmp/watcher_nephew_test'):
        WatcherChild.__init__(self, path=path)
        self._init_atom_register_class(_watcher_nephew_)


class TestWatcher(unittest.TestCase):

    def test_file_created_watcher(self):
        File('/tmp/file_to_watch').remove()
        wf = WatcherChild('/tmp/file_to_watch')
        wf.start()
        
        File('/tmp/file_to_watch').write('Init')
        sleep(0.01)

        self.assertEqual(True, wf.file_has_created)

    def test_file_modified_watcher(self):
        wf = WatcherChild('/tmp/file_to_watch')
        wf.start()
        
        File('/tmp/file_to_watch').append('Modified')
        sleep(0.01)

        self.assertEqual(True, wf.file_has_modified)

    def test_folder_watcher(self):
        pass



if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='/tmp/markpy_unittest/'))
