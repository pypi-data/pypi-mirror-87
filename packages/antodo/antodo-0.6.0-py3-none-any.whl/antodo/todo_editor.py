import os
import tempfile


class TodoEditorError(Exception):
    pass


class TodoEditor:
    def __init__(self, todo):
        self._todo = todo
        self._editor = os.getenv("EDITOR")
        if self._editor is None:
            raise TodoEditorError("env var EDITOR not set")

    def get_new_todo_content(self):
        path = self._make_todo_file()
        self._run_file_editing(path)
        new_content = _read_file(path)
        return _clean_content(new_content)

    def get_new_todo_subtask_content(self, index: int):
        path = self._make_todo_subtask_file(index)
        self._run_file_editing(path)
        new_content = _read_file(path)
        return _clean_content(new_content)

    def _make_todo_subtask_file(self, index: int):
        path = _get_templfile()
        with open(path, "w") as file:
            file.write(self._todo.subtasks[index])
        return path

    def _make_todo_file(self):
        path = _get_templfile()
        with open(path, "w") as file:
            file.write(self._todo.content)
        return path

    def _run_file_editing(self, path):
        try:
            os.system(f"{self._editor} {path}")
        except Exception as error:
            raise TodoEditorError(error)


def _clean_content(content):
    return content.replace("\n", "")


def _read_file(path):
    with open(path) as file:
        return file.read()


def _get_templfile():
    file, path = tempfile.mkstemp()
    os.close(file)
    return path
