from pathlib import Path
from os import makedirs

# DEFAULT PACKAGE FOLDER
DEFAULT_PACKAGE_FOLDER = Path().home() / '.markipy'
DEFAULT_LOG_PATH = DEFAULT_PACKAGE_FOLDER / 'logs'

if not DEFAULT_LOG_PATH.exists():
    makedirs(DEFAULT_LOG_PATH, exist_ok=True)

from . import basic
from . import script
from . import gui
