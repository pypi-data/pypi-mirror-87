from pathlib import Path
from watchdog.events import FileSystemEventHandler
from watchdog.events import FileMovedEvent, DirMovedEvent
from watchdog.events import FileModifiedEvent, DirModifiedEvent
from watchdog.events import FileCreatedEvent, DirCreatedEvent
from watchdog.events import FileDeletedEvent, DirDeletedEvent
from watchdog.observers import Observer
from pathlib import Path

from markipy import DEFAULT_LOG_PATH
from .logger import Logger, Performance
from .filesystem import File, Folder

_watcher_ = {'class': 'Watcher', 'version': 3}


class Watcher(Logger, FileSystemEventHandler):

    def __init__(self, path=Path.cwd(), console=False, recursive=False, log_path=DEFAULT_LOG_PATH):
        FileSystemEventHandler.__init__(self)

        if Path(path).is_dir():
            path = Path(path)
            self.target_file = None
            log_file = f'FolderWatcher.{path}'
        else:
            self.target_file = Path(path)
            path = Path(path).parent
            log_file = f'FileWatcher.{path}'

        self.path = path
        self.recursive = recursive

        Logger.__init__(self, console=console, file_log=log_file, log_path=log_path)
        self._init_atom_register_class(_watcher_)

    def start(self):
        self.observer_thread = Observer()
        self.observer_thread.schedule(self, path=self.path, recursive=self.recursive)
        self.observer_thread.start()

        self.log.debug(f'Filesystem observer point to: {self.cyan(self.path)}')
        if self.target_file:
            self.log.debug(f'Target file: {self.cyan(self.target_file)}')

    def __del__(self):
        self.observer_thread.stop()
        self.observer_thread.join()

    def dispatch(self, event):
        if self.target_file is not None:
            self.dispatch_file(event)
        else:
            self.dispatch_folder(event)

    def dispatch_file(self, event):
        if event.src_path == str(self.target_file):
            if isinstance(event, FileMovedEvent):
                self.task_file_moved(event)
            if isinstance(event, FileModifiedEvent):
                self.task_file_modified(event)
            if isinstance(event, FileCreatedEvent):
                self.task_file_created(event)
            if isinstance(event, FileDeletedEvent):
                self.task_file_deleted(event)

    def dispatch_folder(self, event):
        if isinstance(event, FileMovedEvent):
            self.task_file_moved(event)
        if isinstance(event, FileModifiedEvent):
            self.task_file_modified(event)
        if isinstance(event, FileCreatedEvent):
            self.task_file_created(event)
        if isinstance(event, FileDeletedEvent):
            self.task_file_deleted(event)
        if isinstance(event, DirMovedEvent):
            self.task_dir_moved(event)
        if isinstance(event, DirModifiedEvent):
            self.task_dir_modified(event)
        if isinstance(event, DirCreatedEvent):
            self.task_dir_created(event)
        if isinstance(event, DirDeletedEvent):
            self.task_dir_deleted(event)

    def task_file_moved(self, event):
        self.log.debug(f'File moved from {self.orange(event.src_path)} to {self.green(event.dest_path)}')

    def task_file_modified(self, event):
        self.log.debug(f'File modified {self.orange(event.src_path)}')

    def task_file_created(self, event):
        self.log.debug(f'File created {self.green(event.src_path)}')

    def task_file_deleted(self, event):
        self.log.debug(f'File deleted {self.red(event.src_path)}')

    def task_dir_moved(self, event):
        self.log.debug(f'Folder moved from {self.orange(event.src_path)} to {self.green(event.dest_path)}')

    def task_dir_modified(self, event):
        self.log.debug(f'Folder modified {self.orange(event.src_path)}')

    def task_dir_created(self, event):
        self.log.debug(f'Folder created {self.green(event.src_path)}')

    def task_dir_deleted(self, event):
        self.log.debug(f'Folder deleted {self.red(event.src_path)}')
