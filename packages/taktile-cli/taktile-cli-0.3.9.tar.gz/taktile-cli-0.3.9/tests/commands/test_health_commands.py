import pytest

from tktl.commands.health import GetGrpcHealthCommand, GetRestHealthCommand
from tktl.core.exceptions.exceptions import APIClientException


def test_health(logged_in_context, test_user_deployed_repos):
    for repo, branch, endpoint in test_user_deployed_repos:
        cmd = GetRestHealthCommand(repository=repo, branch_name=branch, local=False)
        result = cmd.execute(endpoint_name=endpoint)
        assert result.status_code == 200

    rest_repo_name, rest_epo_branch, rest_epo_endpoint = test_user_deployed_repos[0]
    with pytest.raises(APIClientException):
        cmd = GetGrpcHealthCommand(
            repository=rest_repo_name, branch_name=rest_epo_branch, local=False
        )
        cmd.execute(endpoint_name=rest_epo_endpoint)

    grpc_repo_name, grpc_repo_branch, grpc_repo_endpoint = test_user_deployed_repos[-1]
    cmd = GetGrpcHealthCommand(
        repository=grpc_repo_name, branch_name=grpc_repo_branch, local=False
    )
    result = cmd.execute(endpoint_name=grpc_repo_endpoint)
    assert result is True
