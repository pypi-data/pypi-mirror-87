from .local import LocalSaveHandler
from .s3 import S3SaveHandler

SUPPORTED_SAVES = {"local": LocalSaveHandler, "S3": S3SaveHandler}


def get_save_client(where, *args, **kwargs):
    return SUPPORTED_SAVES[where](*args, **kwargs)
