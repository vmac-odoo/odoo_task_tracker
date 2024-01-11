import os
import time
from datetime import datetime
from tabulate import tabulate
import schedule
import typer

from odoo_task_tracker.api import ApiHelper


class Service:
    def __init__(
        self,
        is_scheduled,
        schedule_minutes,
        url,
        port,
        db,
        username,
        password,
        search_tasks,
        search_limit,
    ):
        self.is_scheduled = is_scheduled
        self.schedule_minutes = schedule_minutes
        self.url = url
        self.port = port
        self.db = db
        self.username = username
        self.password = password
        self.search_tasks = search_tasks
        self.search_limit = search_limit

    def clear_screen(self):
        os.system("clear")

    def transform_task_data(self, search_task, task):
        task_url = f"{self.url}/web?debug=1#id={task['id']}&cids=17&menu_id=6478&action=4043&model=project.task&view_type=form"
        return [search_task["display_name"], task["id"], task["name"], task_url]

    def fetch_tasks(self):
        api = ApiHelper(self.url, self.port, self.db, self.username, self.password)
        project_rights = api.check_rights("project.project", ["read"])
        task_rights = api.check_rights("project.task", ["read"])

        if not project_rights and task_rights:
            raise Exception("You dont have access to project or tasks")

        clean_task_count = [["SEARCH", "TASK COUNT"]]
        clean_task = [["SEARCH", "ID", "NAME", "TASK URL"]]
        for search_task in self.search_tasks:
            tasks_count_from_api = api.search_count(
                "project.task", [search_task["domain"]]
            )
            clean_task_count.append([search_task["display_name"], tasks_count_from_api])
            if tasks_count_from_api != 0 and not search_task.get(
                "disable_search", False
            ):
                tasks_from_api = api.search_read(
                    "project.task",
                    ["id", "name"],
                    [search_task["domain"]],
                    limit=self.search_limit,
                    order="id desc",
                )
                clean_task.extend(
                    map(
                        lambda task: self.transform_task_data(search_task, task),
                        tasks_from_api,
                    )
                )

        current_datetime = datetime.now()
        formatted_date = current_datetime.strftime("%A %d %B, %Y at %H:%M:%S")
        self.clear_screen()
        typer.secho(
            f"Last Update: {formatted_date}",
            fg=typer.colors.GREEN,
        )
        typer.secho("----------------------------------------------")
        typer.secho("-           SEARCH COUNT PROJECTS            -")
        typer.secho("----------------------------------------------")
        typer.secho(
            tabulate(clean_task_count, headers="firstrow", tablefmt="fancy_grid")
        )
        if len(clean_task) > 1:
            typer.secho("----------------------------------------------")
            typer.secho("-            SEARCH COUNT TASKS              -")
            typer.secho("----------------------------------------------")
            typer.secho(tabulate(clean_task, headers="firstrow", tablefmt="fancy_grid"))

    def scheduled_action(self):
        self.fetch_tasks()
        schedule.every(self.schedule_minutes).minutes.do(self.fetch_tasks)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def run_service(self):
        self.clear_screen()
        if self.is_scheduled:
            self.scheduled_action()
        else:
            self.fetch_tasks()
