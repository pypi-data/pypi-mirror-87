import json
from typing import List

import click
import yaml
from pydantic import UUID4, BaseModel

from tktl.cli.common import LOG, ClickGroup, get_cmd_shared_options, to_uuid
from tktl.commands import deployments as deployments_commands
from tktl.core.config import settings
from tktl.core.schemas.utils import get_table_from_list_of_schemas
from tktl.login import validate_decorator


@click.group("get", help="Get resources", cls=ClickGroup, **settings.HELP_COLORS_DICT)
def get():
    pass


@get.command("deployments", help="Get deployment resources")
@click.argument("deployment_id", required=False, callback=to_uuid)
@click.option("-c", "--commit", help="SHA commit")
@click.option("-b", "--branch", help="Branch Name")
@click.option("-s", "--status", help="Status in which deployment is")
@get_cmd_shared_options
@validate_decorator
def get_deployment_by_id(
    deployment_id: UUID4,
    commit: str,
    branch: str,
    status: str,
    full: bool,
    all_resources: bool,
    output: str,
):
    command = deployments_commands.GetDeployments()
    result = command.execute(
        deployment_id=deployment_id,
        commit_sha=commit,
        branch_name=branch,
        status_name=status,
        return_all=all_resources,
    )
    keys = ["id", "Branch @ Commit", "Status"] if not full else None
    return produce_output(resources=result, keys=keys, maxwidth=350, output_kind=output)


@get.command("repositories", help="Get repository resources")
@click.argument("repository_id", required=False, callback=to_uuid)
@click.option("-r", "--repo-name", help="Repository name")
@click.option("-o", "--owner", help="Owner of the repository")
@get_cmd_shared_options
@validate_decorator
def get_repository_by_id(
    repository_id: UUID4,
    repo_name: str,
    owner: str,
    full: bool,
    all_resources: bool,
    output: str,
):
    command = deployments_commands.GetRepositories()
    result = command.execute(
        repository_id=repository_id,
        repository_name=repo_name,
        repository_owner=owner,
        return_all=all_resources,
    )
    keys = ["Name"] if not full else None
    return produce_output(resources=result, keys=keys, maxwidth=200, output_kind=output)


@get.command("endpoints", help="Get endpoint resources")
@click.argument("endpoint_id", required=False, callback=to_uuid)
@click.option("-e", "--endpoint-name", help="Endpoint name")
@get_cmd_shared_options
@validate_decorator
def get_endpoint_by_id(
    endpoint_id: UUID4,
    endpoint_name: str,
    all_resources: bool,
    output: str,
    full: bool = True,
):
    command = deployments_commands.GetEndpoints()
    result = command.execute(
        endpoint_id=endpoint_id, endpoint_name=endpoint_name, return_all=all_resources
    )
    return produce_output(resources=result, output_kind=output, keys=None, maxwidth=130)


class GenericResourceList(BaseModel):
    __root__: List


def produce_output(
    resources: List[BaseModel],
    output_kind: str,
    keys: List[str] = None,
    maxwidth: int = None,
):
    if not resources:
        LOG.error("No resources found")
        return
    if output_kind == "stdout":
        table = get_table_from_list_of_schemas(resources, maxwidth=maxwidth, keys=keys)
        LOG.log(table)
    elif output_kind == "json":
        LOG.log(GenericResourceList.parse_obj(resources).json())
    elif output_kind == "yaml":
        LOG.log(yaml.dump_all([json.loads(r.json()) for r in resources]))
