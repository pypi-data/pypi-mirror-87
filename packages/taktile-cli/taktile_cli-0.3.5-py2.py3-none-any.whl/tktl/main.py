import click
import click_completion
import requests

from tktl.cli.common import ClickGroup
from tktl.cli.delete import delete as delete_commands
from tktl.cli.get import get as get_commands
from tktl.cli.health import health
from tktl.cli.init import init
from tktl.cli.login import login, logout
from tktl.cli.validate import validate
from tktl.commands.version import get_version
from tktl.core.config import settings
from tktl.core.exceptions import ApplicationError, TaktileSdkError
from tktl.core.loggers import LOG, set_grpc_verbosity

click_completion.init()


class TaktileGroup(ClickGroup):
    def main(self, *args, **kwargs):
        try:
            super(TaktileGroup, self).main(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            msg = (
                "Can't connect to Taktile API. "
                "Please check https://status.taktile.com/ for more information."
            )
            LOG.error(msg)
            exit(1)
        except (ApplicationError, TaktileSdkError) as e:
            if settings.DEBUG:
                raise

            LOG.error(e)


@click.group(cls=TaktileGroup, **settings.HELP_COLORS_DICT)
@click.option(
    "-v", "--verbose", is_flag=True, help="Enables verbose mode", default=False
)
def cli(verbose):
    LOG.verbose = verbose
    set_grpc_verbosity(verbose)


cli.add_command(get_version)
cli.add_command(logout)
cli.add_command(login)
cli.add_command(init)
cli.add_command(get_version)
cli.add_command(delete_commands)
cli.add_command(get_commands)
cli.add_command(validate)
cli.add_command(health)
