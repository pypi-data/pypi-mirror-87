from click.testing import CliRunner

from tktl import main
from tktl.core.exceptions.exceptions import CLIError


def test_health(logged_in_context, test_user_deployed_repos):
    """Test the CLI."""
    runner = CliRunner()
    grpc_repo_name, grpc_repo_branch, grpc_repo_endpoint = test_user_deployed_repos[-1]
    for repo, branch, endpoint in test_user_deployed_repos:
        result = runner.invoke(
            main.health, ["-r", repo, "-b", branch, "-e", endpoint, "-s", "rest"]
        )
        assert result.exit_code == 0
    result = runner.invoke(
        main.health,
        [
            "-r",
            grpc_repo_name,
            "-b",
            grpc_repo_branch,
            "-e",
            grpc_repo_endpoint,
            "-s",
            "grpc",
        ],
    )
    assert result.exit_code == 0


def test_health_fail(test_user_deployed_repos):
    repo, branch, endpoint = test_user_deployed_repos[0]
    runner = CliRunner()
    result = runner.invoke(
        main.health, ["-r", repo, "-b", branch, "-e", endpoint, "-s", "rest"]
    )
    # User not logged in
    assert result.exit_code == 1


def test_health_local(logged_in_context):
    runner = CliRunner()
    result = runner.invoke(main.health, ["-s", "rest"])
    assert result.exc_info[0] == CLIError

    result = runner.invoke(main.health, ["-s", "rest", "-l"])
    assert result.exc_info[0] == SystemExit

    # No running local service
    assert result.exit_code == 1
