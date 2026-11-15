"""Helper that lets a normal Python script (main.py) run inside the web page.

Your script stays the same as the one you run on your PC. This file makes three things work:
  1. input() waits for you to type in the page's console.
  2. playsound() plays the sound through the browser and WAITS until it has finished
     (just like in the terminal), before the next line of your script runs.
  3. os.system("cls") / os.system("clear") clears the page's console.

How the waiting works: before running, the script is rewritten in memory so that every
call to input() or playsound() is awaited, and every function that (directly or
indirectly) calls them becomes an async function. Your main.py file itself is not changed.
"""
import ast
import inspect
import os
import sys
import types

import js

# name used in your script -> awaitable version used on the web page
ASYNC_BASE = {"input": "web_input", "playsound": "web_playsound"}


async def web_input(prompt=""):
    js.writeInline(str(prompt))
    answer = await js.waitForInput()
    return str(answer)


async def web_playsound(path, block=True):
    await js.playSoundAndWait(str(path))


def _own_nodes(node):
    """All nodes inside node, without going into nested functions or lambdas."""
    stack = list(ast.iter_child_nodes(node))
    while stack:
        current = stack.pop()
        yield current
        if isinstance(current, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            continue
        stack.extend(ast.iter_child_nodes(current))


def _is_async_call(node, async_names):
    return (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            and node.func.id in async_names)


def _find_async_functions(tree):
    functions = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    for lam in (n for n in ast.walk(tree) if isinstance(n, ast.Lambda)):
        for node in _own_nodes(lam):
            if _is_async_call(node, set(ASYNC_BASE)):
                raise RuntimeError(
                    f"input() or playsound() is used inside a lambda (line {node.lineno}). "
                    "Please use a normal def function instead.")
    async_names = set(ASYNC_BASE)
    async_functions = set()
    changed = True
    while changed:
        changed = False
        for func in functions:
            if func.name in async_functions:
                continue
            if any(_is_async_call(n, async_names) for n in _own_nodes(func)):
                async_functions.add(func.name)
                async_names.add(func.name)
                changed = True
    return async_functions


class _Asyncify(ast.NodeTransformer):
    def __init__(self, async_functions):
        self.async_functions = async_functions
        self.async_names = set(ASYNC_BASE) | async_functions

    def visit_FunctionDef(self, node):
        self.generic_visit(node)
        if node.name in self.async_functions:
            new = ast.AsyncFunctionDef(**{f: getattr(node, f) for f in node._fields})
            return ast.copy_location(new, node)
        return node

    def visit_Call(self, node):
        self.generic_visit(node)
        if _is_async_call(node, self.async_names):
            name = ASYNC_BASE.get(node.func.id, node.func.id)
            call = ast.Call(func=ast.Name(id=name, ctx=ast.Load()),
                            args=node.args, keywords=node.keywords)
            return ast.copy_location(ast.Await(value=call), node)
        return node


def _install_playsound_shim():
    def playsound(path, block=True):
        pass  # only here so "from playsound3 import playsound" works; calls are rewritten

    module = types.ModuleType("playsound3")
    module.playsound = playsound
    sys.modules["playsound3"] = module
    sys.modules["playsound"] = module


def _install_os_shim():
    def system(command):
        if str(command).strip() in ("cls", "clear"):
            js.clearConsole()
        return 0

    os.system = system


async def run_script(source, filename="main.py"):
    _install_playsound_shim()
    _install_os_shim()
    tree = ast.parse(source, filename)
    async_functions = _find_async_functions(tree)
    tree = ast.fix_missing_locations(_Asyncify(async_functions).visit(tree))
    code = compile(tree, filename, "exec", flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT)
    result = eval(code, {"__name__": "__main__",
                         "web_input": web_input, "web_playsound": web_playsound})
    if inspect.isawaitable(result):
        await result
