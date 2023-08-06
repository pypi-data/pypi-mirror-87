import pytest
from pydantic import UUID4

from tktl.commands.deployments import GetDeployments, GetEndpoints
from tktl.core.exceptions.exceptions import APIClientException
from tktl.login import logout


def test_get_deployment_commands(logged_in_context):
    cmd = GetDeployments()
    result = cmd.execute(UUID4("b15e5dd1-fbab-42bd-a646-f50d22b6b425"), "", "", "")
    assert len(result) == 1

    result = cmd.execute("", "", "", "", return_all=True)
    assert len(result) >= 3

    cmd = GetEndpoints()
    result = cmd.execute(UUID4("b15e5dd1-fbab-42bd-a646-f50d22b6b425"), "")
    assert len(result) == 0

    cmd = GetDeployments()
    with pytest.raises(APIClientException) as e:
        logout()
        cmd.execute(UUID4("b15e5dd1-fbab-42bd-a646-f50d22b6b425"), "", "", "")
