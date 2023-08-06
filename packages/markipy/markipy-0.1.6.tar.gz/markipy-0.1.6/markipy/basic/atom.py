import time
from random import random
from dataclasses import dataclass

from .time import datetime, clock
from .perf import Performance

_atom_ = {'class': 'Atom', 'version': 3}


class ClassDetails:
    def __init__(self, name, version):
        self.name = name
        self.version = version
        self.creation_date = datetime()
        self.creation_time = clock()
        self.destruction_date: datetime = None
        self.was_init = False
        self.rand_id = random()
        
    def __eq__(self, other):
        return self.version == other.version and self.creation_date == other.creation_date and self.creation_time == other.creation_time

    def __hash__(self):
        return hash((self.name, self.version, self.creation_time, self.rand_id))

    def init(self):
        self.was_init = True


class AtomHistory:

    def __init__(self, name, version):
        class_details = ClassDetails(name=name, version=version)
        self.classes = {name: class_details}
        self.classes_history_hash = [self.__hash__()]

    def __eq__(self, other):
        return self.classes == other.classes

    def __hash__(self):
        _hashes = []
        for atom in self.classes:
            _hashes += [hash(self.classes[atom])]
        return hash(tuple(_hashes))

    def add(self, name, version):
        self.classes[name] = ClassDetails(name=name, version=version)
        self.classes_history_hash.append(self.__hash__())

    def show(self):
        return str(self.classes), str(self.classes_history_hash)

    def get_names(self):
        return list(self.classes.keys())

    def get_versions(self):
        return [v.version for k, v in self.classes.items()]

    def set_class_init(self, name):
        self.classes[name].init()

    def __call__(self, name):
        return self.classes[name]


class Atom:

    performance = Performance()

    def __init__(self, name, version):
        if not hasattr(self, '_history'):
            self._history = AtomHistory(name=_atom_['class'], version=_atom_['version'])
            self._history.add(name=name, version=version)
        else:
            self._history.add(name=name, version=version)

    def _get_classes_history(self):
        return self._history

    def _get_class_details(self, name):
        return self._history(name)

    def _get_classes_name_list(self):
        return self._history.get_names()

    def _get_classes_versions_list(self):
        return self._history.get_versions()

    def _get_classes_name_str(self):
        return '.'.join(self._get_classes_name_list())

    def _get_classes_versions_str(self):
        return '.'.join([str(v) for v in self._get_classes_versions_list()])

    def _show_classes_history(self):
        return self._history.show()

    def _get_classes_hash(self):
        return hash(self._history)

    def __hash__(self):
        return hash(self._history)
