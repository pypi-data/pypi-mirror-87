from pathlib import Path

import markipy as mpy

DEFAULT_PKG_INSTALLED_PATH = Path(mpy.__file__).parent
DEFAULT_DATA_PATH = DEFAULT_PKG_INSTALLED_PATH / 'nn' / 'data'

from . import commons
from . import gans  
