"""Publish CLI."""

import click
from python_on_whales import Builder, DockerClient

PLATFORMS = ["linux/amd64", "linux/arm64/v8"]


@click.command()
@click.option(
    "--docker-hub-username",
    envvar="DOCKER_HUB_USERNAME",
    help="Docker Hub username",
)
@click.option(
    "--docker-hub-token",
    envvar="DOCKER_HUB_TOKEN",
    help="Docker Hub token",
)
@click.option("--version-tag", envvar="GIT_TAG_NAME", required=True, help="Version tag")
@click.option(
    "--registry", envvar="REGISTRY", default="docker.io", help="Docker registry"
)
def main(
    docker_hub_username: str,
    docker_hub_token: str,
    version_tag: str,
    registry: str,
) -> None:
    """Build and publish image to Docker Hub.

    :param docker_hub_username:
    :param docker_hub_token:
    :param registry:
    :param publish_manually:
    :return:
    """
    reference: str = f"{registry}/pfeiffermax/device-statistics:{version_tag}"

    docker_client: DockerClient = DockerClient()
    builder: Builder = docker_client.buildx.create(
        driver="docker-container", driver_options=dict(network="host")
    )

    if docker_hub_username and docker_hub_token:
        docker_client.login(
            server=registry,
            username=docker_hub_username,
            password=docker_hub_token,
        )

    docker_client.buildx.build(
        context_path=".",
        tags=[reference],
        platforms=PLATFORMS,
        builder=builder,
        push=True,
    )

    # Cleanup
    docker_client.buildx.stop(builder)
    docker_client.buildx.remove(builder)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
