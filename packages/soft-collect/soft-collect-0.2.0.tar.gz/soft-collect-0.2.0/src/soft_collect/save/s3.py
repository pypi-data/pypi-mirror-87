import io
import logging

import botocore
import pandas as pd
from tucuxi import Session

from .abstract import AbstractSaveHandler
from soft_collect.config import settings

logger = logging.getLogger(__name__)


class S3SaveHandler(AbstractSaveHandler):
    def __init__(self):
        super().__init__()
        logger.info(f"Connecting to AWS S3 Bucket {settings.bucket}")
        proxy = settings.get("proxy", None)
        if proxy:
            logger.info(f"Using proxy for S3 connection. Proxy: {settings.proxy}")
        sess = Session(settings.access_key, settings.secret_access_key,)
        self.s3 = sess.s3(
            settings.bucket,
            config=botocore.client.Config(proxies=proxy, max_pool_connections=1000),
        )

    def write_file(self, dirname, filename, obj):
        key = dirname + filename
        self.s3.set_object(key, obj)

    def exists(self, prefix):
        return bool(list(self.s3.list_objects(prefix)))

    def get_file(self, filepath):
        if filepath[-3:] == "csv":
            csv = io.BytesIO(self.s3.get_object(filepath))
            return pd.read_csv(csv)
        return {}
