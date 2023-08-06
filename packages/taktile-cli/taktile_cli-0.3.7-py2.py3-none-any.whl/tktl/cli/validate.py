import click

from tktl.cli.common import ClickGroup
from tktl.commands.validate import (
    validate_all,
    validate_import,
    validate_integration,
    validate_profiling,
    validate_project_config,
    validate_unittest,
)
from tktl.core.config import settings


@click.group(
    "validate", help="Validate the project", cls=ClickGroup, **settings.HELP_COLORS_DICT
)
def validate():
    pass


@validate.command("config", help="Validate the configuration")
@click.option(
    "--path", "-p", help="Validate project located at this path", type=str, default="."
)
def validate_config_command(path) -> None:
    """Validates a new project for the necessary scaffolding, as well as the supporting
    files needed. The directory structure of a new project.
    """
    validate_project_config(path=path)


@validate.command("import", help="Validate src/endpoints.py")
@click.option(
    "--path", "-p", help="Validate project located at this path", type=str, default="."
)
def validate_import_command(path: str) -> None:
    validate_import(path=path)


@validate.command("unittest", help="Validate the unittests")
@click.option(
    "--path", "-p", help="Validate project located at this path", type=str, default="."
)
def validate_unittest_command(path: str) -> None:
    validate_unittest(path=path)


@validate.command("integration", help="Validate integration")
@click.option(
    "--path", "-p", help="Validate project located at this path", type=str, default="."
)
@click.option("--nocache", help="Enable or disable using cache of images", is_flag=True)
def validate_integration_command(path: str, nocache: bool) -> None:
    validate_integration(path=path, nocache=nocache)


@validate.command("profiling", help="Validate profiling")
@click.option(
    "--path", "-p", help="Validate project located at this path", type=str, default="."
)
@click.option("--nocache", help="Enable or disable using cache of images", is_flag=True)
def validate_profiling_command(path: str, nocache: bool) -> None:
    validate_profiling(path=path, nocache=nocache)


@validate.command("all", help="Validate everything")
@click.option(
    "--path", "-p", help="Validate project located at this path", type=str, default="."
)
def validate_all_command(path: str) -> None:
    validate_all(path=path)
