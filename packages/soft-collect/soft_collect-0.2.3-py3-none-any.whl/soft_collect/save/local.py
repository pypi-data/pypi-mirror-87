import logging
from glob import glob
from pathlib import Path

import pandas as pd

from .abstract import AbstractSaveHandler

logger = logging.getLogger(__name__)


def make_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


class LocalSaveHandler(AbstractSaveHandler):
    def __init__(self):
        super().__init__()
        logger.info("Using local to save results")
        self.dir = "data/" + self.dir

    def write_file(self, dirname, filename, obj):
        make_dir(dirname)
        mode = "w" if isinstance(obj, str) else "wb"
        with open(dirname + filename, mode) as f:
            f.write(obj)

    def exists(self, filepath):
        return len(glob(f"{filepath}*")) > 0

    def get_file(self, filepath):
        if filepath[-3:] == "csv":
            return pd.read_csv(filepath)
        return {}
