from typing import Any, Optional, Tuple

import click

from anyscale.controllers.session_controller import SessionController


@click.command(name="down", help="Stop the current session.")
@click.argument("session-name", required=False, default=None)
@click.option(
    "--terminate", help="Terminate the session instead of stopping it.", is_flag=True
)
@click.option(
    "--workers-only", is_flag=True, default=False, help="Only destroy the workers."
)
@click.option(
    "--keep-min-workers",
    is_flag=True,
    default=False,
    help="Retain the minimal amount of workers specified in the config.",
)
@click.option("--delete", help="Delete the session after terminating.", is_flag=True)
@click.pass_context
def anyscale_stop(
    ctx: Any,
    session_name: Optional[str],
    terminate: bool,
    workers_only: bool,
    keep_min_workers: bool,
    delete: bool,
) -> None:
    session_controller = SessionController()
    session_controller.stop(
        session_name,
        terminate=terminate,
        workers_only=workers_only,
        keep_min_workers=keep_min_workers,
        delete=delete,
    )


@click.command(
    name="up",
    context_settings=dict(ignore_unknown_options=True,),
    help="Start or update a session based on the current project configuration.",
)
@click.argument("session-name", required=False)
@click.option(
    "--config", "config", help="Cluster to start session with.", default=None,
)
@click.option(
    "--no-restart",
    is_flag=True,
    default=False,
    help=(
        "Whether to skip restarting Ray services during the update. "
        "This avoids interrupting running jobs."
    ),
)
@click.option(
    "--restart-only",
    is_flag=True,
    default=False,
    help=(
        "Whether to skip running setup commands and only restart Ray. "
        "This cannot be used with 'no-restart'."
    ),
)
@click.option(
    "--min-workers",
    required=False,
    type=int,
    help="Override the configured min worker node count for the cluster.",
)
@click.option(
    "--max-workers",
    required=False,
    type=int,
    help="Override the configured max worker node count for the cluster.",
)
@click.option(
    "--disable-sync",
    is_flag=True,
    default=False,
    help=(
        "Disables syncing file mounts and project directory. This is "
        "useful when 'restart-only' is set and file syncing takes a long time."
    ),
)
@click.option("--cloud-id", required=False, help="Id of the cloud to use", default=None)
@click.option(
    "--cloud-name", required=False, help="Name of the cloud to use", default=None
)
@click.option(
    "--yes", "-y", is_flag=True, default=False, help="Don't ask for confirmation."
)
@click.option("--verbose", "-v", help="Print out more information", is_flag=True)
def anyscale_up(
    session_name: Optional[str],
    config: Optional[str],
    min_workers: Optional[int],
    max_workers: Optional[int],
    no_restart: bool,
    restart_only: bool,
    disable_sync: bool,
    cloud_id: Optional[str],
    cloud_name: Optional[str],
    yes: bool,
    verbose: bool,
) -> None:
    session_controller = SessionController()
    session_controller.up(
        session_name,
        config,
        min_workers,
        max_workers,
        no_restart,
        restart_only,
        disable_sync,
        cloud_id,
        cloud_name,
        yes,
        verbose=verbose,
    )


@click.command(name="ssh", help="SSH into head node of cluster.")
@click.argument(
    "session-name", type=str, required=False, default=None, envvar="SESSION_NAME"
)
@click.option("-o", "--ssh-option", multiple=True)
def anyscale_ssh(session_name: str, ssh_option: Tuple[str]) -> None:
    session_controller = SessionController()
    session_controller.ssh(session_name, ssh_option)


@click.command(
    name="autopush",
    short_help="Automatically synchronize a local project with a session.",
    help="""
This command launches the autopush service that will synchronize
the state of your local project to the Anyscale session that you specify.

If there is only a single session running, this command without arguments will
default to that session.""",
)
@click.argument("session-name", type=str, required=False, default=None)
@click.option("--verbose", help="Show output from autosync.", is_flag=True)
@click.option(
    "-d",
    "--delete",
    help="Whether to delete the files that do not exist locally but are found in the cluster.",
    is_flag=True,
    default=False,
)
def anyscale_autopush(
    session_name: Optional[str], verbose: bool, delete: bool,
) -> None:
    session_controller = SessionController()
    session_controller.autopush(session_name, verbose, delete=delete)


@click.command(
    name="autosync",
    short_help="Automatically synchronize a local project with a session.",
    help="""
DEPRECATED: Renamed to autopush

This command launches the autosync service that will synchronize
the state of your local project with the Anyscale session that you specify.

If there is only a single session running, this command without arguments will
default to that session.""",
)
@click.argument("session-name", type=str, required=False, default=None)
@click.option("--verbose", help="Show output from autosync.", is_flag=True)
@click.option(
    "-d",
    "--delete",
    help="Whether to delete the files that do not exist locally but are found in the cluster.",
    is_flag=True,
    default=False,
)
@click.option(
    "-i",
    "--ignore-errors",
    help="Whether to continue syncing even when rsync returns an error code.",
    is_flag=True,
    default=False,
)
def anyscale_autosync(
    session_name: Optional[str], verbose: bool, delete: bool, ignore_errors: bool,
) -> None:
    print(
        "Deprecation warning: autosync has been renamed to autopush. autosync will "
        "be removed in a future version."
    )
    session_controller = SessionController()
    session_controller.autopush(
        session_name, verbose, delete=delete, ignore_errors=ignore_errors
    )


@click.command(name="push", help="Push current project to session.")
@click.argument(
    "session-name", type=str, required=False, default=None, envvar="SESSION_NAME"
)
@click.option(
    "--source",
    "-s",
    type=str,
    required=False,
    default=None,
    help="Source location of the files on the local file system which should"
    "be transferred. If source and target are specified, only those files/directories "
    "will be updated.",
)
@click.option(
    "--target",
    "-t",
    type=str,
    required=False,
    default=None,
    help="Target location on the head node to transfer the files to. If source "
    "and target are specified, only those files/directories will be updated.",
)
@click.option(
    "--config",
    type=str,
    required=False,
    default=None,
    help="Updates session with this configuration file.",
)
@click.option(
    "--all-nodes",
    "-A",
    is_flag=True,
    required=False,
    help="Choose to update to all nodes (workers and head) if source and target are specified.",
)
@click.pass_context
def anyscale_push(
    ctx: Any,
    session_name: str,
    source: Optional[str],
    target: Optional[str],
    config: Optional[str],
    all_nodes: bool,
) -> None:
    session_controller = SessionController()
    session_controller.anyscale_push_session(
        ctx, session_name, source, target, config, all_nodes
    )


@click.command(name="pull", help="Pull session")
@click.argument(
    "session-name", type=str, required=False, default=None, envvar="SESSION_NAME"
)
@click.option(
    "--source",
    "-s",
    type=str,
    required=False,
    default=None,
    help="Source location to transfer files located on head node of cluster "
    "from. If source and target are specified, only those files/directories "
    "will be updated.",
)
@click.option(
    "--target",
    "-t",
    type=str,
    required=False,
    default=None,
    help="Local target location to transfer files to. If source and target "
    "are specified, only those files/directories will be updated.",
)
@click.option(
    "--config",
    type=str,
    required=False,
    default=None,
    help="Pulls cluster configuration from session this location.",
)
@click.confirmation_option(
    prompt="Pulling a session will override the local project directory. Do you want to continue?"
)
def anyscale_pull(
    session_name: str,
    source: Optional[str],
    target: Optional[str],
    config: Optional[str],
) -> None:
    session_controller = SessionController()
    session_controller.pull(session_name, source, target, config)


@click.command(
    name="fork", help="Clones an existing session by name and initializes it"
)
@click.argument("session-name", type=str, required=True)
@click.argument("new-session-name", type=str, required=True)
@click.option(
    "--project-name",
    type=str,
    required=False,
    default=None,
    help="""
    Name of the project the existing session belongs to.
    By default, we will use the project configured in your current workspace.
    """,
)
def anyscale_fork(
    session_name: str, new_session_name: str, project_name: Optional[str] = None
) -> None:
    session_controller = SessionController()
    output = session_controller.fork_session(session_name, new_session_name)
    print(output)
