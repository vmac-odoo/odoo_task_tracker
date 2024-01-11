from pathlib import Path
from typing import Optional

import typer

from odoo_task_tracker import (
    ERRORS,
    __app_name__,
    __version__,
    config,
    database,
)
from odoo_task_tracker.service import Service

app = typer.Typer()

@app.command()
def run(
    scheduled: Optional[bool] = typer.Option(
        False,
        "--scheduled",
        "-s",
        help="Makes the call from the api constant.",
        is_eager=True,
    ),
    schedule_minutes: Optional[int] = typer.Option(
        False,
        "--scheduled-minutes",
        "-sm",
        help="Set the schedule minutes (override default configuration).",
        is_eager=True,
    ),
    user: Optional[str] = typer.Option(
        False,
        "--user",
        "-u",
        help="Set the user email (override default configuration).",
        is_eager=True,
    ),
    password: Optional[str] = typer.Option(
        False,
        "--password",
        "-p",
        help="Set the password (override default configuration).",
        is_eager=True,
    ),
    search_limit: Optional[int] = typer.Option(
        False,
        "--search-limit",
        "-sl",
        help="Set the search limit (override default configuration).",
        is_eager=True,
    ),
) -> None:
    """Consult tasks"""
    config_data = config.Configuration.get_configuration()
    try:
        Service(
            scheduled,
            config_data.schedule_minutes if not schedule_minutes else schedule_minutes,
            config_data.url,
            config_data.port,
            config_data.db,
            config_data.user if not user else user,
            config_data.password if not password else password,
            config_data.search,
            config_data.search_limit if search_limit else search_limit,
        ).run_service()
    except:
        typer.secho(
            f"Fetch xml rpc failing",
            fg=typer.colors.RED,
        )
        raise typer.Exit(8)


@app.command()
def init(
    db_path: str = typer.Option(
        str(database.DEFAULT_DB_FILE_PATH),
        "--db-path",
        "-db",
        prompt="config database location?",
    ),
) -> None:
    """Initialize the config database."""
    app_init_error = config.Configuration.init_app(db_path)
    if app_init_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    db_init_error = database.Database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
            f'Creating database failed with "{ERRORS[db_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"The odoo_task_tracker database is {db_path}", fg=typer.colors.GREEN
        )


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return
