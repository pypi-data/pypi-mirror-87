from dataclasses import dataclass
from dataclasses import field
from typing import List, Optional

import click

import antodo.config as c


@dataclass
class Todo:
    content: str
    urgent: bool
    current: Optional[bool] = False
    subtasks: List[str] = field(default_factory=list)

    def __str__(self) -> str:
        return self.content

    def add_sabtask(self, content: str):
        self.subtasks.append(content)

    def remove_subtask(self, sub_index: int):
        self.subtasks.pop(sub_index)

    def toggle_urgent(self):
        self.urgent = not self.urgent

    def toggle_current(self):
        self.current = not self.current

    def show(self, index: int):
        click.secho(f"{index}. {self.content}", fg=self.get_color())
        self.print_subtasks()

    def print_subtasks(self):
        if self.subtasks:
            for i, task in enumerate(self.subtasks):
                click.echo(f"\t{i+1} {task}")

    def get_color(self):
        if self.current:
            return c.CURRENT_COLOR
        if self.urgent:
            return c.URGENT_COLOR
        return c.DEFAULT_COLOR
