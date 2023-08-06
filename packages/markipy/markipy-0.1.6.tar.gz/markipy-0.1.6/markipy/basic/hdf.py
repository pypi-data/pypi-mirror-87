import pandas as pd

from .perf import Performance
from .filesystem import File


class Hdf(File):

    @Performance.collect
    def read(self, key=None):
        self.log.debug("Reading hdf.")
        if self.exist():
            if key:
                return pd.read_hdf(self.__file__, key=key)
            else:
                return pd.read_hdf(self.__file__)
        else:
            return None

    @Performance.collect
    def save(self, key, dataframe):
        self.log.debug("Saving hdf.")
        mode = 'a' if self.exist() else 'w'
        dataframe.to_hdf(self.__file__.absolute(), key=key, mode=mode)

    @Performance.collect
    def keys(self):
        self.log.debug("Asking keys hdf.")
        with pd.HDFStore(self.__file__) as hdf:
            return hdf.keys()
