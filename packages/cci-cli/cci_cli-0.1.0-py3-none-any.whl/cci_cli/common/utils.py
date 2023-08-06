from enum import Enum
import os
import sys
from typing import Dict

import confuse
import typer

APP_NAME = "circleci-cli"


class OutputFormat(Enum):
    table = "table"
    json = "json"


def save_config(config_values: Dict) -> None:
    config = read_config()
    config_dir = config.config_dir()
    config_filename = confuse.CONFIG_FILENAME

    if config.exists():
        config.clear()

    config.add(config_values)
    config_full_path = os.path.join(config_dir, config_filename)
    with open(config_full_path, "w") as file:
        file.seek(0)
        file.write(config.dump())
        file.truncate()

    exit_cli(message=f"Configuration File created at {config_filename}", status_code=0)


def read_config() -> confuse.Configuration:
    return confuse.Configuration(APP_NAME)


def exit_cli(message: str, status_code: int) -> None:
    status_symbol = "✅" if status_code == 0 else "❌"
    typer.echo(f"{status_symbol}  {message}")
    sys.exit(status_code)


def show_progress():
    sys.stdout.write(".")
    sys.stdout.flush()
