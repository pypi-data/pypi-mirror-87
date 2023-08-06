import os
import time

import docker

from tktl.commands.health import GetGrpcHealthCommand, GetRestHealthCommand
from tktl.core.exceptions.exceptions import APIClientException, MissingDocker
from tktl.core.loggers import LOG

TESTING_DOCKERFILE = "Dockerfile.taktile-cli-testing"


class DockerManager:
    def __init__(self, path):
        try:
            self._client = docker.from_env()
            self._path = path
        except docker.errors.DockerException as err:
            raise MissingDocker from err

    def get_docker_file(self) -> str:
        with open(os.path.join(self._path, ".dockerfile")) as fp:
            return fp.read()

    def stream_logs(self, container) -> None:
        for line in container.logs(stream=True):
            LOG.trace(f"> {line.decode()}".strip())

    def patch_docker_file(self, output: str = TESTING_DOCKERFILE):
        """patch_docker_file

        Remove the line that does the profiling
        """
        with open(os.path.join(self._path, ".dockerfile")) as fp:
            lines = fp.readlines()
            desired_contents = []
            for line in lines:
                if line.startswith("ARG"):
                    break
                desired_contents.append(line)

        with open(os.path.join(self._path, output), "w") as fp:
            fp.writelines(desired_contents)

    def remove_patched_docker_file(self, file_path: str = TESTING_DOCKERFILE):
        os.remove(os.path.join(self._path, file_path))

    def build_image(self, dockerfile: str = TESTING_DOCKERFILE) -> str:
        image = self._client.images.build(
            path=self._path, dockerfile=dockerfile, tag="taktile-cli-test"
        )
        return image[0].id

    def test_import(self, image_id: str):
        container = self._client.containers.run(
            image_id, "python -c 'from src.endpoints import tktl'", detach=True
        )
        self.stream_logs(container)

        status = container.wait()
        return status, container.logs()

    def test_unittest(self, image_id: str):
        container = self._client.containers.run(
            image_id, "python -m pytest ./user_tests/", detach=True
        )
        self.stream_logs(container)

        status = container.wait()
        return status, container.logs()

    def test_integration(self, image_id: str):
        container = self._client.containers.run(
            image_id, detach=True, ports={"80/tcp": 8080, "5005/tcp": 5005}
        )
        grpc_health_cmd = GetGrpcHealthCommand(
            branch_name="", repository="", local=True
        )
        rest_health_cmd = GetRestHealthCommand(
            branch_name="", repository="", local=True
        )

        try:
            for _ in range(5):
                try:
                    time.sleep(5)
                    rest_response = rest_health_cmd.execute(endpoint_name="")
                    grpc_response = grpc_health_cmd.execute(endpoint_name="")
                    return rest_response, grpc_response, container.logs()
                except (APIClientException, Exception):
                    pass

            return None, container.logs()
        finally:
            container.kill()
