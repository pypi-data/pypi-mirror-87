import logging

import pyodbc

from .abstract import Abstract_DB
from soft_collect.config import settings as s

logger = logging.getLogger(__name__)


class SQLServer(Abstract_DB):
    def select(self, sql):
        with self.set_up_connection() as conn:
            c = conn.cursor()
            c.execute(sql)
            row = c.fetchone()
            while row:
                yield row
                row = c.fetchone()

    def fetch_all(self, sql):
        with self.set_up_connection() as conn:
            c = conn.cursor()
            return c.execute(sql).fetchall()

    def set_up_connection(self, _retry=2):
        logger.info(f"Creating connection to SQL Server in {s.ip}")

        pyodbc_drivers = [dri for dri in pyodbc.drivers() if "SQL Server" in dri]
        if pyodbc_drivers:
            driver = pyodbc_drivers[0]
        else:
            raise Exception("No SQL Server Driver found, please install it.")

        credentials_kargs = {}
        if s.get("USER", None):
            credentials_kargs = {"user": s.user, "password": s.passowrd}
        try:
            connection = pyodbc.connect(
                "Trusted_Connection=yes",
                driver="{" + driver + "}",
                server=s.ip,
                database=s.base,
                **credentials_kargs,
            )
        except BaseException as e:
            logger.error(f"Can't set up a connection with {s.ip}/{s.base}, {e}")
            if _retry:
                return self.set_up_connection(_retry - 1)
            raise e

        return connection
