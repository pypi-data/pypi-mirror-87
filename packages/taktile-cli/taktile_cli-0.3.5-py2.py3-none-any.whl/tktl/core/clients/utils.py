from typing import Any, Callable, Dict, List, Optional, Union

from pydantic import UUID4

from .. import loggers as sdk_logger
from ..exceptions import TaktileSdkError
from ..schemas.repository import Endpoint, Repository, RepositoryDeployment
from ..t import Resources

_logger = sdk_logger.SdkLogger()

default_comp = lambda x, y: x == y


def filter_prop(
    resources: List[Resources], prop_name: str, value: Any, key: Callable = default_comp
):
    if value is not None:
        return [d for d in resources if key(value, getattr(d, prop_name))]
    return resources


def filter_deployments(
    deployments: List[RepositoryDeployment],
    deployment_id: UUID4,
    commit_sha: str = None,
    branch_name: str = None,
    status_name: str = None,
) -> List[RepositoryDeployment]:
    if deployment_id:
        deployments = [d for d in deployments if d.id == deployment_id]

        if deployments:
            return deployments
        else:
            _logger.warning("No deployments with matching id found")

    for n, v in zip(
        ["commit_hash", "branch_name", "status"], [commit_sha, branch_name, status_name]
    ):
        if n == "commit_hash" and commit_sha:
            if len(commit_sha) < 40:
                comp = lambda x, y: y.startswith(x)
            else:
                comp = default_comp
        else:
            comp = default_comp
        deployments = filter_prop(deployments, prop_name=n, value=v, key=comp)

    return deployments


def filter_repositories(
    repositories: List[Repository],
    repository_id: UUID4,
    repository_name: str = None,
    repository_owner: str = None,
) -> List[Repository]:
    if repository_id:
        repositories = [r for r in repositories if r.id == repository_id]
        if repositories:
            return repositories
        else:
            _logger.warning("No repositories with matching id found")

    for n, v in zip(
        ["repository_name", "repository_owner"], [repository_name, repository_owner]
    ):
        repositories = filter_prop(repositories, prop_name=n, value=v)
    return repositories


def filter_endpoints(
    endpoints: List[Endpoint], endpoint_id: UUID4, endpoint_name: str = None
) -> List[Endpoint]:
    if endpoint_id:
        endpoints = [r for r in endpoints if r.id == endpoint_id]
        if endpoints:
            return endpoints
        else:
            _logger.warning("No endpoints with matching id found")

    for n, v in zip(["name"], [endpoint_name]):
        endpoints = filter_prop(endpoints, prop_name=n, value=v)
    return endpoints


def get_deployment_from_endpoint_and_branch(
    endpoint_mapping: List[Dict[str, Union[Endpoint, RepositoryDeployment]]],
    endpoint_name: str,
    branch_name: str = None,
) -> Optional[RepositoryDeployment]:
    filtered = [e for e in endpoint_mapping if e if e["endpoint"].name == endpoint_name]
    if len(filtered) == 0:
        _logger.warning(
            f"No endpoints with name: {endpoint_name} found across all deployed branches"
        )
        return
    if len(filtered) == 1:
        deployment = filtered[0]["deployment"]
        if branch_name is not None and deployment.branch_name != branch_name:
            _logger.warning(
                f"No endpoint {endpoint_name} for branch {branch_name}, but found one for branch: "
                f"{deployment.branch_name}. Returning that instead"
            )
        return deployment
    else:
        available_branches = set(
            [e["deployment"].branch_name for e in endpoint_mapping]
        )
        if branch_name is None:
            _logger.warning(
                f"Ambiguous: more than one branch for repository with endpoint: {endpoint_name}. Please "
                f"specify a branch. Available branches: with such endpoint: {', '.join(available_branches)}"
            )
            return
        branch_filtered = [
            e for e in filtered if e["deployment"].branch_name == branch_name
        ]
        if len(branch_filtered) == 0:
            _logger.warning(
                f"No endpoints with name: {endpoint_name} and branch {branch_name} found. Available "
                f"branches with such endpoint: {', '.join(available_branches)}"
            )
            return
        elif len(branch_filtered) == 1:
            return branch_filtered[0]["deployment"]
        else:
            print(
                [
                    (e["deployment"].branch_name, e["deployment"].status)
                    for e in endpoint_mapping
                ]
            )
            # Impossible to have more than one endpoint in the same branch for the same repo with the same name
            raise TaktileSdkError("This should never, ever happen")
