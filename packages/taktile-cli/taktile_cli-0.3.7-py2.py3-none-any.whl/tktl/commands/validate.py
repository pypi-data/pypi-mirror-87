from docker.errors import APIError
from pydantic import ValidationError

from tktl.core.exceptions.exceptions import (
    MissingDocker,
    NoContentsFoundException,
    UserRepoValidationException,
)
from tktl.core.loggers import LOG
from tktl.core.managers.docker import DockerManager
from tktl.core.managers.project import ProjectManager
from tktl.core.schemas.project import ProjectValidationOutput
from tktl.core.validation.outputs import (
    ConfigFileValidationFailure,
    ProjectValidationFailure,
)


def validate_project_config(path: str):
    try:
        ProjectManager.validate_project_config(path)
    except ValidationError as e:
        validation_output = ProjectValidationOutput(
            title=ConfigFileValidationFailure.title,
            summary=ConfigFileValidationFailure.summary,
            text=ConfigFileValidationFailure.format_step_results(validation_errors=e),
        )
        log_failure(validation_output)
        return
    except (NoContentsFoundException, UserRepoValidationException) as e:
        validation_output = ProjectValidationOutput(
            title=ProjectValidationFailure.title,
            summary=ProjectValidationFailure.summary,
            text=ProjectValidationFailure.format_step_results(validation_errors=e),
        )
        log_failure(validation_output)
        return
    LOG.log("Project scaffolding is valid!", color="green")


def log_failure(validation_output: ProjectValidationOutput):
    LOG.log(f"Project scaffolding is invalid: {validation_output.title}", color="red")
    LOG.log(validation_output.summary, color="red", err=True)
    LOG.log(validation_output.text, color="red", err=True)


def build_image(path: str, nocache: bool = False):
    dm = DockerManager(path)

    LOG.log("Patching docker file...")
    dm.patch_docker_file()
    LOG.log("Building docker image...")
    image = dm.build_image(nocache=nocache)
    dm.remove_patched_docker_file()

    return dm, image


def status_output(status, logs):
    if status["StatusCode"] == 0:
        LOG.log("Success", color="green")
    else:
        LOG.log("Error", color="red")
        print(logs.decode())


def validate_import(path: str):
    try:
        dm, image = build_image(path)
        LOG.log("Testing import of tktl...")
        status, logs = dm.test_import(image)
        status_output(status, logs)
    except MissingDocker:
        LOG.log(
            "Couldn't locate docker, please make sure it is installed, or use the DOCKER_HOST environment variable",
            color="red",
        )


def validate_unittest(path: str):
    try:
        dm, image = build_image(path)
        LOG.log("Running unittests...")
        status, logs = dm.test_unittest(image)
        status_output(status, logs)
    except MissingDocker:
        LOG.log(
            "Couldn't locate docker, please make sure it is installed, or use the DOCKER_HOST environment variable",
            color="red",
        )


def validate_integration(path: str, nocache: bool):
    try:
        dm, image = build_image(path, nocache=nocache)
        LOG.log("Waiting for service to start...")
        rest_response, grpc_response, container = dm.run_and_check_health(
            image, kill_on_success=True
        )
        if _validate_container_response(
            rest_response=rest_response,
            grpc_response=grpc_response,
            output=container.logs(),
        ):
            LOG.log("Success", color="green")
        else:
            LOG.log(
                "Unable to run container. See stack trace for more info", color="red"
            )

    except MissingDocker:
        LOG.log(
            "Couldn't locate docker, please make sure it is installed, or use the DOCKER_HOST environment variable",
            color="red",
        )


def validate_profiling(path: str, nocache: bool):
    try:
        dm, image = build_image(path, nocache=nocache)
        LOG.log("Waiting for service to start...")
        rest_response, grpc_response, container = dm.run_and_check_health(
            image, kill_on_success=False, auth_enabled=False
        )
        success = _validate_container_response(
            rest_response=rest_response,
            grpc_response=grpc_response,
            output=container.logs(),
        )
        if not success:
            LOG.log(
                "Failed to run service container, ensure service can run with `tktl validate integration`",
                color="red",
            )
            return
        try:
            LOG.log("Initiating remote profiling...")
            status, logs = dm.run_profiling_container()
            status_output(status, logs)
        finally:
            try:
                container.kill()
            except APIError:
                pass

    except MissingDocker:
        LOG.log(
            "Couldn't locate docker, please make sure it is installed, or use the DOCKER_HOST environment variable",
            color="red",
        )


def _validate_container_response(rest_response, grpc_response, output):
    if rest_response is None:
        LOG.log("Could not access REST endpoint", color="red")
        print(output.decode())
    elif rest_response.status_code != 200:
        LOG.log(f"Response status code {rest_response.status_code}", color="red")
        print(output.decode())
    elif grpc_response is None:
        LOG.log("Could not access gRPC endpoint", color="red")
    else:
        return True
    return False


def validate_all(path: str):
    validate_project_config(path)
    validate_import(path)
    validate_unittest(path)
    validate_integration(path)
    validate_profiling(path)
