import logging
from abc import ABC
from abc import abstractmethod

from pandas.errors import EmptyDataError

from soft_collect.config import settings

logger = logging.getLogger(__name__)


class AbstractSaveHandler(ABC):
    def __init__(self):
        s = settings
        self.dir = f"{s.alias}/{s.grau}/{s.base}"

    @abstractmethod
    def write_file(self, dirname, filename, obj):
        pass

    @abstractmethod
    def exists(self, filepath):
        pass

    @abstractmethod
    def get_file(self, filepath):
        pass

    def save_obj(self, obj, cdclass, key, part):
        pdf_dir = f"{self.dir}/{cdclass}/"  # TODO Check if pdf
        filename = f"{key}_1/{part}.pdf"
        logger.info(f"Saving {filename}")
        self.write_file(pdf_dir, filename, obj)

    def save_meta(self, df, filename):
        meta_dir = f"{self.dir}/meta/"
        filename = f"{filename}.csv"
        obj = df.to_csv(index=False)
        logger.info(f"Saving {filename}")
        self.write_file(meta_dir, filename, obj)

    def check_obj(self, cdclass, key):
        filepath = f"{self.dir}/{cdclass}/{key}"
        logger.info(f"Checking if {filepath} exists")
        return self.exists(filepath)

    def check_meta(self, filename, return_obj=True):
        filepath = f"{self.dir}/meta/{filename}.csv"
        logger.info(f"Checking if {filepath} exists")
        res = self.exists(filepath)
        if return_obj:
            try:
                obj = self.get_file(filepath) if res else None
            except EmptyDataError:
                logger.error(f"The file {filepath} is empty")
                res = False
                obj = None
            return (res, obj)
        return res
