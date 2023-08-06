from typing import List

from pydantic import UUID4

from tktl.commands import BaseDeploymentApiCommand
from tktl.core.schemas.deployment import DeploymentBase
from tktl.core.schemas.repository import Endpoint


class GetDeployments(BaseDeploymentApiCommand):
    def execute(
        self,
        deployment_id: UUID4,
        commit_sha: str,
        branch_name: str,
        status_name: str,
        return_all: bool = False,
    ):
        return self.client.get_deployments(
            deployment_id=deployment_id,
            commit_sha=commit_sha,
            branch_name=branch_name,
            status_name=status_name,
            return_all=return_all,
        )


class GetRepositories(BaseDeploymentApiCommand):
    def execute(
        self,
        repository_id: UUID4,
        repository_name: str,
        repository_owner: str,
        return_all: bool = False,
    ):
        return self.client.get_repositories(
            repository_id=repository_id,
            repository_name=repository_name,
            repository_owner=repository_owner,
            return_all=return_all,
        )


class GetEndpoints(BaseDeploymentApiCommand):
    def execute(
        self, endpoint_id: UUID4, endpoint_name: str, return_all: bool = False
    ) -> List[Endpoint]:
        return self.client.get_endpoints(
            endpoint_id=endpoint_id, endpoint_name=endpoint_name, return_all=return_all
        )


class DeleteDeployment(BaseDeploymentApiCommand):
    def execute(self, deployment_id: UUID4) -> DeploymentBase:
        return self.client.delete_deployment(deployment_id=deployment_id)


class ListDeploymentsCommand(BaseDeploymentApiCommand):
    WAITING_FOR_RESPONSE_MESSAGE = "Waiting for data..."

    def execute(self, **kwargs):
        # TODO: implement list deployments and show as table

        # with halo.Halo(text=self.WAITING_FOR_RESPONSE_MESSAGE, spinner="dots"):
        #     instances = self._get_instances(**kwargs)

        raise NotImplemented


class GetDeploymentDetails(BaseDeploymentApiCommand):
    def _get_table_data(self, instance):
        pass

    def execute(self, id_):
        # TODO: get deployment details
        raise NotImplemented


class GetDeploymentMetricsCommand(BaseDeploymentApiCommand):
    def execute(
        self, deployment_id, start, end, interval, built_in_metrics, *args, **kwargs
    ):
        # TODO: stream metrics
        raise NotImplemented


class StreamDeploymentMetricsCommand(BaseDeploymentApiCommand):
    def execute(self, **kwargs):
        # TODO: stream metrics
        raise NotImplemented


class DeploymentLogsCommand(BaseDeploymentApiCommand):
    def execute(self, **kwargs):
        # TODO: get logs
        raise NotImplemented

    def _get_log_row_string(self, id, log):
        raise NotImplemented

    def _make_table(self, logs, id):
        raise NotImplemented
