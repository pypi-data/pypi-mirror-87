import os
import pathlib

HOME = str(pathlib.Path().home())
TODOS_DIR = os.path.join(HOME, ".antodo")
TODOS_JSON_PATH = os.path.join(TODOS_DIR, "todos.json")

URGENT_COLOR = "red"
CURRENT_COLOR = "green"
DEFAULT_COLOR = "white"
