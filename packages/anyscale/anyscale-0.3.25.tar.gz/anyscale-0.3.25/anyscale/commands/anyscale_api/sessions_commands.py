"""
Commands to interact with the Anyscale Sessions API
"""

from typing import Optional

import click

from anyscale.api import get_anyscale_api_client
from anyscale.formatters import common_formatter
from anyscale.sdk.anyscale_client import CreateSession, UpdateSession  # type: ignore


@click.group(
    "sessions", help="Commands to interact with the Sessions API.",
)
def sessions() -> None:
    pass


@sessions.command(
    name="list", short_help="Lists all Sessions belonging to the Project."
)
@click.argument("project_id", required=True)
@click.option(
    "--count", type=int, default=10, help="Number of projects to show. Defaults to 10."
)
@click.option(
    "--paging-token",
    required=False,
    help="Paging token used to fetch subsequent pages of projects.",
)
def list_sessions(project_id: str, count: int, paging_token: Optional[str],) -> None:
    """Lists all the non-deleted sessions under PROJECT_ID. """

    api_client = get_anyscale_api_client()
    response = api_client.list_sessions(
        project_id, count=count, paging_token=paging_token
    )

    print(common_formatter.prettify_json(response.to_dict()))


@sessions.command(name="get", short_help="Retrieves a Session.")
@click.argument("session_id", required=True)
def get_session(session_id: str) -> None:
    """Get details about the Session with id SESSION_ID"""

    api_client = get_anyscale_api_client()
    response = api_client.get_session(session_id)

    print(common_formatter.prettify_json(response.to_dict()))


@sessions.command(name="create", short_help="Creates a Session.")
@click.argument("name", required=True)
@click.argument("project_id", required=True)
@click.argument("cloud_id", required=True)
@click.argument("cluster_config", required=True)
def create_session(
    name: str, project_id: str, cloud_id: str, cluster_config: str,
) -> None:
    """Creates a Session with NAME, PROJECT_ID, CLOUD_ID, CLUSTER_CONFIG."""

    api_client = get_anyscale_api_client()
    create_data = CreateSession(
        name=name,
        cluster_config=cluster_config,
        project_id=project_id,
        cloud_id=cloud_id,
    )
    response = api_client.create_session(create_data)

    print(common_formatter.prettify_json(response.to_dict()))


@sessions.command(name="update", short_help="Updates a Session.")
@click.argument("session_id", required=True)
@click.argument("cluster_config", required=True)
def update_session(session_id: str, cluster_config: str) -> None:
    """
    Updates Session SESSION_ID with CLUSTER_CONFIG.
    """

    api_client = get_anyscale_api_client()
    update_data = UpdateSession(cluster_config=cluster_config)
    response = api_client.update_session(session_id, update_data)
    print(response)

    print(common_formatter.prettify_json(response.to_dict()))


@sessions.command(name="delete", short_help="Deletes a Session.")
@click.argument("session_id", required=True)
def delete_session(session_id: str) -> None:
    """Delete the Session with id SESSION_ID"""

    api_client = get_anyscale_api_client()
    api_client.delete_session(session_id)
