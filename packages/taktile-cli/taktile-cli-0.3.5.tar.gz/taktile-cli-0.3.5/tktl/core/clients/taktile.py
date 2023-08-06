from collections import defaultdict
from typing import Dict, List, Union

from pydantic import UUID4

from .. import loggers as sdk_logger
from ..config import settings
from ..exceptions import TaktileSdkError
from ..managers.auth import AuthConfigManager
from ..schemas.deployment import DeploymentBase
from ..schemas.repository import (
    Endpoint,
    Repository,
    RepositoryDeployment,
    RepositoryList,
)
from ..utils import lru_cache
from .http_client import API, interpret_response
from .utils import filter_deployments, filter_endpoints, filter_repositories

_logger = sdk_logger.SdkLogger()


class TaktileClient(API):
    SCHEME: str

    def __init__(self, api_url):
        """
        Base class. All client classes inherit from it.
        """
        super().__init__(api_url)
        self.api_url = api_url
        self.api_key = AuthConfigManager.get_api_key()

    @lru_cache(timeout=50, typed=False)
    def __get_repositories(self) -> RepositoryList:
        response = self.get(f"{settings.API_V1_STR}/models")
        return interpret_response(response=response, model=RepositoryList)

    def _get_repositories(self) -> RepositoryList:
        repositories = self.__get_repositories()
        if not repositories:
            raise TaktileSdkError(
                "No repositories found on your account, so no resources can be fetched"
            )
        return repositories

    def get_deployments(
        self,
        deployment_id: UUID4 = None,
        commit_sha: str = None,
        branch_name: str = None,
        status_name: str = None,
        return_all: bool = False,
    ) -> List[RepositoryDeployment]:
        deployments = self._get_repositories().get_deployments()
        if return_all:
            return deployments
        return filter_deployments(
            deployments,
            deployment_id=deployment_id,
            commit_sha=commit_sha,
            branch_name=branch_name,
            status_name=status_name,
        )

    def get_repositories(
        self,
        repository_id: UUID4 = None,
        repository_name: str = None,
        repository_owner: str = None,
        return_all: bool = False,
    ) -> List[Repository]:
        repositories = self._get_repositories().get_repositories()
        if return_all:
            return repositories
        return filter_repositories(
            repositories,
            repository_id=repository_id,
            repository_name=repository_name,
            repository_owner=repository_owner,
        )

    def get_endpoints(
        self,
        endpoint_id: UUID4 = None,
        endpoint_name: str = None,
        return_all: bool = False,
    ) -> List[Endpoint]:
        endpoints = self._get_repositories().get_endpoints()
        if return_all:
            return endpoints
        return filter_endpoints(
            endpoints, endpoint_id=endpoint_id, endpoint_name=endpoint_name
        )

    def get_endpoints_for_repository(
        self, repository: str
    ) -> List[Dict[str, Union[Endpoint, RepositoryDeployment]]]:
        repos = self._get_repositories()
        if not repos:
            raise TaktileSdkError("No repos found")
        repo_models = repos.get_repositories()
        repo_endpoints = repos.get_endpoints()
        repo_deployments = repos.get_deployments()

        mapping = defaultdict(list)
        for repo, endpoint, deployment in zip(
            repo_models, repo_endpoints, repo_deployments
        ):
            mapping[f"{repo.repository_owner}/{repo.repository_name}"].append(
                {"endpoint": endpoint, "deployment": deployment}
            )
        if repository not in mapping.keys():
            raise TaktileSdkError(
                f"Repository {repository} not found. Available repos: {list(mapping.keys())}"
            )
        return mapping[repository]

    def delete_deployment(self, deployment_id: UUID4) -> DeploymentBase:
        response = self.delete(f"{settings.API_V1_STR}/deployments/{deployment_id}")
        return interpret_response(response=response, model=DeploymentBase)
