from .atom import Atom
from .logger import Logger
from .perf import Performance
from markipy import DEFAULT_LOG_PATH

import os
from shutil import rmtree
from pathlib import Path

_file_ = {'class': 'File', 'version': 3}
_folder_ = {'class': 'Folder', 'version': 3}


class File(Logger):

    def __init__(self, file_path, console=False, log_path=DEFAULT_LOG_PATH, auto_create=True):
        Logger.__init__(self, console=console, file_log=f'File{file_path}', log_path=log_path)
        self._init_atom_register_class(_file_)

        self.__file__ = Path(file_path)

        status = self._check_input(auto_create)

        attach_mode = self._attach(status)

        self.log.debug(f' File {attach_mode} -> {self.violet(self.__file__)}')

    @Performance.collect
    def _init(self):
        with open(self.__file__, 'w') as fd:
            fd.write('')

    @Performance.collect
    def _check_input(self, auto_create):

        if self.__file__.is_dir():
            raise FileAttacheToFolder(self)

        if not self.__file__.parent.exists():
            if auto_create:
                return ["init_parent", "init_file"]
            else:
                raise ParentPathExceptionNoFlagOnAutoFolderCreation(self)

        if not self.__file__.exists():
            if auto_create:
                return ["init_file"]
            else:
                raise PathDoesNotExistNoFlagOnAutoCreateException(self)

        return ["ok"]

    @Performance.collect
    def _attach(self, mode):
        return_code = []
        if 'ok' in mode:
            return_code += [self.orange('already-exist')]

        if 'init_parent' in mode:
            self.make_parent()
            return_code += [self.green('init-parent')]

        if 'init_file' in mode:
            self._init()
            return_code += [self.green('init-file')]
        else:
            return_code += [self.red('not-exist')]

        return return_code

    @Performance.collect
    def make_parent(self):
        os.makedirs(self.folder(), exist_ok=True)

    @Performance.collect
    def folder(self):
        return self.__file__.parent

    def __str__(self):
        return str(self.__file__).strip()

    def exist(self):
        return self.__file__.exists()

    @Performance.collect
    def read(self):
        with open(self.__file__, 'r') as f:
            return f.read()

    @Performance.collect
    def write(self, data):
        with open(self.__file__, 'w') as f:
            return f.write(str(data))

    def read_fd(self):
        return open(self.__file__, 'r')

    def write_fd(self):
        return open(self.__file__, 'w')

    def append(self, data):
        with open(self.__file__, 'a') as f:
            return f.write(str(data))

    def remove(self):
        os.remove(self.__file__)

    def relative(self, old_path, new_path):
        return Path(new_path) / Path(self.__file__).relative_to(Path(old_path))

    def __call__(self):
        return self.__file__


class Folder(Logger):

    def __init__(self, folder_path='./', console=False, log_path=DEFAULT_LOG_PATH, auto_create=True):
        Logger.__init__(self, console=console, file_log=f'Folder{folder_path}', log_path=log_path)
        Atom.__init__(self, _folder_['class'], _folder_['version'])

        self.__folder__ = Path(folder_path)

        status = self._check_input(auto_create)

        attach_mode = self._attach(status)

        self.log.debug(f' Folder {attach_mode} -> {self.lightviolet(self.__folder__)}')

    @Performance.collect
    def _init(self):
        os.makedirs(self.__folder__, exist_ok=True)

    @Performance.collect
    def _check_input(self, auto_create):

        if self.__folder__.is_file():
            raise FolderAttachedToFileException(self)

        if not self.__folder__.parent.exists():
            if auto_create:
                return ["init_parent", "init_folder"]
            else:
                raise ParentPathExceptionNoFlagOnAutoFolderCreation(self)

        if not self.__folder__.exists():
            if auto_create:
                return ["init_folder"]
            else:
                raise PathDoesNotExistNoFlagOnAutoCreateException(self)

        return ["ok"]

    @Performance.collect
    def _attach(self, mode):
        return_code = []
        if 'ok' in mode:
            return_code += [self.orange('already-exist')]

        if 'init_parent' in mode:
            os.makedirs(self.__folder__.parent, exist_ok=True)
            return_code += [self.green('init-parent')]

        if 'init_file' in mode:
            self._init()
            return_code += [self.green('init-file')]
        else:
            return_code += [self.red('not-exist')]

        return return_code

    @Performance.collect
    def folders(self):
        self.log.debug("call list_folder")
        return [x for x in self.__folder__.iterdir() if x.is_dir()]

    @Performance.collect
    def files(self):
        self.log.debug("call list_files")
        return [x for x in self.__folder__.iterdir() if x.is_file()]

    @Performance.collect
    def ls(self):
        self.log.debug("call ls")
        return [x for x in self.__folder__.iterdir()]

    def walk(self):
        for root, subdirs, files in os.walk(self.__folder__):
            yield root, subdirs, files

    @Performance.collect
    def delete(self, target=None):
        if target is None:
            target = self.__folder__
        self.log.debug(f"call delete_folder on:\t{target}")
        rmtree(target)

    @Performance.collect
    def remove(self, target):
        self.log.debug(f"call delete_file on:\t{target}")
        os.remove(target)

    @Performance.collect
    def empty_folder(self):
        self.log.debug("call empty_folder")
        for folder in self.folders():
            self.delete(folder)
        for file in self.files():
            self.remove(file)

    def get_file(self, file):
        if Path(file) in self.files():
            return File(file)

    def __str__(self):
        return str(self.__folder__)

    def __call__(self):
        return self.__folder__


# ParentPathCreationNewFileNotFound
class ParentPathExceptionNoFlagOnAutoFolderCreation(Exception):
    def __init__(self, FilesystemClass):
        if isinstance(FilesystemClass, File):
            FilesystemClass.log.error(f"Parent path not exist of  {FilesystemClass.red(FilesystemClass.__file__)}")
        else:
            FilesystemClass.log.error(f"Parent path not exist of  {FilesystemClass.red(FilesystemClass.__folder__)}")


class PathDoesNotExistNoFlagOnAutoCreateException(Exception):
    def __init__(self, FilesystemClass):
        if isinstance(FilesystemClass, File):
            FilesystemClass.log.error(f"File path not exist of  {FilesystemClass.red(FilesystemClass.__file__)}")
        else:
            FilesystemClass.log.error(f"Folder path not exist of  {FilesystemClass.red(FilesystemClass.__folder__)}")


class FileAttacheToFolder(Exception):
    def __init__(self, File):
        File.log.error(f"File cannot be attached to a folder: {File.red(File.__file__)}")


class FolderAttachedToFileException(Exception):
    def __init__(self, Folder):
        Folder.log.error(f"Folder cannot be attached to a file: {Folder.red(Folder.__folder__)}")
