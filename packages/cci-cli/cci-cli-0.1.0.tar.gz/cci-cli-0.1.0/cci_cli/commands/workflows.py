from requests.exceptions import HTTPError

import typer

from cci_cli.circle.api import CircleCI
from cci_cli.common import utils

workflows_app = typer.Typer()


@workflows_app.command(help="Approve a specific workflow by id")
def approve(workflow_id: str):
    cci = CircleCI()
    try:
        jobs = cci.get_workflow_jobs(workflow_id)
    except HTTPError as e:
        utils.exit_cli(
            message=e, status_code=1,
        )

    try:
        approval_request_id = next(
            job["approval_request_id"]
            for job in jobs
            if job["type"] == "approval" and job["status"] == "on_hold"
        )
    except StopIteration:
        utils.exit_cli(
            message="Error: No on_hold approval job found for workflow", status_code=1,
        )

    cci.approve_workflow(workflow_id, approval_request_id)


@workflows_app.command(help="Cancel a specific workflow by id")
def cancel(workflow_id: str):
    cci = CircleCI()
    try:
        cci.cancel_workflow(workflow_id)
    except HTTPError as e:
        utils.exit_cli(
            message=e, status_code=1,
        )


@workflows_app.command()
def rerun(workflow_id: str):
    cci = CircleCI()
    try:
        cci.rerun_workflow(workflow_id)
    except HTTPError as e:
        utils.exit_cli(
            message=e, status_code=1,
        )
