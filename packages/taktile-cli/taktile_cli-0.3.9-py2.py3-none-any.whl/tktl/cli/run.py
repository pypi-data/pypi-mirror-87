import click

from tktl.commands.run import run_container


@click.command()
@click.option(
    "--path", help="Directory where the deployment lives", required=False, default="."
)
@click.option("--nocache", help="Enable or disable using cache of images", is_flag=True)
@click.option("--background", help="Run the image in the background", is_flag=True)
@click.option(
    "--auth/--no-auth",
    help="Run with auth enabled or disabled. Enabled by default",
    default=True,
)
def run(path: str, nocache: bool, background: bool, auth: bool) -> None:
    """
    Run a deployment locally

    Parameters
    ----------
    auth
    background
    nocache
    path

    Returns
    -------

    """
    run_container(path=path, nocache=nocache, background=background, auth_enabled=auth)
