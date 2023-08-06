import yaml

from .filesystem import File


class Yaml(File):

    def load(self):
        if self.exist():
            with open(self.__file__, 'r') as fd:
                return yaml.safe_load(fd)
        else:
            return None