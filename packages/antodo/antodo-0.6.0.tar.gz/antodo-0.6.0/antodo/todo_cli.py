import contextlib
from typing import List

import click

import antodo
from . import __version__


@click.group()
@click.version_option(__version__, "--version", "-v")
def todo_cli():
    """simple another todo CLI app"""


@todo_cli.command(help="show current todos")
def show():
    todos = antodo.Todos()
    if todos:
        todos.show()
    else:
        click.echo("No todos found")


@todo_cli.command(help="add todo")
@click.argument("content", nargs=-1, type=click.STRING)
@click.option("--urgent", "-u", is_flag=True, help="set todo as urgent")
def add(content: List[str], urgent: bool):
    content_str: str = " ".join(content)
    if not content_str:
        raise click.BadArgumentUsage("cant add empty todo")
    with todos_operation() as todos:
        todos.add_todo(content_str, urgent)


@todo_cli.command(help="removes todo")
@click.argument("indexes", nargs=-1, type=click.INT)
def remove(indexes: List[int]):
    with todos_operation() as todos:
        indexes_to_remove = filter_indexes(todos, indexes)
        todos.remove_todos(indexes_to_remove)
        click.echo(f"deleted todos: {[i+1 for i in indexes_to_remove]}")


@todo_cli.command(help="toggle todo as urgent")
@click.argument("indexes", nargs=-1, type=click.INT)
def urgent(indexes: List[int]):
    with todos_operation() as todos:
        indexes_to_set = filter_indexes(todos, indexes)
        for index in indexes_to_set:
            todos[index].toggle_urgent()


@todo_cli.command(help="toggle todo as current")
@click.argument("indexes", nargs=-1, type=click.INT)
def current(indexes: List[int]):
    with todos_operation() as todos:
        indexes_to_set = filter_indexes(todos, indexes)
        for index in indexes_to_set:
            todos[index].toggle_current()


@todo_cli.command(help="clear current todos")
@click.option("-y", "confirm", is_flag=True, help="clear without confirm promt")
def clear(confirm: bool):
    if confirm or click.confirm("Delete all todos?"):
        with todos_operation() as todos:
            todos.clear()


@todo_cli.command(help="edit todo")
@click.argument("index", type=click.INT)
def edit(index: int):
    with todos_operation() as todos:
        todo = todos[index - 1]

        editor = antodo.TodoEditor(todo)
        new_content = editor.get_new_todo_content()
        todo.content = new_content


@todo_cli.command(help="edit todo")
@click.argument("todo_index", type=click.INT)
@click.argument("sub_index", type=click.INT)
def edit_sub(todo_index: int, sub_index: int):
    with todos_operation() as todos:
        todo = todos[todo_index - 1]

        editor = antodo.TodoEditor(todo)
        new_content = editor.get_new_todo_subtask_content(sub_index - 1)
        todo.subtasks[sub_index - 1] = new_content


@todo_cli.command(help="add sub taks")
@click.argument("index", type=click.INT)
@click.argument("content", nargs=-1, type=click.STRING)
def add_sub(index: int, content: List[str]):
    content_str: str = " ".join(content)
    with todos_operation() as todos:
        todo = todos[index - 1]
        todo.add_sabtask(content_str)


@todo_cli.command(help="remove sub task")
@click.argument("todo_index", type=click.INT)
@click.argument("sub_index", type=click.INT)
def remove_sub(todo_index: int, sub_index: int):
    with todos_operation() as todos:
        todo = todos[todo_index - 1]
        todo.remove_subtask(sub_index - 1)


@contextlib.contextmanager
def todos_operation():
    todos = antodo.Todos()
    try:
        yield todos
    except Exception as err:
        raise click.ClickException(str(err))
    else:
        todos.save()
    finally:
        todos.show()


def filter_indexes(todos: antodo.Todos, indexes: List[int]):
    return [i - 1 for i in indexes if i - 1 < len(todos)]
