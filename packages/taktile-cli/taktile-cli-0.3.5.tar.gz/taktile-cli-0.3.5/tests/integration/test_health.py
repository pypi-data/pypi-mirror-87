from tktl.commands.health import GetGrpcHealthCommand, GetRestHealthCommand
from tktl.core.config import settings


def test_health(capfd):
    rest_cmd = GetRestHealthCommand(repository="test", branch_name="master", local=True)
    grpc_cmd = GetGrpcHealthCommand(repository="test", branch_name="master", local=True)

    rest_cmd.execute("")
    out, err = capfd.readouterr()
    assert out == f"Service at {settings.LOCAL_REST_ENDPOINT} is up and running\n"

    grpc_cmd.execute("")
    out, err = capfd.readouterr()
    assert out == f"Service at {settings.LOCAL_ARROW_ENDPOINT} is up and running\n"
