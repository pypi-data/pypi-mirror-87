import unittest
import os
import HtmlTestRunner

from markipy.basic import Atom
from markipy.basic import File, Folder


_File_child_ = {'class': 'FileChild', 'version': 2}
_File_nephew_ = {'class': 'FileNephew', 'version': 3}


class FileChild(File):
    def __init__(self, console=False, file_path='/tmp/file_child_test'):
        File.__init__(self, console=console, file_path=file_path)
        self._init_atom_register_class(_File_child_)


class FileNephew(FileChild):
    def __init__(self, console=False, file_path='/tmp/file_nephew_test'):
        FileChild.__init__(self, console=console, file_path=file_path)
        self._init_atom_register_class(_File_nephew_)

class TestFile(unittest.TestCase):

    def test_file_child(self):
        fc = FileChild(file_path='/tmp/file_child_test')
        self.assertEqual(os.path.exists('/tmp/file_child_test'), True)
        
    def test_file_nephew(self):
        fn = FileNephew(file_path='/tmp/file_nephew_test')
        self.assertEqual(os.path.exists('/tmp/file_nephew_test'), True)


_Folder_child_ = {'class': 'FolderChild', 'version': 2}
_Folder_nephew_ = {'class': 'FolderNephew', 'version': 3}


class FolderChild(Folder):
    def __init__(self, console=False, folder_path='/tmp/Folder_child_test'):
        Folder.__init__(self, console=console, folder_path=folder_path)
        self._init_atom_register_class(_Folder_child_)


class FolderNephew(FolderChild):
    def __init__(self, console=False, folder_path='/tmp/Folder_nephew_test'):
        FolderChild.__init__(self, console=console, folder_path=folder_path)
        self._init_atom_register_class(_Folder_nephew_)

class TestFolder(unittest.TestCase):

    def test_performance_child(self):
        fc = FolderChild(folder_path='/tmp/Folder_child_test')
        self.assertEqual(os.path.exists('/tmp/Folder_child_test'), True)
        
        
    def test_performance_nephew(self):
        fn = FolderNephew(folder_path='/tmp/Folder_nephew_test')
        self.assertEqual(os.path.exists('/tmp/Folder_nephew_test'), True)




if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='/tmp/markpy_unittest/'))
