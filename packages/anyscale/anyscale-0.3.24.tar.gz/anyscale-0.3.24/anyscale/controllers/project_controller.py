import os
from typing import Optional

import click
from openapi_client.rest import ApiException  # type: ignore

import anyscale
from anyscale.api import get_api_client
from anyscale.client.openapi_client.api.default_api import DefaultApi  # type: ignore
from anyscale.project import (
    clone_cluster_config,
    create_new_proj_def,
    get_proj_id_from_name,
    load_project_or_throw,
    register_project,
)
from anyscale.util import (
    format_api_exception,
    get_endpoint,
    get_project_directory_name,
    validate_cluster_configuration,
)


class ProjectController:
    def __init__(self, api_client: Optional[DefaultApi] = None):
        if api_client is None:
            api_client = get_api_client()
        self.api_client = api_client

    def clone(self, project_name: str) -> None:
        project_id = get_proj_id_from_name(project_name, self.api_client)

        os.makedirs(project_name)
        clone_cluster_config(project_name, project_name, project_id, self.api_client)

    def init(
        self,
        name: Optional[str] = None,
        config: Optional[str] = None,
        requirements: Optional[str] = None,
    ) -> None:
        project_id_path = anyscale.project.ANYSCALE_PROJECT_FILE
        if config:
            validate_cluster_configuration(config, api_instance=self.api_client)

        if os.path.exists(project_id_path):
            # Project id exists.
            project_definition = load_project_or_throw()
            project_id = project_definition.config["project_id"]

            # Checking if the project is already registered.
            with format_api_exception(ApiException):
                # TODO: Fetch project by id rather than listing all projects
                resp = self.api_client.list_projects_api_v2_projects_get()
            for project in resp.results:
                if project.id == project_id:
                    if not os.path.exists(anyscale.project.ANYSCALE_AUTOSCALER_FILE):
                        # Session yaml file doesn't exist.
                        project_name = get_project_directory_name(
                            project.id, self.api_client
                        )
                        url = get_endpoint(f"/projects/{project.id}")
                        if click.confirm(
                            "Session configuration missing in local project. Would "
                            "you like to replace your local copy of {project_name} "
                            "with the version in Anyscale ({url})?".format(
                                project_name=project_name, url=url
                            )
                        ):
                            clone_cluster_config(
                                project_name, os.getcwd(), project.id, self.api_client
                            )
                            print(f"Created project {project.id}. View at {url}")
                            return
                    else:
                        raise click.ClickException(
                            "This project is already created at {url}.".format(
                                url=get_endpoint(f"/projects/{project.id}")
                            )
                        )
            # Project id exists locally but not registered in the db.
            if click.confirm(
                "The Anyscale project associated with this doesn't "
                "seem to exist anymore. Do you want to re-create it?",
                abort=True,
            ):
                os.remove(project_id_path)
                if os.path.exists(anyscale.project.ANYSCALE_AUTOSCALER_FILE):
                    project_name, project_definition = create_new_proj_def(
                        name,
                        project_definition.cluster_yaml(),
                        use_default_yaml=False,
                        api_client=self.api_client,
                    )
                else:
                    project_name, project_definition = create_new_proj_def(
                        name,
                        config,
                        use_default_yaml=(not bool(config)),
                        api_client=self.api_client,
                    )
        else:
            # Project id doesn't exist and not enough info to create project.
            project_name, project_definition = create_new_proj_def(
                name,
                config,
                use_default_yaml=(not bool(config)),
                api_client=self.api_client,
            )

        register_project(project_definition, self.api_client)
