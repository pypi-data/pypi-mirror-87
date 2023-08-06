import click

from tktl.commands.health import GetGrpcHealthCommand, GetRestHealthCommand
from tktl.core.exceptions.exceptions import APIClientException, CLIError
from tktl.core.managers.auth import AuthConfigManager
from tktl.core.t import ServiceT
from tktl.login import login, logout


@click.command("health", help="Health check your endpoints")
@click.option("-r", "--repo", help="Repository owner & name: owner/repo-name")
@click.option("-e", "--endpoint-name", help="Endpoint name")
@click.option("-b", "--branch-name", help="Branch name", default="master")
@click.option(
    "-s",
    "--service",
    help="Service kind",
    type=click.Choice([ServiceT.REST.value, ServiceT.GRPC.value]),
    default=ServiceT.REST.value,
)
@click.option(
    "-l", "--local", help="Run against local endpoint", is_flag=True, default=False
)
def health(
    repo: str = None,
    endpoint_name: str = None,
    branch_name: str = "master",
    service: str = ServiceT.REST.value,
    local: bool = False,
):
    if (not repo or not endpoint_name) and not local:
        raise CLIError("If not passing repo and endpoint, must pass local = True")

    api_key = AuthConfigManager.get_api_key()
    if local and not api_key:
        login(api_key="NOT SET")
    command = (
        GetRestHealthCommand(repository=repo, branch_name=branch_name, local=local)
        if service == ServiceT.REST.value
        else GetGrpcHealthCommand(repository=repo, branch_name=branch_name, local=local)
    )
    try:
        command.execute(endpoint_name=endpoint_name)
    except (APIClientException, Exception):
        exit(1)
    finally:
        if not api_key:
            logout()
