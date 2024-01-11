## ODOO - TASK TRACKER
[![Python 3.9](https://img.shields.io/badge/python-3.9-purple.svg)](https://www.python.org/downloads/release/python-390/)

A simple script to schedule or single execute to review if there is any task to do.

### Instructions
1. Install requirements
```console
pip install requirements.txt
```
2. Run the next command (this will create a configuration file), and you can type where you want to save it or leave it blank.
```console
python -m odoo_task_tracker init
```

2. Set up your variables on the .json file created by init command
```json
{
    "user": "sample@odoo.com",
    "password": "password",
    "url": "https://www.url.com",
    "db": "db",
    "port": null,
    "search_limit": 5,
    "schedule_minutes": 90,
    "search": [
    ]
}
```
3. Execute in bash(out of folder)
```console
python -m odoo_task_tracker run
```

### JSON definition
- user: your email
- password: Odoo API Key
- url: Link to odoo db
- db: Name of the db
- port: Number of port (optional)
- search_limit: Limit of tasks to search and show
- schedule_minutes: Time to execute the query to the db in minutes (BE CAREFUL DON'T SET A LOW NUMBER, THIS WILL CALL TO MUCH TIMES AND YOU CAN BE BANNED)
- search: Structure for search (json array). The structure is the following:
    -  display_name: Name of the search (only to show in the table, you can put any string as you wish).
    - domain: Domain of the task search (please add to the domain the project_id)
    - disable_search (optional): if is set as true it will skip the search_read and only will count in that search

    Example:
    ```json
    [
        {
            "display_name": "Help",
            "domain": ["&", "&", "&", "&", "&", "&", "&", "&", "&", ["project_id", "=", 49], ["tag_ids", "not ilike", "perf"], ["tag_ids", "not ilike", "Internal"], ["tag_ids", "not ilike", "Apps"], ["tag_ids", "not ilike", "Administration"], ["tag_ids", "not ilike", "iap"], ["tag_ids", "not ilike", "tech_squad_infra"], ["tag_ids", "not ilike", "tech_squad_sh"], ["tag_ids", "not ilike", "special-ops"],"&",["user_ids", "=", false], ["stage_id", "ilike", "tech"],["tag_ids", "not ilike", "On-premise"]],
            "disable_search": true
        }
    ]
    ```