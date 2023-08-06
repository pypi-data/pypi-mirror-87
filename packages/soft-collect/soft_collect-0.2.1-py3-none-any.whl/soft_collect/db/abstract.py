import logging
from abc import ABC
from abc import abstractmethod

from soft_collect.config import settings

logger = logging.getLogger(__name__)


def get_sql(sql):
    if sql[-4:] == ".sql":
        with open(sql, encoding="utf8", errors="ignore") as f:
            return f.read()
    return sql


class Abstract_DB(ABC):
    def __init__(self):
        print("Connecting to DB...")
        self.set_up_connection()
        print("Connected to DB")

    @abstractmethod
    def set_up_connection(self, _retry=2):
        pass

    @abstractmethod
    def select(self, sql):
        pass

    @abstractmethod
    def fetch_all(self, sql):
        pass

    def get_rows(self, query, format):
        logger.info(f"Getting rows {format}")
        sql = get_sql(query).format(**format)
        return self.fetch_all(sql)

    def get_objects(self, key):
        logger.info(f"Getting objects for key {key}")
        sql = get_sql(settings.objs_sql).format(KEY=key)
        yield from self.select(sql)
