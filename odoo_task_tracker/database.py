import configparser
import json
from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from odoo_task_tracker import DB_READ_ERROR, DB_WRITE_ERROR, JSON_ERROR, SUCCESS


DEFAULT_DB_FILE_PATH = Path.home().joinpath("." + Path.home().stem + "_config.json")


class DBResponse(NamedTuple):
    json: List[Dict[str, Any]]
    error: int


class DatabaseHandler:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
    
    @staticmethod
    def init_database(db_path: Path) -> int:
        """Create the configuration database."""
        try:
            db_path.write_text(
                """
            {
                "user": "email@odoo.com",
                "password": "API-TOKEN",
                "url": "https://google.com",
                "db": "db",
                "port": null,
                "search_limit": 5,
                "schedule_minutes": 90,
                "search": []
            }
            """
            )
            return SUCCESS
        except OSError:
            return DB_WRITE_ERROR

        
    @staticmethod
    def get_database_path(config_file: Path) -> Path:
        """Return the current path to the to-do database."""
        config_parser = configparser.ConfigParser()
        config_parser.read(config_file)
        return Path(config_parser["General"]["database"])

    def read_configuration(self) -> DBResponse:
        try:
            with self._db_path.open("r") as db:
                try:
                    return DBResponse(json.load(db), SUCCESS)
                except json.JSONDecodeError:  # Catch wrong JSON format
                    return DBResponse([], JSON_ERROR)
        except OSError:  # Catch file IO problems
            return DBResponse([], DB_READ_ERROR)
