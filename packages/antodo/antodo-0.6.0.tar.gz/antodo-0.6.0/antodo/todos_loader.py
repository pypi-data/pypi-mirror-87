import os
import json
from typing import List

import safer

import antodo
import antodo.config as c


class TodosLoader:
    DEFAULT_TODOS: dict = {"todos": []}

    def __init__(self):
        self.todos_path = c.TODOS_JSON_PATH
        self.todos_dir = c.TODOS_DIR

    def load_todos(self) -> List[antodo.Todo]:
        todos_json = self._get_or_create_todos()
        todos = list(map(lambda todo: antodo.Todo(**todo), todos_json["todos"]))
        return todos

    def _get_or_create_todos(self) -> dict:
        if os.path.exists(self.todos_path):
            with open(self.todos_path) as file:
                return json.load(file)

        os.makedirs(self.todos_dir, exist_ok=True)
        with safer.open(self.todos_path, "w") as file:
            json.dump(self.DEFAULT_TODOS, file)

        return self.DEFAULT_TODOS

    def save_todos(self, todos: antodo.Todos):
        with safer.open(self.todos_path, "w") as file:
            json.dump({"todos": todos.to_json()}, file)
