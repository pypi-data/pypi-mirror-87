import asyncio
import logging
from shutil import copyfile

import click
import pandas as pd

from .collect import Collect
from .config import settings as s
from .config import validate_collect
from .config import validate_db
from .config import validate_s3
from .query import Query
from .templates import secr_template
from .templates import sett_template

logger = logging.getLogger(__name__)


def load_sett_files(settings, secrets):
    if settings:
        logger.info(f"Loading settings file from {settings}")
        s.load_file(path=settings)
    if secrets:
        logger.info(f"Loading secrets file from {secrets}")
        s.load_file(path=secrets)


@click.group()
def cli():
    pass


@cli.command(help="Create template for settings and secrets files")
@click.argument("name")
def init(name):
    logger.info(f"Creating {name}-settings.toml file")
    copyfile(sett_template, f"{name}-settings.toml")
    logger.info(f"Creating {name}.secrets.toml")
    copyfile(secr_template, f"{name}.secrets.toml")
    logger.info("Successful init command")


@cli.command(help="Run a arbitrary query and save results in a .csv")
@click.argument("sql")
@click.option(
    "--name",
    default="result.csv",
    help="Filename for saving results, if not passed default is result.csv",
)
@click.option(
    "--settings",
    default=None,
    help="Path for settings file, if not passed default is settings.toml",
)
@click.option(
    "--secrets",
    default=None,
    help="Path for .secrets file, if not passed default is .secrets.toml",
)
@click.option(
    "--save",
    type=click.Choice(["S3", "local"], case_sensitive=False),
    default="local",
    help="Choose where to save files. If not passed default is local",
)
def query(sql, name, settings, secrets, save):
    load_sett_files(settings, secrets)

    validate_db()
    q = Query(save)
    q.run(sql, name)
    logger.info("Successful query command")


@cli.command(help="Collect files from a database.")
@click.option(
    "--settings",
    default=None,
    help="Path for settings file, if not passed default is settings.toml",
)
@click.option(
    "--secrets",
    default=None,
    help="Path for .secrets file, if not passed default is .secrets.toml",
)
@click.option(
    "--save",
    type=click.Choice(["S3", "local"], case_sensitive=False),
    default="local",
    help="Choose where to save files. If not passed default is local",
)
@click.option(
    "--classes",
    default=None,
    help="CSV with classes in the first column, you can also pass it in settings classes variable.",
)
def collect(settings, secrets, save, classes):
    load_sett_files(settings, secrets)

    validate_db()
    validate_collect()
    if save == "S3":
        validate_s3()

    c = Collect(save)
    if not classes:
        logger.info("Loading classes from settings")
        classes = s.classes
    if ".sql" not in classes:
        classes = list(pd.read_csv(classes, header=None).iloc[:, 0])
        logger.info(f"Found {len(classes)} classes")
    else:
        logger.info("Received a SQL for getting the classes")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(c.run(classes))
    logger.info("Successful collect command")


def main():
    cli()
