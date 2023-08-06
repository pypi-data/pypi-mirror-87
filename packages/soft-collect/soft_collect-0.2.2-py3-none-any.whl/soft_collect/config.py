import logging

from dynaconf import Dynaconf
from dynaconf import Validator

root = logging.getLogger()
filename = "soft-collect.log"
file_handler = logging.FileHandler(filename=filename)

formatter = logging.Formatter(
    "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
)

file_handler.setFormatter(formatter)

root.setLevel(logging.INFO)
root.addHandler(file_handler)
root.propagate = False

logger = logging.getLogger(__name__)

settings = Dynaconf(
    envvar_prefix="DYNACONF", settings_files=["settings.toml", ".secrets.toml"],
)


def validate_db():
    logger.info("Validating DB variables")
    v = [
        Validator("DBM", must_exist=True),
        Validator("IP", must_exist=True),
        Validator("BASE", must_exist=True),
    ]
    validate(v)


def validate_collect():
    logger.info("Validating Collect variables")
    v = [
        Validator("ALIAS", must_exist=True),
        Validator("GRAU", len_eq=2, must_exist=True),
        Validator("OBJS_SQL", "KEYS_SQL", must_exist=True),
    ]
    validate(v)


def validate_s3():
    logger.info("Validating S3 variables")
    v = [
        Validator("ACCESS_KEY", must_exist=True),
        Validator("SECRET_ACCESS_KEY", must_exist=True),
        Validator("BUCKET", must_exist=True),
    ]
    validate(v)


def validate(v):
    settings.validators.register(*v)
    settings.validators.validate()
