from typing import Optional

import typer

from cci_cli.common import utils

config_app = typer.Typer()


def _evaluate_vcs(value: str):
    if value not in ["gh", "bb"]:
        raise typer.BadParameter("vcs can only be one of {'gh', 'bb'}.")
    return value


@config_app.command(help="Configure the CCI CLI")
def setup(
    vcs: Optional[str] = typer.Option(
        None,
        callback=_evaluate_vcs,
        prompt="Which VCS are you using (Github/BitBucket)",
    ),
    org: Optional[str] = typer.Option(
        None, prompt="Please input your organization/username"
    ),
    token: Optional[str] = typer.Option(
        None, prompt="Please input your CircleCI token"
    ),
):
    utils.save_config({"vcs": vcs, "organization": org, "circle_token": token})


@config_app.command(help="Display the current configuration")
def show():
    configuration = utils.read_config()
    typer.echo(configuration.dump())
