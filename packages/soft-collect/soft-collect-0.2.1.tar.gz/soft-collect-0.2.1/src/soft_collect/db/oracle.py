import logging

import cx_Oracle

from .abstract import Abstract_DB
from soft_collect.config import settings as s

logger = logging.getLogger(__name__)


class Oracle(Abstract_DB):
    def select(self, sql):
        with self.set_up_connection() as conn:
            c = conn.cursor()
            yield from c.execute(sql)

    def fetch_all(self, sql):
        with self.set_up_connection() as conn:
            c = conn.cursor()
            return c.execute(sql).fetchall()

    def set_up_connection(self, _retry=2):
        logger.info(f"Creating connection to SQL Server in {s.ip}")

        try:
            connection = cx_Oracle.connect(
                s.user,
                s.password,
                f"{s.ip}/{s.base}",
                encoding="UTF-8",
                nencoding="UTF-8",
            )
        except cx_Oracle.DatabaseError as e:
            logger.error(f"Can't set up a connection with {s.ip}/{s.base}, {e}")
            if _retry:
                return self.set_up_connection(_retry - 1)
            raise e

        return connection
