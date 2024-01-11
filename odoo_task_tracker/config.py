import configparser
from pathlib import Path
from typing import Dict, List

import typer

from odoo_task_tracker import (
    DB_WRITE_ERROR,
    DIR_ERROR,
    FILE_ERROR,
    SUCCESS,
    config,
    __app_name__,
)
from odoo_task_tracker.database import DatabaseHandler


CONFIG_DIR_PATH = Path(typer.get_app_dir(__app_name__))
CONFIG_FILE_PATH = CONFIG_DIR_PATH / "config-odoo-task.ini"

class ConfigurationStructure:
    user: str
    password: str
    url: str
    db: str
    port: int
    search_limit: int
    schedule_minutes: int
    search: List[Dict]

    def _set_variables(self, configuration_content: Dict):
        self.user = configuration_content.get("user")
        self.password = configuration_content.get("password")
        self.url = configuration_content.get("url")
        self.port = configuration_content.get("port")
        self.db = configuration_content.get("db")
        self.search_limit = configuration_content.get("search_limit")
        self.schedule_minutes = configuration_content.get("schedule_minutes")
        self.search = configuration_content.get("search")

    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)
        self._set_variables(self._db_handler.read_configuration().json)

class Configuration:
    
    @staticmethod
    def get_configuration():
        if config.CONFIG_FILE_PATH.exists():
            db_path = DatabaseHandler.get_database_path(config.CONFIG_FILE_PATH)
        else:
            typer.secho(
                'Config file not found. Please, run "odoo_task_tracker init"',
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)
        if db_path.exists():
            configuration = ConfigurationStructure(db_path)
            return configuration
        else:
            typer.secho(
                'Database not found. Please, run "odoo_task_tracker init"',
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)

    @staticmethod
    def init_app(db_path: str) -> int:
        """Initialize the application."""
        config_code = Configuration._init_config_file()
        if config_code != SUCCESS:
            return config_code
        database_code = Configuration._create_database(db_path)
        if database_code != SUCCESS:
            return database_code
        return SUCCESS

    @staticmethod
    def _init_config_file() -> int:
        try:
            CONFIG_DIR_PATH.mkdir(exist_ok=True)
        except OSError:
            return DIR_ERROR
        try:
            CONFIG_FILE_PATH.touch(exist_ok=True)
        except OSError:
            return FILE_ERROR
        return SUCCESS

    @staticmethod
    def _create_database(db_path: str) -> int:
        config_parser = configparser.ConfigParser()
        config_parser["General"] = {"database": db_path}
        try:
            with CONFIG_FILE_PATH.open("w") as file:
                config_parser.write(file)
        except OSError:
            return DB_WRITE_ERROR
        return SUCCESS
