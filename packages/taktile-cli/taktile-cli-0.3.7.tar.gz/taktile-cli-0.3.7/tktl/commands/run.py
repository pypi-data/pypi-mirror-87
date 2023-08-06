from tktl.commands.validate import build_image
from tktl.core.exceptions.exceptions import MissingDocker
from tktl.core.loggers import LOG


def run_container(
    path: str, nocache: bool, background: False, auth_enabled: bool = True
):
    try:
        dm, image = build_image(path, nocache=nocache)
    except MissingDocker:
        LOG.log(
            "Couldn't locate docker, please make sure it is installed, or use the DOCKER_HOST environment variable",
            color="red",
        )
        return
    LOG.log("Waiting for service to start...")
    container = dm.run_container(image, detach=True, auth_enabled=auth_enabled)
    if background:
        return container
    try:
        dm.stream_logs(container)
    except KeyboardInterrupt:
        container.kill()
